import sys

data_type_IDs = {
    'int': 1, 
    'float': 2, 
    'char': 3, 
    'bool': 4, 
}

data_type_values = {
    1: 'int',
    2: 'float',
    3: 'char',
    4: 'bool',
}

operator_IDs = {
    '+': 1,
    '-': 2,
    '/': 3,
    '*': 4,
    '<': 5,
    '<=': 6,
    '>': 7,
    '>=': 8,
    '==': 9,
    '!=': 10,
    '&&': 11,
    '||': 12,
    '=': 13,
    'RETURN': 14,
    'READ': 15,
    'PRINT': 16, 
    'PRINT_MULTIPLE': 17,
    
    'GOTO': 20,
    'GOTOV': 21,
    'GOTOF': 22,
    'GOSUB': 23,
    'ERA': 24,
    'VERIFY': 25,
    'PARAM': 26,
    'ENDFUNC': 27,
    'END': 28,

    'MEAN': 30,
    'MEDIAN': 31,
    'VARIANCE': 32,
    'STD': 33,
    'RAND': 34,
    'PLOT': 35,
    'CORR': 36,
    'REGRESSION': 37
}


def print_error(message, id=''):
    print(f'Error ID:{id}\n', f'Description: {message}', '\n')
    sys.exit()