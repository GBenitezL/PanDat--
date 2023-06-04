from compiler.utils import print_error

cube = {
    '=': {
        'int': {'int': True, 'float': True},
        'float': {'float': True},
        'char': {'char': True},
        'bool': {'bool': True}
    },
    '/': {
        'int': {'int': 'float'},
        'float': {'float': 'float', 'int': 'float'}
    },
    '&&': {
        'bool': {'bool': 'bool'}
    },
    '||': {
        'bool': {'bool': 'bool'}
    }
}

arithmetic_symbols = ['+', '-', '*']
comparison_symbols = ['<', '<=', '>', '>=', '==', '!=']

for symbol in arithmetic_symbols:
    cube[symbol] = {
        'int': {'int': 'int', 'float': 'float'},
        'float': {'float': 'float', 'int': 'float'}
    }

for symbol in comparison_symbols:
    cube[symbol] = {
        'int': {'int': 'bool', 'float': 'bool'},
        'float': {'float': 'bool', 'int': 'bool'},
        'char': {'char': 'bool'},
        'bool': {'bool': 'bool'}
    }

# Function to get the type of the operation result
def get_type(operand, type1, type2):
    result_type = cube.get(operand, {}).get(type1, {}).get(type2)

    if result_type is None:
        return 'Error'
    else:
        return result_type
