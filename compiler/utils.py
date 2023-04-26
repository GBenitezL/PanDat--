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

def print_error(message, id=''):
    print(f'Error ID:{id}\n', f'Description: {message}', '\n')
    sys.exit()