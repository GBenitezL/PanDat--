import sys
import operator
import statistics
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import deque

from compiler.parser import scopes, quadruples, constants_table
from compiler.utils import print_error, data_type_values

mem_size = 10000
is_executing = True
global_mem = {}
current_mem = None
mem_stack = deque()
instruction_pointer = 0
instruction_pointer_stack = deque()
params_queue = deque()
func_call_IDs = deque()


##### MEMORY #####

def start_global_mem():
    global constants_table, global_mem, mem_size

    global_mem = {value: constant for index, (constant, value) in enumerate(constants_table.items())}
    global_size = len(constants_table) + scopes.get_size('program')
    
    check_mem(global_size)
    

def start_main_mem():
    global current_mem, mem_stack

    check_mem(scopes.get_size('main'))
    current_mem = {}

def check_mem(required_size):
    global mem_size

    if mem_size < required_size:
        print_error('Insufficient Memory', 'EE-01')
    mem_size -= required_size


def save_mem_for_function(function_ID):
    if scopes.exists(function_ID):
        check_mem(scopes.get_size(function_ID))
    else:
        print_error(f'Function {function_ID} is yet to be defined', 'EE-02')
    

##### POINTERS #####

def arithmetic_operation(left_oper, right_oper, save_address, operation):
    save_pointer_value(save_address, operation(get_pointer_value(left_oper), get_pointer_value(right_oper)))


def assign_value(value_address, save_address):
    save_pointer_value(save_address if str(save_address)[0] != '5' else find_address(save_address), 
                       get_pointer_value(value_address))


def get_pointer_value(address):
    return find_address(address if str(address)[0] != '5' else find_address(address))


def save_pointer_value(address, value):
    if int(address / 10000) == 1:
        global_mem[address] = value
    else:
        current_mem[address] = value


def update_instruction_pointer(new_pos=None):
    global instruction_pointer
    
    new_pos = new_pos if new_pos is not None else instruction_pointer + 1
    
    if new_pos > len(quadruples):
        print_error(f'Cannot locate positon {new_pos}', 'EE-03')

    instruction_pointer = new_pos


def find_address(pointer):
    value = current_mem.get(pointer) if pointer in current_mem else global_mem.get(pointer) 
    if value is None:
        print_error(f'Cannot locate value. Pointer {pointer} has not been assigned yet', 'EE-04')

    value = True if value == 'true' else False if value == 'false' else value
    return value

def find_address_no_error(pointer):
    value = current_mem.get(pointer) if pointer in current_mem else global_mem.get(pointer) 
    value = True if value == 'true' else False if value == 'false' else value
    return value

def save_pointer_value_on_input(save_address, type_to_read):
    input_value = input()
    
    try:
        if type_to_read == 1:
            input_value = int(input_value)
        elif type_to_read == 2:
            input_value = float(input_value)
        elif type_to_read == 3:
            input_value = str(input_value)
            if len(input_value) > 1:
                print_error(f'char should have a length of 1', 'EE-05')
        elif type_to_read == 4:
            if input_value == 'true':
                input_value = True
            elif input_value == 'false':
                input_value = False
            else:
                print_error(f'bool should have a value of either true or false', 'EE-06')
    except:
        print_error(f'Expected a value of type {data_type_values[type_to_read]}', 'EE-07')
    
    save_address = save_address if str(save_address)[0] != '5' else find_address(save_address)
    save_pointer_value(save_address, input_value)


##### FUNCTIONS #####

def go_to_function(function_ID, new_instruction_pointer):
    global mem_stack, instruction_pointer_stack, scopes, instruction_pointer, current_mem, func_call_IDs, params_queue

    parameter_IDs = scopes.get_parameter_IDs(function_ID)
    new_current_mem = {get_func_local_address(function_ID, parameter_ID): get_pointer_value(params_queue.popleft()) for parameter_ID in parameter_IDs}
    
    instruction_pointer_stack.append(instruction_pointer + 1)
    update_instruction_pointer(new_instruction_pointer)
    mem_stack.append(current_mem)
    current_mem = new_current_mem
    func_call_IDs.append(function_ID)

def on_function_end():
    global func_call_IDs, scopes, instruction_pointer_stack, current_mem, mem_stack, mem_size

    function_ID = func_call_IDs.pop()
    func_return_type = scopes.get_return_type(function_ID)
    
    if func_return_type != 'void':
        print_error(f'Function {function_ID} requires a return value of type {func_return_type}', 'EE-08')
        
    current_mem = mem_stack.pop()
    update_instruction_pointer(instruction_pointer_stack.pop())
    mem_size += scopes.get_size(function_ID)

