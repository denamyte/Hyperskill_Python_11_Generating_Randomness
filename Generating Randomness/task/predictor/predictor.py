import itertools as it
from typing import List, Tuple, Dict


class Predictor:
    DATA_FILTER = ['0', '1']
    TRIADS: List[str] = [f'{i:03b}' for i in range(8)]

    def __init__(self, data_min_size: int = 100):
        self.data_min_size = data_min_size
        self._data = ''
        self._data_len = 0
        self._followers: List[Tuple[int, int]] = []

    def collect_data(self):
        while len(self._data) < self.data_min_size:
            self.input_data_portion()
            self.print_intermediate_collect_result()
        self._data_len = len(self._data)
        self.print_final_collect_result()

    def input_data_portion(self):
        raw_str = input('Print a random string containing 0 or 1:\n\n')
        self._data += ''.join(x for x in raw_str if x in self.DATA_FILTER)

    def print_intermediate_collect_result(self):
        length = len(self._data)
        if length < self.data_min_size:
            print(f'Current data length is {length}, {self.data_min_size - length} symbols left')

    def print_final_collect_result(self):
        print(f'''
Final data string:
{self._data}''')

    def analyze_triads(self):
        pass
        # todo: iterate through TRIADS and analyze_str_occurrences
        #  fill the self._followers

    def analyze_str_occurrences(self, pattern: str) -> Tuple[int, int]:
        start = 0
        occurrences = [0, 0]  # an array of size 2, the occurrences of 0 and 1
        length = len(pattern)
        found_i = self._data.find(pattern, start, self._data_len - 1)
        while found_i > -1:
            occurrences[int(self._data[found_i + length])] += 1
            start = found_i + 1
            found_i = self._data.find(pattern, start, self._data_len - 1)
        return occurrences[0], occurrences[1]

    def test(self):
        pass


p = Predictor()
# p.test()
p.collect_data()
# p.analyze_str_occurrences('000')
