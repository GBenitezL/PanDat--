from compiler.lexer import LexerClass
from compiler.directory import Variables, ScopesDirectory
from compiler.semantic_cube import get_type
from compiler.quadruple import Quadruple
from compiler.utils import data_type_IDs, operator_IDs, print_error
from collections import deque
from sly import Parser

class ParserClass(Parser):
    tokens = LexerClass.tokens

    @_('PROGRAM np_create_global_scope ID SEMI program_2 np_end_program',
       'PROGRAM np_create_global_scope ID SEMI variables program_2 np_end_program')
    def program(self, p):
        return 'ok'

    @_('function program_2',
       'main_block')
    def program_2(self, p):
        return None

    @_('MAIN np_create_main_scope LPAREN RPAREN block np_end_main',
       'MAIN np_create_main_scope LPAREN RPAREN variables block np_end_main')
    def main_block(self, p):
        pass

    @_('LBRACE statements RBRACE',
       'LBRACE RBRACE')
    def block(self, p):
        pass

    @_('variables_2')
    def variables(self, p):
        pass

    @_('VAR variables_3 variables_2',
       'VAR variables_3')
    def variables_2(self, p):
        pass

    @_('ID COLON var_type np_add_variables SEMI',
       'ID COMMA np_append_variables variables_3')
    def variables_3(self, p):
        pass

    @_('INT array',
       'FLOAT array',
       'CHAR array',
       'BOOL array')
    def var_type(self, p):
        return p[0]

    @_('LBRACKET CTEI RBRACKET',
       'epsilon')
    def array(self, p):
        pass

    @_('FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN variables np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN parameters RPAREN np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN parameters RPAREN variables np_function_start block np_function_end')
    def function(self, p):
        return None

    @_('VOID',
       'var_type')
    def return_type(self, p):
        return p[1]

    @_('ID COLON var_type np_add_variables np_add_parameters_type COMMA parameters',
       'ID COLON var_type np_add_variables np_add_parameters_type')
    def parameters(self, p):
        pass

    @_('ID LPAREN np_check_function_call np_func_end_parameters RPAREN',
       'ID LPAREN np_check_function_call function_parameters np_func_end_parameters RPAREN')
    def function_call_return(self, p):
        pass

    @_('ID LPAREN np_check_function_call np_func_end_parameters RPAREN SEMI',
       'ID LPAREN np_check_function_call function_parameters np_func_end_parameters RPAREN SEMI')
    def function_call_void(self, p):
        pass

    @_('expression expression np_add_function_call_parameters',
       'expression np_add_function_call_parameters COMMA function_parameters')
    def function_parameters(self, p):
        pass

    @_('RETURN expression np_set_return_quad SEMI')
    def return_stmt(self, p):
        pass

    @_('assignment statements_2',
       'condition statements_2',
       'write statements_2',
       'read statements_2',
       'loop statements_2',
       'return_stmt statements_2',
       'function_call_void statements_2',
       'plot statements_2',
       'regression statements_2')
    def statements(self, p):
        return (p[0], p[1])

    @_('sum',
        'mean',
        'median',
        'variance',
        'std',
        'rand',
        'corr')
    def statistics(self, p):
        pass

    @_('statements',
       'epsilon')
    def statements_2(self, p):
        return p[0]

    @_('ID np_add_id EQUALS np_add_operator expression np_quad_expression SEMI',
       'ID np_add_id LBRACKET expression RBRACKET EQUALS np_add_operator expression np_quad_expression SEMI')
    def assignment(self, p):
        pass

    @_('IF LPAREN expression RPAREN np_if_gotof block np_if_end_gotof',
       'IF LPAREN expression RPAREN np_if_gotof block ELSE np_else_goto block np_if_end_gotof')
    def condition(self, p):
        pass

    @_('exp',
       'comparison np_quad_comparison',
       'logical np_quad_logical')
    def expression(self, p):
        return p[0]

    @_('exp LT np_add_operator exp',
       'exp LE np_add_operator exp',
       'exp GT np_add_operator exp',
       'exp GE np_add_operator exp',
       'exp EQ np_add_operator exp',
       'exp NE np_add_operator exp')
    def comparison(self, p):
        return(p[1], p[2], p[3])

    @_('expression AND np_add_operator expression',
       'expression OR np_add_operator expression')
    def logical(self, p):
        pass

    @_('term np_quad_plus_minus',
       'term np_quad_plus_minus exp_2')
    def exp(self, p):
        pass

    @_('PLUS np_add_operator exp',
       'MINUS np_add_operator exp')
    def exp_2(self, p):
        pass

    @_('factor np_quad_times_div',
       'factor term_2 np_quad_times_div')
    def term(self, p):
        pass

    @_('TIMES np_add_operator term',
       'DIVIDE np_add_operator term')
    def term_2(self, p):
        pass

    @_('LPAREN np_open_parenthesis expression RPAREN np_close_parenthesis',
       'ID LBRACKET expression RBRACKET',
       'function_call_return',
       'factor_2',
       'statistics')
    def factor(self, p):
        pass

    @_('PLUS constant',
       'MINUS constant',
       'constant')
    def factor_2(self, p):
        pass

    @_('ID np_add_id',
       'CTEI np_add_int',
       'CTEF np_add_float',
       'CTEC np_add_char',
       'TRUE np_add_bool',
       'FALSE np_add_bool')
    def constant(self, p):
        pass
    
    @_('for_loop',
       'while_loop')
    def loop(self, p):
        pass

    @_('WHILE np_while_start LPAREN expression RPAREN np_while_expression block np_while_end')
    def while_loop(self, p):
        pass

    @_('FOR LPAREN ID np_add_id EQUALS np_add_operator expression np_for_expression SEMI expression np_for_limit SEMI expression RPAREN block np_for_end')
    def for_loop(self, p):
        pass

    @_('PRINT LPAREN write_2 RPAREN SEMI')
    def write(self, p):
        pass

    @_('expression np_quad_print_exp COMMA write_2_multiple',
       'expression np_quad_print_exp',
       'CTESTRING np_quad_print_str COMMA write_2_multiple',
       'CTESTRING np_quad_print_str')
    def write_2(self, p):
        pass

    @_('expression np_quad_print_multiple_exp COMMA write_2_multiple',
       'expression np_quad_print_multiple_exp',
       'CTESTRING np_quad_print_multiple_str COMMA write_2_multiple',
       'CTESTRING np_quad_print_multiple_str')
    def write_2_multiple(self, p):
        pass

    @_('READ LPAREN read_2 RPAREN np_quad_read SEMI')
    def read(self, p):
        pass

    @_('ID np_add_id',
       'ID np_add_id LBRACKET expression RBRACKET')
    def read_2(self, p):
        pass
    
    @_('SUM LPAREN ID RPAREN')
    def sum(self, p):
        pass

    @_('MEAN LPAREN ID RPAREN')
    def mean(self, p):
        pass

    @_('MEDIAN LPAREN ID RPAREN')
    def median(self, p):
        pass

    @_('VARIANCE LPAREN ID RPAREN')
    def variance(self, p):
        pass

    @_('STD LPAREN ID RPAREN')
    def std(self, p):
        pass

    @_('RAND LPAREN CTEI COMMA CTEI RPAREN')
    def rand(self, p):
        pass

    @_('CORR LPAREN ID COMMA ID RPAREN SEMI')
    def corr(self, p):
        pass
    
    @_('PLOT LPAREN ID COMMA ID COMMA CTESTRING RPAREN SEMI',
       'PLOT LPAREN ID COMMA CTESTRING RPAREN SEMI')
    def plot(self, p):
        pass

    @_('REGRESSION LPAREN ID COMMA ID RPAREN SEMI')
    def regression(self, p):
        pass

    @_('')
    def epsilon(self, p):
        return None
    

    # Neuralgic Points

    # Scopes

    @_(' ')
    def np_create_global_scope(self, p):
        global scopes, current_scope, jumps_stack
        create_scope('program', 'void')
        set_quad('GOTO', -1, -1, -1)
        jumps_stack.append(len(quadruples) - 1)

    @_(' ')
    def np_create_main_scope(self, p):
        global jumps_stack
        create_scope('main', 'void')
        main_quadruple_position = jumps_stack.pop()
        old_main_goto_quadruple = quadruples[main_quadruple_position]
        old_main_goto_quadruple.set_result(len(quadruples))

    @_(' ')
    def np_create_new_scope(self, p):
        global scopes, current_scope
        function_id = p[-3]
        return_type = p[-1]
        create_scope(function_id, return_type)
        if return_type != 'void':
            global_scope_variables = scopes.get_variables_table('program')
            global_scope_variables.add_var(function_id, return_type)
            global_scope_variables.set_arrray_values(function_id, bool_arr, arr_size)
    
    @_(' ')
    def np_end_main(self, p):
        global scopes, current_scope
        scopes.set_size(current_scope)
        scopes.set_size('program')

    @_(' ')
    def np_end_program(self, p):
        set_quad('END', -1, -1, -1)

    
    # Variables

    @_(' ')
    def np_append_variables(self, p):
        global variables_stack
        variables_stack.append(p[-1])

    @_(' ')
    def np_add_variables(self, p):
        global scopes, current_scope, variables_stack
        var_id = p[-3]
        variables_stack.append(var_id)
        variables_type = p[-1]
        while variables_stack:
            current_scope_variables = scopes.get_variables_table(current_scope)
            current_scope_variables.add_var(variables_stack[0], variables_type)
            variables_stack.popleft()

    @_(' ')
    def np_add_id(self, p):
        global operands_stack, types_stack
        current_var = get_var(p[-1])
        var_type = current_var['type']
        operands_stack.append(p[-1])
        types_stack.append(var_type)


    @_(' ')
    def np_add_int(self, p):
        global operands_stack, types_stack
        operands_stack.append(p[-1])
        types_stack.append('int')
    

    @_(' ')
    def np_add_float(self, p):
        global operands_stack, types_stack
        operands_stack.append(p[-1])
        types_stack.append('float')

    @_(' ')
    def np_add_char(self, p):
        global operands_stack, types_stack
        operands_stack.append(p[-1])
        types_stack.append('char')

    @_(' ')
    def np_add_bool(self, p):
        global scopes, current_scope
        operands_stack.append(p[-1])
        types_stack.append('bool')
        
    @_(' ')
    def np_add_operator(self, p):
        global operators_stack
        operators_stack.append(p[-1])

    @_(' ')
    def np_open_parenthesis(self, p):
        global operators_stack
        operators_stack.append(p[-1])

    @_(' ')
    def np_close_parenthesis(self, p):
        global operators_stack
        if operators_stack[-1] != '(':
            print_error('Error: \'(\' not found in operators_stack stack ', '')
        operators_stack.pop()

    # Arithmetics

    @_(' ')
    def np_quad_plus_minus(self, p):
        create_quad(['+', '-'])

    @_(' ')
    def np_quad_times_div(self, p):
        create_quad(['*', '/'])

    @_(' ')
    def np_quad_comparison(self, p):
        create_quad(['<', '<=', '>', '>=', '==', '!='])
    
    @_(' ')
    def np_quad_logical(self, p):
        create_quad(['||', '&&'])

    @_(' ')
    def np_quad_expression(self, p):
        global operators_stack, operands_stack, types_stack, quadruples
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        res_type = get_type(operator, right_type, left_type)
        if res_type == 'Error':
            print_error(f'Error: Type mismatch on {right_type}, and {left_type} with a {operator}', '')
        set_quad(operator, right_oper, -1, left_oper)


    # Read / Write

    @_(' ')
    def np_quad_read(self, p):
        global operands_stack, types_stack
        var = operands_stack.pop()
        set_quad('READ', -1, data_type_IDs[types_stack.pop()], var)

    @_(' ')
    def np_quad_print_str(self, p):
        set_quad('PRINT', -1, -1, p[-1])

    @_(' ')
    def np_quad_print_exp(self, p):
        global operands_stack, types_stack
        types_stack.pop()
        set_quad('PRINT', -1, -1, operands_stack.pop())

    @_(' ')
    def np_quad_print_multiple_str(self, p):
        set_quad('PRINT_MULTIPLE', -1, -1, p[-1])

    @_(' ')
    def np_quad_print_multiple_exp(self, p):
        global operands_stack, types_stack
        types_stack.pop()
        set_quad('PRINT_MULTIPLE', -1, -1, operands_stack.pop())


    # Non-Linear Statements

    @_(' ')
    def np_if_gotof(self, p):
        global operands_stack, types_stack, quadruples, jumps_stack
        res_if_type = types_stack.pop()
        if res_if_type == 'bool':
            set_quad('GOTOF', operands_stack.pop(), -1, -1)
            jumps_stack.append(len(quadruples) - 1)
        else:
            print_error(f'Conditional statement must be of type bool', '')
    
    @_(' ')
    def np_if_end_gotof(self, p):
        global jumps_stack, quadruples
        old_quad = quadruples[jumps_stack.pop()]
        old_quad.set_result(len(quadruples))

    @_(' ')
    def np_else_goto(self, p):
        set_quad('GOTO', -1, -1, -1)
        old_quad = quadruples[jumps_stack.pop()]
        jumps_stack.append(len(quadruples) - 1)
        old_quad.set_result(len(quadruples))

    @_(' ')
    def np_for_expression(self, p):
        global operators_stack, operands_stack, types_stack, quadruples, jumps_stack
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        if right_type == 'int' and left_type == 'int' :
            set_quad(operator, right_oper, -1, left_oper)
            jumps_stack.append(len(quadruples))
            operands_stack.append(left_oper)
            types_stack.append('int')
        else:
            print_error(f'For loop requires limits of type int', '')
    
    @_(' ')
    def np_for_limit(self, p):
        global operands_stack, types_stack, quadruples, jumps_stack
        result = operands_stack.pop()
        operand_type = types_stack.pop()

        if operand_type == 'bool':
            set_quad('GOTOV', result, -1, -1)
            jumps_stack.append(len(quadruples) - 1)
        else:
            print_error(f'For loop requires condition of type bool', '')

    @_(' ')
    def np_for_end(self, p):
        global operands_stack, types_stack, quadruples
        for_length = operands_stack.pop()
        if types_stack.pop() == 'int':
            for_value = operands_stack.pop()
            for_var_type = types_stack.pop()
        else:
            print_error('Value for For loop update variable should be int', '')
        
        if get_type('+', for_var_type, 'int') == 'int':
            set_quad('+', for_value, for_length, for_value)
            end_pos = jumps_stack.pop()
            set_quad('GOTO', -1, -1, jumps_stack.pop())
            quadruples[end_pos].set_result(len(quadruples))
        else:
            print_error(f'Cannot perform operation + to {for_var_type} and int', '')


    @_(' ')
    def np_while_start (self, p):
        jumps_stack.append(len(quadruples))

    @_(' ')
    def np_while_expression (self, p):
        exp_type = types_stack.pop()
        if exp_type == 'bool': 
            set_quad('GOTOF', operands_stack.pop(), -1, -1)
            jumps_stack.append(len(quadruples) - 1)
        else:
            print_error(f'Conditional statement must be of type bool', '')

    @_(' ')
    def np_while_end (self, p):
        end_pos = jumps_stack.pop()
        set_quad('GOTO', -1, -1, jumps_stack.pop())
        quadruples[end_pos].set_result(len(quadruples))


    # Modules
    
    @_(' ')
    def np_function_start(self, p):
        global scopes, current_scope, quadruples
        scopes.set_quad_count(current_scope, len(quadruples))

    @_(' ')
    def np_add_parameters_type(self, p):
        global scopes, current_scope
        parameter_ID = p[-4]
        parameter_type = p[-2]
        current_scope_parameters = scopes.get_parameters(current_scope)
        current_scope_IDs_parameters = scopes.get_parameter_IDs(current_scope)
        current_scope_IDs_parameters.append(parameter_ID)
        current_scope_parameters.append(parameter_type)

    @_(' ')
    def np_function_end(self, p):
        global scopes, current_scope, mem_count
        set_quad('ENDFUNC', -1, -1, -1)
        scopes.set_size(current_scope)
        mem_count.reset_local_counters()
        mem_count.reset_temp_counters()

    @_(' ')
    def np_check_function_call(self, p):
        global scopes, parameters_stack, current_function_call_ID, function_call_ID_stack, operators_stack
        current_function_call_ID = p[-2]
        if scopes.exists(current_function_call_ID):    
            parameters_stack.append(0)
            function_call_ID_stack.append(current_function_call_ID)
            set_quad('ERA', -1, -1, current_function_call_ID)
            operators_stack.append('~')
        else:
            print_error(f'Function {current_function_call_ID} is not defined', 'EC-13')

    @_(' ')
    def np_add_function_call_parameters(self, p):
        global types_stack, parameters_stack, function_call_ID_stack, scopes
        parameter_type = types_stack.pop()
        parameters_count = parameters_stack.pop()
        current_function_call_ID = function_call_ID_stack[-1]
        function_call_parameters = scopes.get_parameters(current_function_call_ID)
        
        if(function_call_parameters[parameters_count] == parameter_type):
            set_quad('PARAM', operands_stack.pop(), -1, f'_param_{parameters_count}')
            parameters_count += 1
            parameters_stack.append(parameters_count)
        else:
            print_error(f'The {parameters_count + 1}th argument of function {current_function_call_ID} should be of type {function_call_parameters[parameters_count]}', 'EC-14')
        
    @_(' ')
    def np_func_end_parameters(self, p):
        global parameters_stack, scopes, current_scope, temps_count, function_call_ID_stack, operators_stack
        current_function_call_ID = function_call_ID_stack.pop()
        size_of_parameters = len(scopes.get_parameters(current_function_call_ID))
        operators_stack.pop()
        if size_of_parameters == parameters_stack.pop():
            initial_function_addres = scopes.get_quad_count(current_function_call_ID)
            set_quad('GOSUB', current_function_call_ID, -1, initial_function_addres)
        else:
            print_error(f'Function {current_function_call_ID}, requires {size_of_parameters} arguments', 'EC-15')
        
        fun_return_type = scopes.get_return_type(current_function_call_ID)
        if fun_return_type != 'void':
            current_scope_variables = scopes.get_variables_table(current_scope)
            temp_var_name = f"_temp{temps_count}"
            temps_count += 1
            current_scope_variables.add_var(temp_var_name, fun_return_type)
            new_address = get_variables_new_address(fun_return_type, True)
            current_scope_variables.set_var_address(temp_var_name, new_address)
            directory_var = scopes.get_variables_table('program').get_one(current_function_call_ID)
            set_quad('=', directory_var['address'], -1, new_address)
            operands_stack.append(new_address)
            types_stack.append(fun_return_type)

    @_(' ')
    def np_set_return_quad(self, p):
        global current_scope, scopes, operands_stack, types_stack
        func_return_type = scopes.get_return_type(current_scope)
        if (func_return_type == types_stack.pop()):
            set_quad('RETURN', -1, -1, operands_stack.pop())
        else:
            print_error(f'Function {current_scope} must return a value of type {func_return_type}', 'EC-16')


    # Error
    def error(self, token):
        if token:
            print(f"Syntax error at token {token.var_type} ({token.value}) on line {token.lineno}")
        else:
            print("Syntax error at end of input")



