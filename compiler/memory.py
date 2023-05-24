class Memory:
    def __init__(self):
        self.counters = {
            'global': {'int': 11000, 'float': 12000, 'char': 13000, 'bool': 14000},
            'local': {'int': 21000, 'float': 22000, 'char': 23000, 'bool': 24000},
            'temp': {'int': 31000, 'float': 32000, 'char': 33000, 'bool': 34000},
            'const': {'int': 41000, 'float': 42000, 'char': 43000, 'bool': 44000},
            'pointer': {'int': 50000}
        }

    def reset_local_counters(self):
        self.counters['local'] = {'int': 21000, 'float': 22000, 'char': 23000, 'bool': 24000}

    def reset_temp_counters(self):
        self.counters['temp'] = {'int': 31000, 'float': 32000, 'char': 33000, 'bool': 34000}

    def set_count(self, counter_type, type, space=1):
        if counter_type in self.counters and type in self.counters[counter_type]:
            self.counters[counter_type][type] += space