from utils import print_error

def get_type(symbol, type1, type2):
    basic_symbols = ['+', '-', '*']
    comparison_symbols = ['<', '<=', '>', '>=', '==', '!=']
    
    cube = {
        '=': {
            'int': {'int': True},
            'float': {'float': True},
            'char': {'char': True},
            'bool': {'bool': True}
        },
        '/': {
            'int': {'int': 'float'},
            'float': {'float': 'float', 'int': 'float'},
            'char': {'char': 'float', 'int': 'float'},
        }
    }
    
    for s in basic_symbols:
        cube[s] = {
            'int': {'int': 'int', 'float': 'float'},
            'float': {'float': 'float', 'int': 'float'},
            'char': {'char': 'int', 'int': 'int', 'float': 'float'}
        }
        
    for s in comparison_symbols:
        cube[s] = {
            'int': {'int': 'bool'},
            'char': {'char': 'bool'},
            'bool': {'bool': 'bool'}
        }
    
    result_type = cube.get(symbol, {}).get(type1, {}).get(type2)
    
    if result_type is None:
        print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', "EC-01")
    else:
        return result_type