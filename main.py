# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import time


# TODO Handle usernames with spaces
# TODO API method

class Api:
    def __init__(self,
                 api_word):
        self.api_word = api_word


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
        self.alphabetical_frequency = 0

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

    def calculate_alphabetical_frequency(self, alphabet, alphabet_stats):

        alphabet_stats_total_count = 0
        for char in self.word:
            alphabet_stats_total_count += alphabet_stats[char]

        self.alphabetical_frequency = alphabet_stats_total_count

        print(f'WORD ALPHABET STATS {alphabet_stats_total_count}')

    def check_word(self, lang_twins_dict,
                   lang_trines_dict,
                   twin_multiplier,
                   trine_multiplier,
                   dictionary_words_list,
                   alphabet,
                   alphabet_stats,
                   word_chars_average_frequency):

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

            if dictionary_words_list.count(self.word):
                # print('WORD IN LANG DICT ', self.word)
                self.lexems_amount += 1000

            self.calculate_alphabetical_frequency(alphabet, alphabet_stats)

            if self.alphabetical_frequency < word_chars_average_frequency:
                alphabetical_multiplier = abs(word_chars_average_frequency - self.alphabetical_frequency)
                print(self.alphabetical_frequency)
                print(alphabetical_multiplier)
                alphabetical_multiplier = alphabetical_multiplier / (word_chars_average_frequency / 100)

                if alphabetical_multiplier > 5:
                    alphabetical_multiplier = 0.5
                else:
                    alphabetical_multiplier = 1

            else:
                alphabetical_multiplier = 1
            print(alphabetical_multiplier)

            self.lexems_amount = self.lexems_amount * alphabetical_multiplier


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
        self.input_list_counters = {}
        self.alphabet = []
        self.alphabet_stats = {}
        self.word_chars_average_frequency = 0

    def filter_input_words_dict(self):
        buffer_list = []
        self.input_list_counters['is_space'] = 0
        self.input_list_counters['is_not_ascii'] = 0
        self.input_list_counters['has_spaces'] = 0
        self.input_list_counters['is_url_or_email'] = 0
        for word in self.word_input_list:
            if word.word.isascii():
                if not word.word.isspace():
                    if not word.word.count(' '):
                        if not word.word.count('@') \
                                and not word.word.count('.'):
                            word.word = word.word.replace('\n', '')
                            buffer_list.append(word)
                        else:
                            self.input_list_counters['is_url_or_email'] += 1
                    else:
                        self.input_list_counters['has_spaces'] += 1
                else:
                    self.input_list_counters['is_space'] += 1
                    # print('SPACE WORD', word.word)
            else:
                self.input_list_counters['is_not_ascii'] += 1
                # print('NOT ASCII WORD', word.word)
        self.word_input_list = buffer_list

    def init_dictionary_file(self):
        file = open(self.dict_filepath, 'r')

        clear_list = []
        while True:
            line = file.readline()
            clear_list.append(line.lower())
            if not line:
                break
        file.close()

        for dict_word in clear_list:
            result = dict_word.replace('\n', '')
            if result != '':
                self.dictionary_words_list.append(result)

        print(f'WORDS COUNT IN LANGUAGE:{len(self.dictionary_words_list)}')
        print(f'LANGUAGE LIST:\n{self.dictionary_words_list}')

    def collect_alphabet_frequency(self):
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.alphabet += ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        self.alphabet += ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.alphabet_stats = {}
        for word in self.dictionary_words_list:
            for char in word:
                if self.alphabet.count(char):
                    if char not in self.alphabet_stats.keys():
                        self.alphabet_stats.update({char: 1})
                    else:
                        self.alphabet_stats[char] += 1

        alphabet_stats_total_count = 0
        for char in self.alphabet_stats:
            alphabet_stats_total_count += self.alphabet_stats[char]

        for char in self.alphabet_stats:
            char_percentage = self.alphabet_stats[char] / (alphabet_stats_total_count / 100)
            self.alphabet_stats.update({char: char_percentage})

        # print(f'ALPHA STATS:\n{self.alphabet_stats}')

        for word in self.dictionary_words_list:
            average_frequency_in_word = 0
            for char in word:
                if char in self.alphabet:
                    average_frequency_in_word += self.alphabet_stats[char]
            # print(f'{word}:{average_frequency_in_word}')
            self.word_chars_average_frequency += average_frequency_in_word
        self.word_chars_average_frequency = self.word_chars_average_frequency / len(self.dictionary_words_list)
        # print('AVERAGE ALPHABETIC FREQ', self.word_chars_average_frequency)

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

        self.collect_alphabet_frequency()

        self.calculate_dicts_in_dictionary()

        self.normalize_dicts(100)

    def check_word_list_from_file(self, filepath):
        file = open(filepath, 'r', encoding='UTF-8')
        word_list = []
        while True:
            line = file.readline()
            self.word_input_list.append(Word(line.lower()))
            if not line:
                break
        file.close()

        print(f'WORDS COUNT IN FILE "{filepath}":{len(self.word_input_list)}')

        self.filter_input_words_dict()

        print(f'WORDS COUNT FILTERED:{len(self.word_input_list)}')

        for word in self.word_input_list:
            word.check_word(self.twins_dict,
                            self.trines_dict,
                            self.twin_multiplier,
                            self.trine_multiplier,
                            self.dictionary_words_list)

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
                    # print(f'TWINS: {word.twins_list}: TTL {word.twins_amount}')
                    # print(f'DETECTED TWINS DICT: {word.twins_detected_dict}')
                    # print(f'TRINES: {word.trines_list}: TTL {word.trines_amount}')
                    # print(f'DETECTED TRINES DICT: {word.trines_detected_dict}')
                    # print(f'AMOUNT: {word.lexems_amount}')
                    # print('WORD IS ODD\n')

        words_total = good_words_total + odd_words_total
        percentage = odd_words_total / (words_total / 100)
        print(f'PERCENTAGE OF ODD WORDS {percentage}')
        print('COUNTERS')
        print(f'{self.input_list_counters}')

    def run_console(self, detailed):
        input_word = input('ENTER THE USERNAME:')
        api = Api(Word(input_word))
        api.api_word.check_word(self.twins_dict,
                                self.trines_dict,
                                self.twin_multiplier,
                                self.trine_multiplier,
                                self.dictionary_words_list,
                                self.alphabet,
                                self.alphabet_stats,
                                self.word_chars_average_frequency
                                )

        if detailed == 1:
            print(f'WORD: {api.api_word.word}')
            print(f'TWINS: {api.api_word.twins_list}: TTL {api.api_word.twins_amount}')
            print(f'DETECTED TWINS DICT: {api.api_word.twins_detected_dict}')
            print(f'TRINES: {api.api_word.trines_list}: TTL {api.api_word.trines_amount}')
            print(f'DETECTED TRINES DICT: {api.api_word.trines_detected_dict}')
            print(f'AMOUNT: {api.api_word.lexems_amount}')
        else:
            print(f'WORD: {api.api_word.word}')
            print(f'AMOUNT: {api.api_word.lexems_amount}')
        self.run_console(detailed)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    crazy = CrazyName(dict_filepath='utf.txt', sensitivity=1300, trine_multiplier=20, twin_multiplier=2)
    crazy.init_data()
    crazy.run_console(detailed=1)
    # crazy.check_word_list_from_file('ct_usernames.txt')
    # crazy.report_words_stat(show_odds_only=1, amount_gain_to_show=1200)
    print(f'EXEC TIME: {time.time() - start_time}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
