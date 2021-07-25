import random
from typing import List, Tuple


class Predictor:
    DATA_FILTER = ['0', '1']
    PTN_NUMBER = 8
    PTN_LEN = 3

    def __init__(self, data_min_size: int = 100):
        self._data_min_size = data_min_size
        self._data = ''
        self._follow_counts: List[Tuple[int, int]] = [(0, 0) for _ in range(self.PTN_NUMBER)]
        self._predicted_str = ''
        self._guessed_number = 0
        self._money = 1000

    def collect_data(self):
        print('Please give AI some data to learn...')
        self.print_intermediate_collected_result()
        while len(self._data) < self._data_min_size:
            self.input_data_portion()
            self.print_intermediate_collected_result()
        self.print_final_collected_result()

    def input_data_portion(self):
        raw_data = input('Print a random string containing 0 or 1:\n\n')
        self._data += self._preprocess_data(raw_data)

    @staticmethod
    def invite_to_print():
        print('\nPrint a random string containing 0 or 1:')

    @staticmethod
    def _preprocess_data(data: str) -> str:
        return ''.join(x for x in data if x in Predictor.DATA_FILTER)

    def print_intermediate_collected_result(self):
        length = len(self._data)
        if length < self._data_min_size:
            print(f'The current data length is {length}, {self._data_min_size - length} symbols left')

    def print_final_collected_result(self):
        print(f'''
Final data string:
{self._data}''')

    def update_follow_counts(self):
        results = self._analyze_data_string()
        self._follow_counts = [(fc[0] + res[0], fc[1] + res[1]) for fc, res in zip(self._follow_counts, results)]

    def _analyze_data_string(self) -> List[List[int]]:
        results = [[0, 0] for _ in range(self.PTN_NUMBER)]
        for i in range(self.PTN_LEN, len(self._data)):
            res_index = int(self._data[i - 3:i], 2)
            sym_index = int(self._data[i])
            results[res_index][sym_index] += 1
        return results

    @staticmethod
    def print_game_invitation():
        print('''
You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!''')

    def input_test_string(self):
        self._data = input()

    def is_enough(self):
        return self._data == 'enough'

    def preprocess_test_data(self):
        self._data = self._preprocess_data(self._data)

    def no_data(self):
        return len(self._data) == 0

    def predict_result(self):
        data_len = len(self._data)
        predicted: List[str] = [self.rnd_01() for _ in range(min(self.PTN_LEN, data_len))]
        for i in range(data_len - self.PTN_LEN):
            predicted.append(self.predict_follower(self._data[i:i + self.PTN_LEN]))
        self._predicted_str = ''.join(predicted)

    def predict_follower(self, pattern: str) -> str:
        counts = self._follow_counts[int(pattern, 2)]
        return '0' if counts[0] > counts[1] else '1' if counts[1] > counts[0] else self.rnd_01()

    def analyze_prediction(self):
        analyze_len = len(self._data) - self.PTN_LEN
        self._guessed_number = \
            sum(a == b for a, b in zip(self._data[self.PTN_LEN:], self._predicted_str[self.PTN_LEN:]))
        self._money += analyze_len - 2 * self._guessed_number

    @staticmethod
    def rnd_01() -> str:
        return random.choice(Predictor.DATA_FILTER)

    def render_result(self):
        analyze_len = len(self._data) - self.PTN_LEN
        percent = self._guessed_number / analyze_len * 100
        print(f'''\
prediction:
{self._predicted_str}

Computer guessed right {self._guessed_number} out of {analyze_len} symbols ({percent:0.2f} %)
Your capital is now ${self._money}''')

    @staticmethod
    def game_over():
        print('Game over!', end='')


def run():
    p = Predictor()
    p.collect_data()
    p.update_follow_counts()
    p.print_game_invitation()

    while 1:
        p.invite_to_print()
        p.input_test_string()
        if p.is_enough():
            break
        p.preprocess_test_data()
        if p.no_data():
            continue
        p.predict_result()
        p.analyze_prediction()
        p.render_result()
        p.update_follow_counts()

    p.game_over()


run()
