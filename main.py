# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re


class CrazyName:

    def __init__(self, sensitivity=1000):
        self.dict_filepath = 'utf'
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

    def init_dictionary_file(self):
        file = open('utf.txt', 'r')

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

                if trines_iterator <= 3:
                    current_trine += char
                    trines_iterator += 1
                else:
                    trines_iterator = 2
                    self.trines_list.append(current_trine)
                    current_trine = char

                if strafe < 2:
                    if twins_iterator <= 2:
                        current_twin += char
                        twins_iterator += 1
                    else:
                        twins_iterator = 2
                        self.twins_list.append(current_twin)
                        current_twin = char

    def collect_word_lexems(self, word, strafe):
        twins_iterator = 1
        trines_iterator = 1
        current_twin = ''
        current_trine = ''
        for char in word[strafe:len(word)]:

            if trines_iterator <= 3:
                current_trine += char
                trines_iterator += 1
            else:
                trines_iterator = 2
                self.word_trines_list.append(current_trine)
                current_trine = char
            if strafe < 2:
                if twins_iterator <= 2:
                    current_twin += char
                    twins_iterator += 1
                else:
                    twins_iterator = 2
                    self.word_twins_list.append(current_twin)
                    current_twin = char

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

    def check_word(self, word):

        self.word_twins_list = []
        self.word_trines_list = []

        self.collect_word_lexems(word, 0)
        self.collect_word_lexems(word, 1)
        self.collect_word_lexems(word, 2)

        print(self.word_twins_list)
        print(self.word_trines_list)

        self.calculate_lexems_found_in_word()

        print(self.word_twins_amount)
        print(self.word_trines_amount)

        total_amount = self.word_twins_amount + (self.word_trines_amount * 10)

        print(total_amount)

        if total_amount >= self.sensitivity:
            print('WORD IS OK')
        else:
            print('WORD IS ODD')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c_name = CrazyName(sensitivity=500)
    c_name.init_data()
    c_name.check_word('nxknsbgtdjhyd')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
