# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re


class Word:
    def __init__(self, word='', twins_list=None, trines_list=None, lexems_amount=0):
        self.word = word
        self.twins_list = twins_list
        self.trines_list = trines_list
        self.lexems_amount = lexems_amount


class CrazyName:

    def __init__(self, dict_filepath, sensitivity=1000, trine_multiplicator=50, twin_multiplicator=1):
        self.dict_filepath = dict_filepath
        self.dictionary_words_list = []
        self.twins_list = []
        self.trines_list = []
        self.twins_dict = {}
        self.trines_dict = {}
        self.word_twins_list = []
        self.word_trines_list = []
        self.word_twins_amount = 0
        self.word_trines_amount = 0
        self.sensitivity = sensitivity
        self.trine_multiplicator = trine_multiplicator
        self.twin_multiplicator = twin_multiplicator
        self.word_input_list = []

    def init_dictionary_file(self):
        file = open(self.dict_filepath, 'r')

        clear_list = []
        while True:
            line = file.readline()
            clear_list.append(line)
            if not line:
                break
        file.close()

        for word in clear_list:
            result = word.replace('\n', '')
            if result != '':
                self.dictionary_words_list.append(result)

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

    def collect_word_lexems(self, word, strafe):
        twins_iterator = 1
        trines_iterator = 1
        current_twin = ''
        current_trine = ''
        for char in word[strafe:len(word)]:

            if trines_iterator < 3:
                current_trine += char
                trines_iterator += 1
            else:
                current_trine += char
                self.word_trines_list.append(current_trine)
                trines_iterator = 2
                current_trine = char

            if strafe < 2:
                if twins_iterator < 2:
                    current_twin += char
                    twins_iterator += 1
                else:
                    current_twin += char
                    self.word_twins_list.append(current_twin)
                    current_twin = char
                    twins_iterator = 2

    def calculate_dicts_in_dictionary(self):
        for twin in self.twins_list:
            if twin not in self.twins_dict:
                self.twins_dict[twin] = self.twins_list.count(twin)
        # print(self.twins_dict)

        for trine in self.trines_list:
            if trine not in self.trines_dict:
                self.trines_dict[trine] = self.trines_list.count(trine)
        # print(self.trines_dict)

    def calculate_lexems_found_in_word(self):

        for twin in self.word_twins_list:
            if twin in self.twins_dict.keys():
                self.word_twins_amount += self.twins_dict[twin]

        for trine in self.word_trines_list:
            if trine in self.trines_dict.keys():
                self.word_trines_amount += self.trines_dict[trine]

    def init_data(self):

        self.init_dictionary_file()

        self.collect_dictionary_lexems(0)
        self.collect_dictionary_lexems(1)
        self.collect_dictionary_lexems(2)

        self.calculate_dicts_in_dictionary()

    def check_word_list_from_file(self, filepath):
        file = open(filepath, 'r')
        clear_list = []
        word_list = []
        while True:
            line = file.readline()
            word_list.append(line)
            if not line:
                break
        file.close()

        for word in word_list:
            result = word.replace('\n', '')
            if result != '': clear_list.append(result)

        print(f'WORDS COUNT:{len(clear_list)}')

        for word in clear_list:
            self.check_word(word)

    def check_word(self, word):

        if word:

            self.word_twins_list = []
            self.word_trines_list = []
            self.word_twins_amount = 0
            self.word_trines_amount = 0

            self.collect_word_lexems(word, 0)
            self.collect_word_lexems(word, 1)
            self.collect_word_lexems(word, 2)

            self.calculate_lexems_found_in_word()

            word_length_multiplier = len(word) * pow(len(word),-1)

            if len(word) == 1:
                word_length_multiplier = 100
            elif len(word) == 2:
                word_length_multiplier = 60
            elif len(word) == 3:
                word_length_multiplier = 50
            elif len(word) == 4:
                word_length_multiplier = 3
            elif len(word) == 5:
                word_length_multiplier = 2


            print(self.word_twins_amount, self.word_trines_amount)

            total_amount = (self.word_twins_amount * self.twin_multiplicator * word_length_multiplier) + \
                           (self.word_trines_amount * self.trine_multiplicator * word_length_multiplier)

            self.word_input_list.append(
                Word(word, self.word_twins_list, self.word_trines_list, lexems_amount=total_amount))

    def report_words_stat(self):
        odd_words_total = 0
        good_words_total = 0

        for word in self.word_input_list:
            if word.lexems_amount < self.sensitivity:
                print(f'WORD: {word.word}')
                print(f'WORD TWINS: {word.twins_list}')
                print(f'WORD TRINES: {word.trines_list}')
                print(f'WORD AMOUNT: {word.lexems_amount}')
                print('WORD IS ODD')
            if word.lexems_amount >= self.sensitivity:
                good_words_total += 1
            else:
                odd_words_total += 1
        words_total = good_words_total + odd_words_total
        percentage = odd_words_total / (words_total / 100)
        print(f'PERCENTAGE OF ODD WORDS {percentage}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c_name = CrazyName(dict_filepath='utf2.txt', sensitivity=1000, trine_multiplicator=33, twin_multiplicator=1)
    c_name.init_data()
    c_name.check_word_list_from_file('utf2.txt')
    c_name.report_words_stat()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
