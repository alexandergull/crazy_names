# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import time

class Word:
    def __init__(self, word=''):
        self.word = word
        self.twins_list = []
        self.trines_list = []
        self.trines_amount = 0
        self.twins_amount = 0
        self.lexems_amount = 0
        self.twins_detected_dict = {}
        self.trines_detected_dict = {}

    def calculate_lexems(self, lang_twins_dict, lang_trines_dict):

        for twin in self.twins_list:
            if twin in lang_twins_dict.keys():
                self.twins_amount += lang_twins_dict[twin]
                self.twins_detected_dict[twin] = lang_twins_dict[twin]

        for trine in self.trines_list:
            if trine in lang_trines_dict.keys():
                self.trines_amount += lang_trines_dict[trine]
                self.twins_detected_dict[trine] = lang_trines_dict[trine]

    def collect_lexems(self, strafe):
        twins_iterator = 1
        trines_iterator = 1
        current_twin = ''
        current_trine = ''
        for char in self.word[strafe:len(self.word)]:

            if trines_iterator < 3:
                current_trine += char
                trines_iterator += 1
            else:
                current_trine += char
                self.trines_list.append(current_trine)
                trines_iterator = 2
                current_trine = char

            if strafe < 2:
                if twins_iterator < 2:
                    current_twin += char
                    twins_iterator += 1
                else:
                    current_twin += char
                    self.twins_list.append(current_twin)
                    current_twin = char
                    twins_iterator = 2

    def check_word(self, lang_twins_dict, lang_trines_dict, twin_multiplier, trine_multiplier):

        if self.word:

            self.collect_lexems(0)
            self.collect_lexems(1)
            self.collect_lexems(2)

            self.calculate_lexems(lang_twins_dict, lang_trines_dict)

            x = len(self.word)

            power = -0.1 * x

            word_length_multiplier = 12 * pow(x, power)

            self.lexems_amount = word_length_multiplier * ((self.twins_amount * twin_multiplier) + (
                        self.trines_amount * trine_multiplier))


class CrazyName:

    def __init__(self, dict_filepath, sensitivity=1000, trine_multiplier=50, twin_multiplier=1):
        self.dict_filepath = dict_filepath
        self.dictionary_words_list = []
        self.twins_list = []
        self.trines_list = []
        self.twins_dict = {}
        self.trines_dict = {}
        self.sensitivity = sensitivity
        self.trine_multiplier = trine_multiplier
        self.twin_multiplier = twin_multiplier
        self.word_input_list = []

    def filter_input_words_dict(self):
        buffer_list = []
        for word in self.word_input_list:
            if not word.word.isascii():
                if not word.word.isalnum():
                    if not word.word.isspace()]


            if any(checklist):
                buffer_list.append(word)
        self.word_input_list = buffer_list

    def init_dictionary_file(self):
        file = open(self.dict_filepath, 'r')

        clear_list = []
        while True:
            line = file.readline()
            clear_list.append(line)
            if not line:
                break
        file.close()

        for dict_word in clear_list:
            checklist = [not dict_word.isascii(), not dict_word.isalnum()]
            if any(checklist):
                result = dict_word.replace('\n', '')
                if result != '':
                    self.dictionary_words_list.append(result)

        print(f'WORDS COUNT IN LANGUAGE:{len(self.dictionary_words_list)}')

    def collect_dictionary_lexems(self, strafe):
        for word in self.dictionary_words_list:
            twins_iterator = 1
            trines_iterator = 1
            current_twin = ''
            current_trine = ''
            for char in word[strafe:len(word)]:

                if trines_iterator < 3:
                    # print('trines_iterator ', trines_iterator)
                    current_trine += char
                    trines_iterator += 1
                    # print('CURENT TRINE <3: ' + current_trine)
                else:
                    # print('trines_iterator ', trines_iterator)
                    current_trine += char
                    # print('CURENT TRINE ELSE: ' + current_trine)
                    self.trines_list.append(current_trine)
                    current_trine = char
                    trines_iterator = 2

                if strafe < 2:
                    if twins_iterator < 2:
                        current_twin += char
                        twins_iterator += 1
                    else:
                        current_twin += char
                        self.twins_list.append(current_twin)
                        current_twin = char
                        twins_iterator = 2

                # print(f'TRINES LIST {self.trines_list}')

    def normalize_dicts(self, normal):
        for twin in self.twins_dict:
            if self.twins_dict[twin] > normal:
                self.twins_dict[twin] = self.twins_dict[twin] // 3

    def calculate_dicts_in_dictionary(self):
        for twin in self.twins_list:
            if twin not in self.twins_dict:
                self.twins_dict[twin] = self.twins_list.count(twin)
        # print(self.twins_dict)

        for trine in self.trines_list:
            if trine not in self.trines_dict:
                self.trines_dict[trine] = self.trines_list.count(trine)
        # print(self.trines_dict)

    def init_data(self):

        self.init_dictionary_file()

        self.collect_dictionary_lexems(0)
        self.collect_dictionary_lexems(1)
        self.collect_dictionary_lexems(2)

        self.calculate_dicts_in_dictionary()

        self.normalize_dicts(100)

    def check_word_list_from_file(self, filepath):
        file = open(filepath, 'r', encoding='UTF-8')
        word_list = []
        while True:
            line = file.readline()
            self.word_input_list.append(Word(line))
            if not line:
                break
        file.close()

        self.filter_input_words_dict()

        print(f'WORDS COUNT IN FILE:{len(self.word_input_list)}')

        for word in self.word_input_list:
            word.check_word(self.twins_dict, self.trines_dict, self.twin_multiplier, self.trine_multiplier)

    def report_words_stat(self, show_odds_only=1, amount_gain_to_show=100):
        odd_words_total = 0
        good_words_total = 0

        for word in self.word_input_list:

            if word.lexems_amount < self.sensitivity:
                odd_words_total += 1
            else:
                good_words_total += 1

            if word.lexems_amount > self.sensitivity:
                if show_odds_only != 1:
                    print(f'WORD: {word.word}')
                    print(f'TWINS: {word.twins_list}: TTL {word.twins_amount}')
                    print(f'DETECTED TWINS DICT: {word.twins_detected_dict}')
                    print(f'TRINES: {word.trines_list}: TTL {word.trines_amount}')
                    print(f'DETECTED TRINES DICT: {word.trines_detected_dict}')
                    print(f'AMOUNT: {word.lexems_amount}')
                    print('WORD IS FINE\n')
            else:
                if word.lexems_amount > amount_gain_to_show:
                    print(f'WORD: {word.word}')
                    print(f'TWINS: {word.twins_list}: TTL {word.twins_amount}')
                    print(f'DETECTED TWINS DICT: {word.twins_detected_dict}')
                    print(f'TRINES: {word.trines_list}: TTL {word.trines_amount}')
                    print(f'DETECTED TRINES DICT: {word.trines_detected_dict}')
                    print(f'AMOUNT: {word.lexems_amount}')
                    print('WORD IS ODD\n')

        words_total = good_words_total + odd_words_total
        percentage = odd_words_total / (words_total / 100)
        print(f'PERCENTAGE OF ODD WORDS {percentage}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    crazy = CrazyName(dict_filepath='utf.txt', sensitivity=200, trine_multiplier=20, twin_multiplier=2)
    crazy.init_data()
    crazy.check_word_list_from_file('ct_usernames.txt')
    crazy.report_words_stat(show_odds_only=1, amount_gain_to_show=25)
    print(f'EXEC TIME: {time.time()-start_time}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
