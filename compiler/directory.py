from compiler.utils import print_error, data_type_IDs

class Directory:
    def __init__(self):
        self.directory = {}

    def exists(self, id):
        return id in self.directory

    def get_one(self, id):
        return self.directory.get(id)

    def print_directory(self):
        for key, value in self.directory.items():
            print(f'{key}: {value}')


class Variables(Directory):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope
    
    def add_var(self, id, type):
        if id in self.directory:
            print_error(f"Variable '{id}' has already been declared in this scope", 'EC-04')
        if type == 'void' or type not in ['int', 'float', 'char', 'bool']:
            print_error(f"Variable '{id}' requires a return type {type}", 'EC-03')
        self.directory[id] = {'type': type, 'address': None}
    
    def set_var_address(self, id, address):
        self.directory[id]['address'] = address
    
    def set_array_values(self, id, is_array = False, arr_size = None):
        self.directory[id]['is_array'] = is_array
        self.directory[id]['arr_size'] = arr_size


class ScopesDirectory(Directory):
    def add_new_scope(self, id, return_type, vars_table):
        if self.exists(id):
            print_error(f'Scope {id} already exists in this scope', 'EC-02')
        if return_type not in ['int', 'float', 'char', 'bool', 'void']:
            print_error(f'{id} requires a return type {return_type}', 'EC-03')
        parameters = []
        params_IDs = []
        self.directory[id] = { 'vars_table': vars_table, 'return_type': return_type, 'parameters': parameters, 
            'params_IDs': params_IDs,  'count': None }

    def get_variables_table(self, id):
        return self.directory[id]['vars_table']

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
        vars_table = self.directory[id]['vars_table'].directory
        types_counter = [0] * 4
        total_size = 0
        for key, value in vars_table.items():
            var_type = value['type']
            item_size = value['arr_size'] if ('is_array' in value.keys() and value['is_array']) else 1
            data_type = data_type_IDs[var_type] - 1
            types_counter[data_type] += item_size
            total_size += item_size

        self.directory[id]['types_counter'] = types_counter
        self.directory[id]['total_vars'] = total_size
        
    def get_size(self, id):
        return self.directory[id]['total_vars']

    def print_directory(self):
        for scope, scope_value in self.directory.items():
            print(f'Scope {scope}:')
            for key, value in scope_value.items():
                if key == 'vars_table':
                    print(f'Variables table for {scope}')
                    value.print_directory()
                else:
                    print(f'{key}: {value}')
            print()
