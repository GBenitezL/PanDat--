import sys
from compiler.lexer import LexerClass
from compiler.directory import Variables, ScopesDirectory
from compiler.semantic_cube import get_type
from compiler.quadruple import Quadruple
from compiler.memory import Memory
from compiler.utils import data_type_IDs, operator_IDs, print_error
from collections import deque
from sly import Parser

###### Parser #####

class ParserClass(Parser):
    tokens = LexerClass.tokens

    @_('PROGRAM np_create_global_scope ID SEMI program_2 np_end_program',
       'PROGRAM np_create_global_scope ID SEMI variables program_2 np_end_program')
    def program(self, p):
        # global quadruples
        # for quad in quadruples:
        #     quad.print()
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

    @_('VAR variables_2 variables',
       'VAR variables_2')
    def variables(self, p):
        pass

    @_('ID COLON variable_type np_add_variables SEMI',
       'ID np_append_variables COMMA variables_2')
    def variables_2(self, p):
        pass

    @_('INT array',
       'FLOAT array',
       'CHAR array',
       'BOOL array')
    def variable_type(self, p):
        return p[0]

    @_('LBRACKET CTEI RBRACKET np_set_as_array',
       'epsilon np_not_array')
    def array(self, p):
        pass

    @_('FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN RPAREN variables np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN parameters RPAREN np_function_start block np_function_end',
       'FUNCTION ID COLON return_type np_create_new_scope LPAREN parameters RPAREN variables np_function_start block np_function_end')
    def function(self, p):
        return None

    @_('VOID',
       'variable_type')
    def return_type(self, p):
        return p[0]

    @_('ID COLON variable_type np_add_variables np_add_parameters_type COMMA parameters',
       'ID COLON variable_type np_add_variables np_add_parameters_type')
    def parameters(self, p):
        pass

    @_('ID LPAREN np_check_function_call np_function_end_parameters RPAREN',
       'ID LPAREN np_check_function_call function_parameters np_function_end_parameters RPAREN')
    def function_call_return(self, p):
        pass

    @_('ID LPAREN np_check_function_call np_function_end_parameters RPAREN SEMI',
       'ID LPAREN np_check_function_call function_parameters np_function_end_parameters RPAREN SEMI')
    def function_call_void(self, p):
        pass

    @_('expression np_add_function_call_parameters',
       'expression np_add_function_call_parameters COMMA function_parameters')
    def function_parameters(self, p):
        pass

    @_('RETURN LPAREN expression np_set_return_quad RPAREN SEMI')
    def return_stmt(self, p):
        pass

    @_('assignment statements_2',
       'condition statements_2',
       'print statements_2',
       'read statements_2',
       'loop statements_2',
       'return_stmt statements_2',
       'function_call_void statements_2',
       'plot statements_2',
       'corr statements_2',
       'set_logic statements_2',
       'regression statements_2')
    def statements(self, p):
        return (p[0], p[1])

    @_('sum',
        'count',
        'mean',
        'median',
        'variance',
        'std',
        'rand',
        'iqr')
    def statistics(self, p):
        pass

    @_('statements',
       'epsilon')
    def statements_2(self, p):
        return p[0]

    @_('ID np_add_id EQUALS np_add_operator expression np_quad_assignment SEMI',
       'ID np_add_id LBRACKET np_check_is_array expression np_verify_value_in_array_limits RBRACKET np_get_array_address EQUALS np_add_operator expression np_quad_assignment SEMI')
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
       'ID np_add_id LBRACKET np_check_is_array expression np_verify_value_in_array_limits RBRACKET np_get_array_address',
       'function_call_return',
       'factor_2',
       'statistics')
    def factor(self, p):
        pass

    @_('PLUS constant',
       'MINUS np_set_as_negative constant',
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

    @_('WHILE np_while_start LPAREN expression RPAREN np_while_condition block np_while_end')
    def while_loop(self, p):
        pass

    @_('FOR LPAREN ID np_add_id EQUALS np_add_operator expression np_for_set_iterable SEMI expression np_for_limit SEMI expression RPAREN block np_for_end')
    def for_loop(self, p):
        pass

    @_('PRINT LPAREN print_2 RPAREN SEMI')
    def print(self, p):
        pass

    @_('expression np_quad_print_exp',
       'CTESTRING np_quad_print_str',
       'expression np_quad_print_exp COMMA print_2',
       'CTESTRING np_quad_print_str COMMA print_2',
       'new_line')
    def print_2(self, p):
        pass

    @_('NL np_quad_print_str COMMA print_2',
       'NL np_quad_print_str',
       'epsilon')
    def new_line(self, p):
        pass

    @_('READ LPAREN read_2 RPAREN np_quad_read SEMI')
    def read(self, p):
        pass

    @_('ID np_add_id',
       'ID np_add_id LBRACKET np_check_is_array expression np_verify_value_in_array_limits RBRACKET np_get_array_address')
    def read_2(self, p):
        pass
    
    @_('SUM LPAREN ID RPAREN np_set_statistics_quad')
    def sum(self, p):
        pass

    @_('COUNT LPAREN ID RPAREN np_set_statistics_quad')
    def count(self, p):
        pass

    @_('MEAN LPAREN ID RPAREN np_set_statistics_quad')
    def mean(self, p):
        pass

    @_('MEDIAN LPAREN ID RPAREN np_set_statistics_quad')
    def median(self, p):
        pass

    @_('VARIANCE LPAREN ID RPAREN np_set_statistics_quad')
    def variance(self, p):
        pass

    @_('STD LPAREN ID RPAREN np_set_statistics_quad')
    def std(self, p):
        pass

    @_('IQR LPAREN ID RPAREN np_set_statistics_quad')
    def iqr(self, p):
        pass

    @_('RAND LPAREN CTEI COMMA CTEI RPAREN np_set_rand_quad')
    def rand(self, p):
        pass

    @_('CORR LPAREN ID COMMA ID RPAREN np_verify_same_length np_set_corr_quad SEMI')
    def corr(self, p):
        pass
    
    @_('union',
       'diff',
       'intersect')
    def set_logic(self, p):
        pass

    @_('UNION LPAREN ID COMMA ID RPAREN np_set_stat_print_quad SEMI')
    def union(self, p):
        pass

    @_('DIFF LPAREN ID COMMA ID RPAREN np_set_stat_print_quad SEMI')
    def diff(self, p):
        pass

    @_('INTERSECT LPAREN ID COMMA ID RPAREN np_set_stat_print_quad SEMI')
    def intersect(self, p):
        pass

    @_('one_array_plot',
       'two_array_plot')
    def plot(self, p):
        pass

    @_('hist_plot',
       'box_plot')
    def one_array_plot(self, p):
        pass

    @_('scatter_plot',
       'line_plot',
       'bar_plot')
    def two_array_plot(self, p):
        pass

    @_('HISTPLOT LPAREN ID RPAREN np_set_one_array_plot SEMI')
    def hist_plot(self, p):
        pass
    
    @_('BOXPLOT LPAREN ID RPAREN np_set_one_array_plot SEMI')
    def box_plot(self, p):
        pass

    @_('SCATTERPLOT LPAREN ID COMMA ID RPAREN np_verify_same_length np_set_two_array_plot SEMI')
    def scatter_plot(self, p):
        pass

    @_('LINEPLOT LPAREN ID COMMA ID RPAREN np_verify_same_length np_set_two_array_plot SEMI')
    def line_plot(self, p):
        pass

    @_('BARPLOT LPAREN ID COMMA ID RPAREN np_verify_same_length np_set_two_array_plot SEMI')
    def bar_plot(self, p):
        pass

    @_('REGRESSION LPAREN ID COMMA ID RPAREN np_set_stat_print_quad SEMI')
    def regression(self, p):
        pass

    @_('')
    def epsilon(self, p):
        return None
    

    ##### Neuralgic Points #####

    ##### Scopes #####

    # Se crea un scope global de tipo void con id "program", y se genera el cuádruplo GOTO para el main
    @_(' ')
    def np_create_global_scope(self, p):
        global scopes, current_scope, jumps_stack
        create_scope('program', 'void')
        set_quad('GOTO', -1, -1, -1)
        goto_jump = len(quadruples) - 1
        jumps_stack.append(goto_jump)
        create_constant_int_address(0)

    # Se crea un scope "main" de tipo void y se llena el cuádruplo de GOTO main
    @_(' ')
    def np_create_main_scope(self, p):
        global jumps_stack
        create_scope('main', 'void')
        main_quad = jumps_stack.pop()
        quadruples[main_quad].set_result(len(quadruples))

    # Se crea un scope nuevo con su ID y tipo de retorno. Se crea una variable global 
    # con su mismo ID y tipo de retorno, a menos de que sea void
    @_(' ')
    def np_create_new_scope(self, p):
        global scopes
        function_ID = p[-3]
        return_type = p[-1]
        create_scope(function_ID, return_type)
        if return_type != 'void':
            global_scope_variables = scopes.get_variables_table('program')
            global_scope_variables.add_variable(function_ID, return_type)
            global_scope_variables.set_variable_address(function_ID, get_new_address(return_type, False, 1, 'program'))
            global_scope_variables.set_array_values(function_ID, is_array, array_size)
    
    # Calcula y asigna las memorias de los scope "main" y "program" (global)
    @_(' ')
    def np_end_main(self, p):
        global scopes, current_scope
        scopes.set_size(current_scope)
        scopes.set_size('program')

    # Se genera un cuádruplo END para indicarle a la máquina virtual que termine la ejecución
    @_(' ')
    def np_end_program(self, p):
        set_quad('END', -1, -1, -1)

    
    ##### Variables #####

    # Agrega las variables a su pila. Se usa para declarar múltiples variables en una sola línea.
    @_(' ')
    def np_append_variables(self, p):
        global variables_stack
        variables_stack.append(p[-1])

    # Se sacan todas las variables de la pila y se generan sus direcciones para cada una.
    # Se usa la variable global is_array para asignar si son arreglos 
    # Se asigna 1 como espacio de memoria, a menos de que sean arreglos, entonces se les asigna su tamaño
    @_(' ')
    def np_add_variables(self, p):
        global scopes, current_scope, is_array, array_size, variables_stack
        variables_stack.append(p[-3])
        variables_type = p[-1]
        memory_space = 1 if array_size is None else array_size
        while variables_stack:
            current_scope_variables = scopes.get_variables_table(current_scope)
            variable_ID = variables_stack[0]
            current_scope_variables.add_variable(variable_ID, variables_type)
            current_scope_variables.set_variable_address(variable_ID, get_new_address(variables_type, False, memory_space))
            current_scope_variables.set_array_values(variable_ID, is_array, array_size)
            variables_stack.popleft()

    # Verifica que el ID existe. Se agrega su dirección y tipo a las pilas correspondientes.
    @_(' ')
    def np_add_id(self, p):
        global operands_stack, types_stack
        variable_ID = p[-1]
        current_variable = get_variable_directory(variable_ID)
        operands_stack.append(current_variable['address'])
        types_stack.append(current_variable['type'])

    # Si el entero no existe en la tabla de constantes, lo agrega y le asigna una memoria.
    # Agrega su dirección y tipo a las pilas correspondientes.
    @_(' ')
    def np_add_int(self, p):
        global operands_stack, types_stack, memory, constants_table
        constant_int = p[-1]
        if constant_int not in constants_table:
            constants_table[constant_int] = memory.counters['const']['int']
            memory.set_count('const', 'int')
        operands_stack.append(constants_table[constant_int])
        types_stack.append('int')
    

    # Si el flotante no existe en la tabla de constantes, lo agrega y le asigna una memoria.
    # Agrega su dirección y tipo a las pilas correspondientes.
    @_(' ')
    def np_add_float(self, p):
        global operands_stack, types_stack, memory, constants_table
        constant_float = p[-1]
        if constant_float not in constants_table:
            constants_table[constant_float] = memory.counters['const']['float']
            memory.set_count('const', 'float')
        operands_stack.append(constants_table[constant_float])
        types_stack.append('float')

    # Si el caracter no existe en la tabla de constantes, lo agrega y le asigna una memoria.
    # Agrega su dirección y tipo a las pilas correspondientes.
    @_(' ')
    def np_add_char(self, p):
        global operands_stack, types_stack, memory, constants_table
        constant_char = p[-1]
        if constant_char not in constants_table:
            constants_table[p[-1]] = memory.counters['const']['char']
            memory.set_count('const', 'char')
        operands_stack.append(constants_table[constant_char])
        types_stack.append('char')

    # Si el booleano no existe en la tabla de constantes, lo agrega y le asigna una memoria.
    # Agrega su dirección y tipo a las pilas correspondientes.
    @_(' ')
    def np_add_bool(self, p):
        global scopes, current_scope, memory, constants_table, operands_stack, types_stack
        constant_bool = p[-1]
        if constant_bool not in constants_table:
            constants_table[constant_bool] = memory.counters['const']['bool']
            memory.set_count('const', 'bool')
        operands_stack.append(constants_table[p[-1]])
        types_stack.append('bool')

    # Agrega -1 a la tabla de constantes y a la pila de operandos, junto con un operador de multiplicacion
    # Esto hace que el siguiente valor sea negativo.
    @_(' ')    
    def np_set_as_negative(self, p):
        global memory, constants_table, operands_stack, types_stack, operators_stack
        if -1 not in constants_table:
            constants_table[-1] = memory.counters['const']['int']
            memory.set_count('const', 'int')
        operands_stack.append(constants_table[-1])
        types_stack.append('int')
        operators_stack.append('*')

    # Agrega el operador a la pila de operadores
    @_(' ')
    def np_add_operator(self, p):
        global operators_stack
        operators_stack.append(p[-1])

    # Agrega un parentésis a la pila de operadores, el cual funciona como un fondo falso
    @_(' ')
    def np_open_parenthesis(self, p):
        global operators_stack
        operators_stack.append(p[-1])

    # Verifica que la pila de operadores contenga un paréntesis, y lo saca.
    @_(' ')
    def np_close_parenthesis(self, p):
        global operators_stack
        if operators_stack[-1] != '(':
            print_error('Error: Unbalanced parenthesis ', 'EC-08')
        operators_stack.pop()

    ##### Arithmetics #####

    # Llama a la función create_quad con ['+', '-'], la cual verifica que el cubo semántico permita
    # la operacion con los tipos, y guarda el resultado en una variable temporal, la cual se agrega
    # a la pila de operandos junto con su tipo.
    @_(' ')
    def np_quad_plus_minus(self, p):
        create_quad(['+', '-'])

    # Llama a la función create_quad con ['*', '/']
    @_(' ')
    def np_quad_times_div(self, p):
        create_quad(['*', '/'])

    # Llama a la función create_quad con ['<', '<=', '>', '>=', '==', '!=']
    @_(' ')
    def np_quad_comparison(self, p):
        create_quad(['<', '<=', '>', '>=', '==', '!='])
    
    # Llama a la función create_quad con ['||', '&&']
    @_(' ')
    def np_quad_logical(self, p):
        create_quad(['||', '&&'])

    # Valida que la asignación de variables sea del mismo tipo y genera un cuádruplo de asignación.
    @_(' ')
    def np_quad_assignment(self, p):
        global operators_stack, operands_stack, types_stack, quadruples
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        res_type = get_type(operator, right_type, left_type)
        if res_type == 'Error':
            print_error(f'Error: Type mismatch on "{right_type}", and "{left_type}" with a "{operator}"', 'EC-01')
        set_quad(operator, right_oper, -1, left_oper)


    ##### Read / Write #####

    # Genera un cuádruplo READ indicando la dirección de la variable y su tipo 
    @_(' ')
    def np_quad_read(self, p):
        global operands_stack, types_stack
        variable_to_read = operands_stack.pop()
        variable_type = types_stack.pop()
        set_quad('READ', -1, data_type_IDs[variable_type], variable_to_read)

    # Genera un cuádruplo PRINT con el "letrero" a leer
    @_(' ')
    def np_quad_print_str(self, p):
        string_to_print = p[-1]
        set_quad('PRINT', -1, -1, string_to_print)

    # Genera un cuádruplo PRINT con el último valor de la pila de operandos
    @_(' ')
    def np_quad_print_exp(self, p):
        global operands_stack, types_stack
        value_to_print = operands_stack.pop()
        types_stack.pop()
        set_quad('PRINT', -1, -1, value_to_print)


    ##### Non-Linear Statements #####

    # Verifica que la condición sea de tipo booleana, y genera un cuádruplo GOTOF con la condición a evaluar
    # Agrega el salto al cuádruplo anterior a la pila de saltos.
    @_(' ')
    def np_if_gotof(self, p):
        global operands_stack, types_stack, quadruples, jumps_stack
        condition_variable_type = types_stack.pop()
        if condition_variable_type == 'bool':
            condition_value = operands_stack.pop()
            set_quad('GOTOF', condition_value, -1, -1)
            gotof_jump = len(quadruples) - 1
            jumps_stack.append(gotof_jump)
        else:
            print_error(f'Conditional statement must be of type bool', 'EC-09')
    
    # Se llena el cuádruplo del GOTOF con el valor del cuádruplo actual
    @_(' ')
    def np_if_end_gotof(self, p):
        global jumps_stack, quadruples
        quad_to_fill = quadruples[jumps_stack.pop()]
        quad_to_fill.set_result(len(quadruples))

    # Se genera un cuádruplo GOTO
    # Se llena el cuádruplo donde se inicia la condición actual
    @_(' ')
    def np_else_goto(self, p):
        set_quad('GOTO', -1, -1, -1)
        quad_to_fill = quadruples[jumps_stack.pop()]
        goto_jump = len(quadruples) - 1
        jumps_stack.append(goto_jump)
        quad_to_fill.set_result(len(quadruples))

    # Se valida que la variable iterable y el valor inicial sean de tipo entero.
    # Se asigna el valor inicial y se introduce la posición actual a la pila de saltos.
    @_(' ')
    def np_for_set_iterable(self, p):
        global operators_stack, operands_stack, types_stack, quadruples, jumps_stack
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        if right_type == 'int' and left_type == 'int':
            set_quad(operator, right_oper, -1, left_oper)
            jumps_stack.append(len(quadruples))
            operands_stack.append(left_oper)
            types_stack.append('int')
        else:
            print_error(f'For loop requires limits of type int', 'EC-10')
    
    # Se valida que la condición del for sea tipo booleana.
    # Se genera un cuádruplo GOTOV que se utiliza para cerrar el for, y se añade su posición a la pila de saltos.
    @_(' ')
    def np_for_limit(self, p):
        global operands_stack, types_stack, quadruples, jumps_stack
        result = operands_stack.pop()
        operand_type = types_stack.pop()

        if operand_type == 'bool':
            set_quad('GOTOV', result, -1, -1)
            jumps_stack.append(len(quadruples) - 1)
        else:
            print_error(f'For loop requires condition of type bool', 'EC-11')

    # Verifica que el valor del incremento sea de tipo entero
    # Genera un cuádruplo para sumar la variable iterable con el incremento.
    # Genera un cuádruplo GOTO hacia la posición inicial del for
    # Actualiza el cuádruplo del GOTO anterior con la posición final del for.
    @_(' ')
    def np_for_end(self, p):
        global operands_stack, types_stack, quadruples
        for_step = operands_stack.pop()
        if types_stack.pop() == 'int':
            for_variable_value = operands_stack.pop()
            for_variable_type = types_stack.pop()
        else:
            print_error('Value for For loop update variable should be int', 'EC-12')
        
        if get_type('+', for_variable_type, 'int') == 'int':
            set_quad('+', for_variable_value, for_step, for_variable_value)
            end_position = jumps_stack.pop()
            return_position = jumps_stack.pop()
            set_quad('GOTO', -1, -1, return_position)
            quadruples[end_position].set_result(len(quadruples))
        else:
            print_error(f'Cannot perform operation + to {for_variable_type} and int', 'EC-01')


    # Se agrega la posición actual a la pila de saltos para poder regresar
    @_(' ')
    def np_while_start (self, p):
        jumps_stack.append(len(quadruples))

    # Se verifica que la expresión sea booleana y se genera un cuádruplo GOTOF con la condición a evaluar
    @_(' ')
    def np_while_condition (self, p):
        condition_type = types_stack.pop()
        condition_value = operands_stack.pop()
        if condition_type == 'bool': 
            set_quad('GOTOF', condition_value, -1, -1)
            jumps_stack.append(len(quadruples) - 1)
        else:
            print_error(f'Conditional statement must be of type bool', 'EC-09')

    # Se agrega un GOTO al inicio del while para que regrese y evalúe la condición hasta que sea falsa
    # Se actualiza el GOTO del while para indicar la posición en la cual termina
    @_(' ')
    def np_while_end (self, p):
        end_position = jumps_stack.pop()
        set_quad('GOTO', -1, -1, jumps_stack.pop())
        quadruples[end_position].set_result(len(quadruples))


    ##### Modules #####
    
    # Se guarda la posición donde inicia la función en el directorio de funciones
    @_(' ')
    def np_function_start(self, p):
        global scopes, current_scope, quadruples
        scopes.set_quad_count(current_scope, len(quadruples))

    # Agrega el ID del parámetro y su tipo al directorio del scope de la función
    @_(' ')
    def np_add_parameters_type(self, p):
        global scopes, current_scope
        parameter_ID = p[-4]
        parameter_type = p[-2]
        current_scope_parameters = scopes.get_parameters(current_scope)
        current_scope_parameters.append(parameter_type)
        current_scope_IDs_parameters = scopes.get_parameter_IDs(current_scope)
        current_scope_IDs_parameters.append(parameter_ID)

    # Se genera un cuádruplo ENDFUNC y se establece el tamaño de memoria para la función.
    # Se reinician los contadores de memoria locales y temporales.
    @_(' ')
    def np_function_end(self, p):
        global scopes, current_scope, memory
        set_quad('ENDFUNC', -1, -1, -1)
        scopes.set_size(current_scope)
        memory.reset_local_counters()
        memory.reset_temp_counters()

    # Verifica que el nombre de la función exista en el directorio de scopes.
    # Se genera un cuádruplo ERA con el id de la función. Este tendrá que ser verificado en ejecución.
    @_(' ')
    def np_check_function_call(self, p):
        global scopes, parameters_stack, current_function_call_ID, function_call_ID_stack, operators_stack
        current_function_call_ID = p[-2]
        if scopes.exists(current_function_call_ID):    
            parameters_stack.append(0)
            function_call_ID_stack.append(current_function_call_ID)
            set_quad('ERA', -1, -1, current_function_call_ID)
            # Fondo falso
            operators_stack.append('fb_function')
        else:
            print_error(f'Function {current_function_call_ID} is not defined', 'EC-13')

    # Valida que el parámetro tenga el mismo tipo que el de la firma de la función
    # Se crea un cuádruplo PARAM con el valor del parámetro y su número (posición en la firma)
    @_(' ')
    def np_add_function_call_parameters(self, p):
        global types_stack, parameters_stack, function_call_ID_stack, scopes
        parameter_type = types_stack.pop()
        parameters_count = parameters_stack.pop()
        current_function_call_ID = function_call_ID_stack[-1]
        function_call_parameters = scopes.get_parameters(current_function_call_ID)
        
        if(function_call_parameters[parameters_count] == parameter_type):
            parameter_value = operands_stack.pop()
            set_quad('PARAM', parameter_value, -1, f'_param_{parameters_count}')
            parameters_count += 1
            parameters_stack.append(parameters_count)
        else:
            print_error(f'The {parameters_count + 1}th argument of function {current_function_call_ID} should be of type {function_call_parameters[parameters_count]}', 'EC-14')
        
    # Verifica que la cantidad de parámetros de la llamada sea la misma a la cantidad de parámetros de la firma
    # Además, genera una nueva variable temporal para almacenar el valor que regresa la función (a menos de que sea tipo void)
    # Se genera un cuádruplo de asignación para asignar dicho valor y se agrega a la pila de operandos.
    @_(' ')
    def np_function_end_parameters(self, p):
        global parameters_stack, scopes, current_scope, temps_count, function_call_ID_stack, operators_stack
        current_function_call_ID = function_call_ID_stack.pop()
        size_of_parameters = len(scopes.get_parameters(current_function_call_ID))
        # Fondo falso
        operators_stack.pop()
        if size_of_parameters == parameters_stack.pop():
            initial_function_address = scopes.get_quad_count(current_function_call_ID)
            set_quad('GOSUB', current_function_call_ID, -1, initial_function_address)
        else:
            print_error(f'Function {current_function_call_ID}, requires {size_of_parameters} arguments', 'EC-15')
        
        fun_return_type = scopes.get_return_type(current_function_call_ID)
        if fun_return_type != 'void':
            current_scope_variables = scopes.get_variables_table(current_scope)
            temp_variable_name = f"_temp{temps_count}"
            temps_count += 1
            current_scope_variables.add_variable(temp_variable_name, fun_return_type)
            new_address = get_new_address(fun_return_type, True)
            current_scope_variables.set_variable_address(temp_variable_name, new_address)
            function_global_variable = scopes.get_variables_table('program').get_one(current_function_call_ID)
            set_quad('=', function_global_variable['address'], -1, new_address)
            operands_stack.append(new_address)
            types_stack.append(fun_return_type)

    # Se verifica que el valor a retornar (temporal asignado) sea igual al tipo de la función
    # Se genera el cuádruplo RETURN con el valor a retornar
    @_(' ')
    def np_set_return_quad(self, p):
        global current_scope, scopes, operands_stack, types_stack
        function_return_type = scopes.get_return_type(current_scope)
        if (function_return_type == types_stack.pop()):
            set_quad('RETURN', -1, -1, operands_stack.pop())
        else:
            print_error(f'Function {current_scope} must return a value of type {function_return_type}', 'EC-16')

    ##### Arrays #####

    # Se verifica que el arreglo se declare con una constante mayor o igual a 1
    # Se agrega dicha constante la tabla de constantes
    @_(' ')
    def np_set_as_array(self, p):
        global is_array, array_size
        is_array = True
        array_size = p[-2]
        create_constant_int_address(array_size) if array_size >= 1 else print_error('Array size should be greater than 1', 'EC-05')

    # Restablece las globales is_array y array_size cuando se lee una variable no dimensionada.
    @_(' ')
    def np_not_array(self, p):
        global is_array, array_size
        is_array = False
        array_size = None

    # Se verifica que la dirección esté en el directorio de variables local o global y que sea un arreglo.
    # Se agrega un fondo falso para permitir casos en el que el valor a asignar sea una expresión con un arreglo
    @_(' ')
    def np_check_is_array(self, p):
        global operands_stack, types_stack, operators_stack
        # Quita la direccion de np_add_id
        operands_stack.pop()   
        types_stack.pop()
        array_ID = p[-3]

        current_variable = get_variable_directory(array_ID)
        if current_variable['is_array']:
            operands_stack.append(current_variable['address'])
            types_stack.append(current_variable['type'])
            # Fondo falso
            operators_stack.append('fb_array')
        else:
            print_error(f'Array {array_ID} is not defined.', 'EC-19')
        

    # Crea un cuádruplo que suma el valor del arreglo a acceder y la dirección del arreglo
    # Esto se guarda en una dirección de tipo pointer, y esta se guarda en la pila de operandos.
    @_(' ')
    def np_get_array_address(self, p):
        global operands_stack, types_stack, constants_table
        array_position_to_access = operands_stack.pop()
        types_stack.pop()
        initial_array_address = create_constant_int_address(operands_stack.pop())
        pointer_address = create_pointer_address()
        set_quad('+', array_position_to_access, initial_array_address, pointer_address)
        # Pop al fondo falso
        operators_stack.pop()
        operands_stack.append(pointer_address)

    # Se genera el cuádruplo VERIFY que se usará para verificar que el valor a acceder se encuentra
    # dentro de los límites del arreglo. La verificación se hace en ejecución
    @_(' ')
    def np_verify_value_in_array_limits(self, p):
        global operands_stack, constants_table, types_stack
        accessing_array_type = types_stack[-1]
        array_ID = p[-5]
        value_to_access = operands_stack[-1]
        lower_limit = constants_table[0]
        upper_limit = constants_table[get_variable_directory(array_ID)['array_size']]

        if accessing_array_type == 'int':
            set_quad('VERIFY', value_to_access, lower_limit, upper_limit)
        else:
            print_error(f'Array {array_ID} must be accesed using an int value', 'EC-20')

    # Verifica que ambas variables sean arreglos de tipo enteo o flotante, y que la propiedad array_size sea igual para ambas
    @_(' ')
    def np_verify_same_length(self, p):
        x_array_var = get_variable_directory(p[-4])
        y_array_var = get_variable_directory(p[-2])

        if x_array_var['is_array'] and y_array_var['is_array']:
            if (x_array_var['type'] in ['int', 'float']) and (y_array_var['type'] in ['int', 'float']):
                if x_array_var['array_size'] != y_array_var['array_size']:
                    print_error(f'Arrays{p[-4]} and {p[-2]} must be of equal length', 'EC-17')
            else:
                print_error('This function requires 2 arrays of type int or float', 'EC-18')
        else:
            print_error('This function requires 2 arrays of type int or float', 'EC-18')


    ##### Statistical Functions #####

    # Genera un cuádruplo RAND con los límites de la función y genera una memoria temporal para guardar el resultado.
    @_(' ')
    def np_set_rand_quad(self, p):
        result_address = create_temp_address('int')
        lower_limit = p[-4]
        upper_limit = p[-2]
        operands_stack.append(result_address)
        types_stack.append('int')
        set_quad('RAND', lower_limit, upper_limit, result_address)

    # Llama a la función create_quad_statistics con el ID del arreglo y el tipo de función estadística.
    # Dicha función verifica que la variable sea un arreglo de tipo entero o flotante
    # Guarda el resultado en la pila de operandos como flotante
    @_(' ')
    def np_set_statistics_quad(self, p):
        array_ID = p[-2]
        quad_type = p[-4]
        match quad_type:
            case 'mean':
                create_quad_statistics(array_ID, 'MEAN')
            case 'median':
                create_quad_statistics(array_ID, 'MEDIAN')
            case 'variance':
                create_quad_statistics(array_ID, 'VARIANCE')
            case 'std':
                create_quad_statistics(array_ID, 'STD')
            case 'sum':
                create_quad_statistics(array_ID, 'SUM')
            case 'count':
                create_quad_statistics(array_ID, 'COUNT')
            case 'iqr':
                create_quad_statistics(array_ID, 'IQR')

    # Genera un cuádruplo con el tipo de función, las direcciones de los arreglos, y su tamaño.
    # No guarda el resultado en ningún lado, ya que estas funciones únicamente imprimen
    @_(' ')
    def np_set_stat_print_quad(self, p):
        quad_type = p[-6]
        array_1 = get_variable_directory(p[-4])
        array_2 = get_variable_directory(p[-2])
        match quad_type:
            case 'union':
                set_quad('UNION', array_1['address'], array_2['address'], array_1['array_size'])
            case 'diff':
                set_quad('DIFF', array_1['address'], array_2['address'], array_1['array_size'])
            case 'intersect':
                set_quad('INTERSECT', array_1['address'], array_2['address'], array_1['array_size'])
            case 'regression':
                set_quad('REGRESSION', array_1['address'], array_2['address'], array_1['array_size'])
            case 'corr':
                set_quad('CORR', array_1['address'], array_2['address'], array_1['array_size'])

    # Genera un cuádruplo de tipo CORR, con las direcciones de los arreglos, y su tamaño.
    # No guarda el resultado en ningún lado, porque esta función únicamente imprime
    @_(' ')
    def np_set_corr_quad(self, p):
        array_1 = get_variable_directory(p[-5])
        array_2 = get_variable_directory(p[-3])
        set_quad('CORR', array_1['address'], array_2['address'], array_1['array_size'])
    
    # Genera un cuádruplo con el tipo de gráfico, la direccion del arreglo, y su tamaño.
    @_(' ')
    def np_set_one_array_plot(self, p):
        quad_type = p[-4]
        array = get_variable_directory(p[-2])
        match quad_type:
            case 'histplot':
                set_quad('HISTPLOT', array['address'], -1, array['array_size'])
            case 'boxplot':
                set_quad('BOXPLOT', array['address'], -1, array['array_size'])

    # Genera un cuádruplo con el tipo de gráfico, las direcciones de los arreglos, y su tamaño.
    @_(' ')
    def np_set_two_array_plot(self, p):
        quad_type = p[-7]
        x_array_var = get_variable_directory(p[-5])
        y_array_var = get_variable_directory(p[-3])
        match quad_type:
            case 'scatterplot':
                set_quad('SCATTERPLOT', x_array_var['address'], y_array_var['address'], x_array_var['array_size'])
            case 'lineplot':
                set_quad('LINEPLOT', x_array_var['address'], y_array_var['address'], x_array_var['array_size'])
            case 'barplot':
                set_quad('BARPLOT', x_array_var['address'], y_array_var['address'], x_array_var['array_size'])

    # Error
    def error(self, token):
        print(f"Syntax Error: {token.value!r}", token)
        if token is not None:
            self.index = token.index + 1
        else:
            self.eof = True
        sys.exit()



##### Global Variables #####

scopes = ScopesDirectory()
current_scope = ''

variables_stack = deque()
operators_stack = deque()
operands_stack = deque()
types_stack = deque()
jumps_stack = deque()
quadruples = [];

parameters_count = 0
parameters_stack = deque()
function_call_ID_stack = deque()
current_function_call_ID = None

constants_table = {}
memory = Memory()
temps_count = 0

is_array = False
array_size = 0


##### Scopes Functions #####

def get_variable_directory(variable_ID):
    global scopes, current_scope
    directory_var = scopes.get_variables_table(current_scope).get_one(variable_ID)
    if (directory_var == None):
        directory_var = scopes.get_variables_table('program').get_one(variable_ID)
        if (directory_var == None):
            print_error(f'Variable {variable_ID} not found in current or global scope', 'EC-06')
    return directory_var

def create_scope(scope_id, return_type):
    global scopes, current_scope
    scopes.add_new_scope(scope_id, return_type, Variables(scope_id))
    current_scope = scope_id

def create_quad(operators_to_check):
    global operands_stack, operators_stack, types_stack, scopes, current_scope, temps_count
    if len(operators_stack) > 0 and operators_stack[-1] in operators_to_check:
        operator = operators_stack.pop()
        right_oper = operands_stack.pop()
        right_type = types_stack.pop()
        left_oper = operands_stack.pop()
        left_type = types_stack.pop()
        res_type = get_type(operator, right_type, left_type)

        if res_type != 'Error':
            current_scope_variables = scopes.get_variables_table(current_scope)
            temp_variable_name = "_temp" + f"{temps_count}"
            temps_count += 1
            current_scope_variables.add_variable(temp_variable_name, res_type)
            new_address = get_new_address(res_type, True)
            current_scope_variables.set_variable_address(temp_variable_name, new_address)
            set_quad(operator, left_oper, right_oper, new_address)
            operands_stack.append(new_address)
            types_stack.append(res_type)
        else:
            print_error(f'Cannot perform operation {operator} to {left_type} and {right_type}', 'EC-01')

def create_quad_statistics(array_ID, stat_operator):
    current_variable = get_variable_directory(array_ID)
    if (current_variable['is_array']) and (current_variable['type'] in ['int', 'float']):    
        result_address = create_temp_address('float')
        operands_stack.append(result_address)
        types_stack.append('float')
        set_quad(stat_operator, current_variable['array_size'], current_variable['address'], result_address)
    else:
        print_error(f'{stat_operator} function requires an array of floats or integers.', 'EC-07')


def set_quad(oper_ID, left_oper, right_oper, result):
    quadruples.append(Quadruple(operator_IDs[oper_ID] , left_oper, right_oper, result))


##### Memory Functions #####

def get_global_types_map(memory):
    global_types_map = {
        'int': memory.counters['global']['int'],
        'float': memory.counters['global']['float'],
        'char': memory.counters['global']['char'],
        'bool': memory.counters['global']['bool'],
    }
    return global_types_map

def get_local_types_map(memory):
    local_types_map = {
        'int': memory.counters['local']['int'],
        'float': memory.counters['local']['float'],
        'char': memory.counters['local']['char'],
        'bool': memory.counters['local']['bool'],
    }
    return local_types_map

def get_temporal_types_map(memory):
    local_types_map = {
        'int': memory.counters['temp']['int'],
        'float': memory.counters['temp']['float'],
        'char': memory.counters['temp']['char'],
        'bool': memory.counters['temp']['bool'],
    }
    return local_types_map

def create_constant_int_address(value):
    global memory, constants_table
    if value in constants_table:
        return constants_table[value]
    else:
        new_mem_address = memory.counters['const']['int']
        constants_table[value] = new_mem_address
        memory.set_count('const', 'int')
        return new_mem_address

def create_pointer_address():
    global memory
    new_pointer_address = memory.counters['pointer']['int']
    memory.set_count('pointer', 'int')
    return new_pointer_address

def create_temp_address(variable_type):
    global scopes, temps_count, current_scope
    current_scope_variables = scopes.get_variables_table(current_scope)
    temp_variable_name = f"_temp{temps_count}"
    temps_count += 1
    current_scope_variables.add_variable(temp_variable_name, 'float')
    new_address = get_new_address(variable_type, True)
    current_scope_variables.set_variable_address(temp_variable_name, new_address)
    return new_address
    
def get_new_address(variable_type, is_temp = False, space = 1, other_scope = None):
    global current_scope, memory
    if other_scope is not None:
        scope = other_scope
    else:
        scope = current_scope
    if is_temp:
        temporal_types_map = get_temporal_types_map(memory)
        memory.set_count('temp', variable_type, space)
        return temporal_types_map[variable_type]
    if scope == 'program':
        global_types_map = get_global_types_map(memory)
        memory.set_count('global', variable_type, space)
        return global_types_map[variable_type]
    local_types_map = get_local_types_map(memory)
    memory.set_count('local', variable_type, space)
    return local_types_map[variable_type]
