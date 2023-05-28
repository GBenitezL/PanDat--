from compiler.utils import print_error, data_type_IDs

class Directory:
    def __init__(self):
        self.directory = {}

    def exists(self, id):
        return id in self.directory

    def get_one(self, id):
        return self.directory.get(id)

    def print_directory(self):
        print('\n'.join(f'{key}: {value}' for key, value in self.directory.items()))


class Variables(Directory):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope
    
    def add_variable(self, id, type):
        if id in self.directory:
            print_error(f"Variable '{id}' has already been declared in this scope", 'EC-04')
        if type == 'void' or type not in ['int', 'float', 'char', 'bool']:
            print_error(f"Variable '{id}' requires a return type {type}", 'EC-03')
        self.directory[id] = {'type': type, 'address': None}
    
    def set_variable_address(self, id, address):
        self.directory[id]['address'] = address
    
    def set_array_values(self, id, is_array=False, array_size=None):
        self.directory[id].update({'is_array': is_array, 'array_size': array_size})


class ScopesDirectory(Directory):
    def add_new_scope(self, id, return_type, variables_table):
        if self.exists(id):
            print_error(f'Scope {id} already exists in this scope', 'EC-02')
        if return_type not in ['int', 'float', 'char', 'bool', 'void']:
            print_error(f'{id} requires a return type {return_type}', 'EC-03')

        self.directory[id] = { 'variables_table': variables_table, 'return_type': return_type, 'parameters': [], 
            'params_IDs': [],  'count': None }

    def get_variables_table(self, id):
        return self.directory[id]['variables_table']

    def get_parameters(self, id):
        return self.directory[id]['parameters']
    
    def get_parameter_IDs(self, id):
        return self.directory[id]['params_IDs']

    def get_return_type(self, id):
        return self.directory[id]['return_type']

    def set_quad_count(self, id, count):
        self.directory[id]['count'] = count

    def get_quad_count(self, id):
        return self.directory[id]['count']
    
    def set_size(self, id):
        variables_table = self.directory[id]['variables_table'].directory
        types_counter = [0] * 4
        total_size = sum(
            value['array_size'] if ('is_array' in value.keys() and value['is_array']) else 1 
            for key, value in variables_table.items()
        )
        for key, value in variables_table.items():
            types_counter[data_type_IDs[value['type']] - 1] += value['array_size'] if ('is_array' in value.keys() and value['is_array']) else 1
        self.directory[id].update({'types_counter': types_counter, 'total_variables': total_size})

    def get_size(self, id):
        return self.directory[id]['total_variables']

    def print_directory(self):
        for scope, scope_value in self.directory.items():
            print(f'Scope {scope}:')
            for key, value in scope_value.items():
                print(f'Variables table for {scope}') if key == 'variables_table' else print(f'{key}: {value}')
                if key == 'variables_table': value.print_directory()
            print()
