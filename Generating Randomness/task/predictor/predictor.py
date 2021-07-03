from typing import List, Tuple


class Predictor:
    DATA_FILTER = ['0', '1']
    PATTERNS: List[str] = [f'{i:03b}' for i in range(8)]
    PATTERN_LENGTH = 3

    def __init__(self, data_min_size: int = 100):
        self._data_min_size = data_min_size
        self._data = ''
        self._data_len = 0
        self._follow_counts: List[Tuple[int, int]] = []

    def collect_data(self):
        while len(self._data) < self._data_min_size:
            self.input_data_portion()
            self.print_intermediate_collected_result()
        self._data_len = len(self._data)
        self.print_final_collected_result()

    def input_data_portion(self):
        raw_str = input('Print a random string containing 0 or 1:\n\n')
        self._data += ''.join(x for x in raw_str if x in self.DATA_FILTER)

    def print_intermediate_collected_result(self):
        length = len(self._data)
        if length < self._data_min_size:
            print(f'Current data length is {length}, {self._data_min_size - length} symbols left')

    def print_final_collected_result(self):
        print(f'''
Final data string:
{self._data}''')

    def analyze_patterns(self):
        self._follow_counts = [self.analyze_pattern_with_followers(p) for p in self.PATTERNS]

    def analyze_pattern_with_followers(self, pattern: str) -> Tuple[int, int]:
        start = 0
        occurrences = [0, 0]  # an array of size 2, the occurrences of 0 and 1 after the pattern
        found_i = self._data.find(pattern, start, self._data_len - 1)
        while found_i > -1:
            occurrences[int(self._data[found_i + self.PATTERN_LENGTH])] += 1
            start = found_i + 1
            found_i = self._data.find(pattern, start, self._data_len - 1)
        return occurrences[0], occurrences[1]

    def render_patterns_occurrences(self):
        print()
        for pattern, res in zip(self.PATTERNS, self._follow_counts):
            print(f'{pattern}: {res[0]},{res[1]}')


def run():
    p = Predictor()
    p.collect_data()
    p.analyze_patterns()
    p.render_patterns_occurrences()


run()