def on_function_end_with_return(return_value_address):
    global func_call_IDs, scopes, instruction_pointer_stack, current_mem, mem_stack, mem_size

    function_ID = func_call_IDs.pop()
    func_return_type = scopes.get_return_type(function_ID)
    
    if data_type_values[int(str(return_value_address)[1])] != func_return_type:
        print_error(f'Function {function_ID} requires a return value of type {func_return_type}', 'EE-08')
        
    save_pointer_value(get_func_global_address(function_ID), get_pointer_value(return_value_address))
    current_mem = mem_stack.pop()
    update_instruction_pointer(instruction_pointer_stack.pop())
    mem_size += scopes.get_size(function_ID)
    
def add_parameter_for_function_call(value_address):
    params_queue.append(value_address)
    
def get_func_global_address(function_ID):
    return scopes.get_variables_table('program').get_one(function_ID).get('address')

def get_func_local_address(scope_ID, variable_ID):
    return scopes.get_variables_table(scope_ID).get_one(variable_ID).get('address')


##### ARRAYS #####

def verify_array_access(access_value, array_inferior_limit, array_upp_limit):
    value = get_pointer_value(access_value)
    inferior_limit = get_pointer_value(array_inferior_limit)
    upper_limit =  get_pointer_value(array_upp_limit)
    
    if not inferior_limit <= value < upper_limit:
        print_error(f'Out of bounds: {value} is not within the limits of {inferior_limit} and {upper_limit}', 'EE-09')

def get_array_as_list(starting_address, array_size):
    return [find_address(starting_address + x) for x in range(array_size)]

def get_array_as_list_with_none(starting_address, array_size):
    return [find_address_no_error(starting_address + x) for x in range(array_size)]


##### STATISTICS #####

def calculate_mean(array_size, array_variable_address, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, sum(find_address(array_variable_address + x) for x in range(array_size)) / array_size)

def calculate_median(array_size, array_variable_address, save_address_pointer_value):
    numbers_list = get_array_as_list(array_variable_address, array_size)
    numbers_list.sort()
    save_pointer_value(save_address_pointer_value, statistics.median(numbers_list))

def calculate_variance_value(array_size, array_variable_address, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, statistics.variance(get_array_as_list(array_variable_address, array_size)))

def calculate_std_value(array_size, array_variable_address, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, statistics.stdev(get_array_as_list(array_variable_address, array_size)))

def calculate_sum_value(array_size, array_variable_address, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, sum(get_array_as_list(array_variable_address, array_size)))

def calculate_count_value(array_size, array_variable_address, save_address_pointer_value):
    array = get_array_as_list_with_none(array_variable_address, array_size)
    count = 0
    for value in array:
        if value != None:
            count += 1
    save_pointer_value(save_address_pointer_value, count)

def calculate_iqr_value(array_size, array_variable_address, save_address_pointer_value):
    sorted_array = sorted(get_array_as_list(array_variable_address, array_size))
    q1_index = int((len(sorted_array) - 1) * 0.25)
    q3_index = int((len(sorted_array) - 1) * 0.75)
    q1 = sorted_array[q1_index]
    q3 = sorted_array[q3_index]
    iqr = q3 - q1
    save_pointer_value(save_address_pointer_value, iqr)

def create_random(lower_limit, upper_limit, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, random.randint(lower_limit, upper_limit))

def calculate_correlation(x_array_variable_address, y_array_variable_address, array_size):
    x_data = get_array_as_list(x_array_variable_address, array_size)
    y_data = get_array_as_list(y_array_variable_address, array_size)
    correlation_coef, p_value = stats.pearsonr(x_data, y_data)
    print("Correlation Coefficient:", correlation_coef)
    print("P-value:", p_value)


def calculate_linear_regression(x_array_variable_address, y_array_variable_address, array_size):
    x_data = get_array_as_list(x_array_variable_address, array_size)
    y_data = get_array_as_list(y_array_variable_address, array_size)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
    print("Slope:", slope)
    print("Intercept:", intercept)
    print("R-value:", r_value)
    print("P-value:", p_value)
    print("Standard Error:", std_err)

def find_union(array_1_address, array_2_address, array_size):
    array_1 = get_array_as_list(array_1_address, array_size)
    array_2 = get_array_as_list(array_2_address, array_size)
    print(list(set(array_1) | set(array_2)))

def find_difference(array_1_address, array_2_address, array_size):
    array_1 = get_array_as_list(array_1_address, array_size)
    array_2 = get_array_as_list(array_2_address, array_size)
    print(list(set(array_1) - set(array_2)))

def find_intersection(array_1_address, array_2_address, array_size):
    array_1 = get_array_as_list(array_1_address, array_size)
    array_2 = get_array_as_list(array_2_address, array_size)
    print(list(set(array_1) & set(array_2)))

def create_hist_plot(array_variable_address, array_size):
    sns.histplot(get_array_as_list(array_variable_address, array_size))
    plt.show()

