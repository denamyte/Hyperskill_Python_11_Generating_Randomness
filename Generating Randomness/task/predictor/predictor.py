import random
from typing import List, Tuple


class Predictor:
    DATA_FILTER = ['0', '1']
    PATTERNS: List[str] = [f'{i:03b}' for i in range(8)]
    PTN_LEN = 3

    def __init__(self, data_min_size: int = 100):
        self._data_min_size = data_min_size
        self._data = ''
        self._data_len = 0
        self._follow_counts: List[Tuple[int, int]] = []
        self._data2 = ''
        self._predicted_str = ''
        self._guessed_number = 0

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
            occurrences[int(self._data[found_i + self.PTN_LEN])] += 1
            start = found_i + 1
            found_i = self._data.find(pattern, start, self._data_len - 1)
        return occurrences[0], occurrences[1]

    def input_second_string(self):
        self._data2 = input('\n\nPlease enter a test string containing 0 or 1:\n\n')

    def predict_result(self):
        d2_len = len(self._data2)
        predicted: List[str] = [self.rnd_01() for _ in range(min(self.PTN_LEN, d2_len))]
        for i in range(d2_len - self.PTN_LEN):
            predicted.append(self.predict_follower(self._data2[i:i + self.PTN_LEN]))
        self._predicted_str = ''.join(predicted)

    def predict_follower(self, pattern: str) -> str:
        counts = self._follow_counts[int(pattern, 2)]
        return '0' if counts[0] > counts[1] else '1' if counts[1] > counts[0] else self.rnd_01()

    def analyze_prediction_accuracy(self):
        self._guessed_number = \
            sum(a == b for a, b in zip(self._data2[self.PTN_LEN:], self._predicted_str[self.PTN_LEN:]))

    @staticmethod
    def rnd_01() -> str:
        return random.choice(Predictor.DATA_FILTER)

    def render_result(self):
        analyze_len = len(self._data2) - self.PTN_LEN
        percent = self._guessed_number / analyze_len * 100
        print(f'''\
prediction:
{self._predicted_str}

Computer guessed right {self._guessed_number} out of {analyze_len} symbols ({percent:0.2f} %)''')


def run():
    p = Predictor()
    p.collect_data()
    p.analyze_patterns()
    p.input_second_string()
    p.predict_result()
    p.analyze_prediction_accuracy()
    p.render_result()


run()
