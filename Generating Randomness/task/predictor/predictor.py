class Predictor:
    DATA_FILTER = '01'

    def __init__(self, data_min_size: int = 100):
        self.data_min_size = data_min_size
        self._data = ''

    def collect_data(self):
        while len(self._data) < self.data_min_size:
            self.input_data_portion()
            self.print_intermediate_result()
        self.print_final_result()

    def input_data_portion(self):
        raw_str = input('Print a random string containing 0 or 1:\n\n')
        self._data += ''.join(x for x in raw_str if x in self.DATA_FILTER)

    def print_intermediate_result(self):
        length = len(self._data)
        if length < self.data_min_size:
            print(f'Current data length is {length}, {self.data_min_size - length} symbols left')

    def print_final_result(self):
        print(f'''
Final data string:
{self._data}''')


p = Predictor()
p.collect_data()