def create_box_plot(array_variable_address, array_size):
    sns.boxplot(get_array_as_list(array_variable_address, array_size))
    plt.show()

def create_scatter_plot(x_array_variable_address, y_array_variable_address, array_size):
    x_data = get_array_as_list(x_array_variable_address, array_size)
    y_data = get_array_as_list(y_array_variable_address, array_size)
    sns.scatterplot(x=x_data, y=y_data)
    plt.show()

def create_line_plot(x_array_variable_address, y_array_variable_address, array_size):
    x_data = get_array_as_list(x_array_variable_address, array_size)
    y_data = get_array_as_list(y_array_variable_address, array_size)
    sns.lineplot(x=x_data, y=y_data)
    plt.show()

def create_bar_plot(x_array_variable_address, y_array_variable_address, array_size):
    x_data = get_array_as_list(x_array_variable_address, array_size)
    y_data = get_array_as_list(y_array_variable_address, array_size)
    sns.barplot(x=x_data, y=y_data)
    plt.show()

##### PRINTING #####

def print_value(value, multiple = False):
    is_address = type(value) is int
    if(is_address):
        value_to_print = get_pointer_value(value)
        sys.stdout.write(str(value_to_print))
    elif (value == "`n"):
        print()
    else:
        value_to_print = value[1:-1]
        sys.stdout.write(str(value_to_print))
    
    # if value_to_print == "/n":
    #     print(value_to_print)
    # else:
    #     sys.stdout.write(str(value_to_print))

# Print Global Memory
def print_global_mem():
    for index, (address, value) in enumerate(global_mem.items()):
        print(f'{index} \t\t {value} \t\t {address}')

# Print Current_Memory
def print_current_mem():
    for index, (address, value) in enumerate(current_mem.items()):
        print(f'{index} \t\t {value} \t\t {address}')


##### QUADRUPLES #####
def check_quadruples():
    global is_executing, instruction_pointer
    op_dict = {
        1: operator.add, 2: operator.sub, 3: operator.truediv, 4: operator.mul, 5: operator.lt,
        6: operator.le, 7: operator.gt, 8: operator.ge, 9: operator.eq, 10: operator.ne,
        11: operator.and_, 12: operator.or_, 30: calculate_mean, 31: calculate_median, 32: calculate_variance_value,
        33: calculate_iqr_value,
        35: calculate_std_value, 36: create_random, 37: calculate_sum_value, 38: calculate_count_value,
        34: calculate_correlation, 39: calculate_linear_regression, 40: find_union, 41: find_difference, 42: find_intersection,
        43: create_hist_plot, 44: create_box_plot, 45: create_scatter_plot, 46: create_line_plot, 47: create_bar_plot
    }
    
    while is_executing:
        quad = quadruples[instruction_pointer]
        operation = quad.get_operator()
        left_oper = quad.get_left_operator()
        right_oper = quad.get_right_operator()
        result = quad.get_result()
        match operation:
            case 28:
                is_executing = False
                print('\n\nProgram Executed Successfully\n')
            case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12:
                if operation == 3 and get_pointer_value(right_oper) == 0:
                    print_error(f'Cannot perform a division by 0', 'EE-10')
                arithmetic_operation(left_oper, right_oper, result,
                                     op_dict[operation])
                update_instruction_pointer()
            case 13:
                assign_value(left_oper, result)
                update_instruction_pointer()
            case 20:
                update_instruction_pointer(result)
            case 21:
                if get_pointer_value(left_oper):
                    update_instruction_pointer(result)
                else:
                    update_instruction_pointer()
            case 22:
                if get_pointer_value(left_oper):
                    update_instruction_pointer()
                else:
                    update_instruction_pointer(result)
            case 23:
                go_to_function(left_oper, result)
            case 24:
                save_mem_for_function(result)
                update_instruction_pointer()
            case 25:
                verify_array_access(left_oper, right_oper, result)
                update_instruction_pointer()
            case 26:
                add_parameter_for_function_call(left_oper)
                update_instruction_pointer()
            case 27:
                on_function_end()
            case 14:
                on_function_end_with_return(result)
            case 16:
                print_value(result)
                update_instruction_pointer()
            case 17:
                print_value(result, multiple=True)
                update_instruction_pointer()
            case 15:
                save_pointer_value_on_input(result, right_oper)
                update_instruction_pointer()
            case 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 45 | 46 | 47:
                op_dict[operation](left_oper,right_oper,result)
                update_instruction_pointer()
            case 43 | 44:
                op_dict[operation](left_oper, result)
                update_instruction_pointer()
            case _:
                instruction_pointer +=1




def start_vm():
    start_global_mem()
    start_main_mem()
    print('\nStarting Program Execution\n')
    check_quadruples()
    # print('Global Memory')
    # print_global_mem()
    # print('Last Memory')f
    # print_current_mem()