# Global Variables

scopes = ScopesDirectory()
current_scope = ''

variables_stack = deque()
operators_stack = deque()
operands_stack = deque()
types_stack = deque()
jumps_stack = deque()
quadruples = [];

temps_count = 0


# Functions

def get_var(var_id):
    global scopes, current_scope
    scope_variables = scopes.get_variables_table(current_scope)
    directory_var = scope_variables.get_one(var_id)
    if (directory_var == 'not_in_directory'):
        program_variables = scopes.get_variables_table('program')
        directory_var = program_variables.get_one(var_id)
        print_error(f'Error: Variable {var_id} not found in current or global scope', '')

    return directory_var

def create_scope(scope_id, return_type):
    global scopes, current_scope
    scopes.add_new_scope(scope_id, return_type, Variables(scope_id))
    current_scope = scope_id

def create_quad(operator_to_check):
    global operands_stack, operators_stack, types_stack, scopes, current_scope, temps_count
    if len(operators_stack) > 0 and (operators_stack[-1] in operator_to_check):
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        res_type = get_type(operator, right_type, left_type)
        
        if res_type == 'Error':
            print_error(f'Invalid operation, type mismatch on {right_type} and {left_type} with a {operator}', '')
        current_scope_variables = scopes.get_variables_table(current_scope)
        temp_var_name = f"_temp{temps_count}"
        temps_count += 1
        current_scope_variables.add_var(temp_var_name, res_type)
        set_quad(operator, left_oper, right_oper, temp_var_name)
        operands_stack.append(temp_var_name)
        types_stack.append(res_type)

def set_quad(first, second, third, fourth):
    operator_id = operator_IDs[first]
    new_quadruple = Quadruple(operator_id, second, third, fourth)
    quadruples.append(new_quadruple)