from cn_api import Api
from cn_word import Word
from cn_sqlite import cn_sqlite


class CrazyName:

    def __init__(self, dict_filepath, sensitivity=1000, trine_multiplier=50, twin_multiplier=1):
        self.dict_filepath = dict_filepath
        self.language_list = []
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
                self.language_list.append(result)
                db = cn_sqlite.db
                db.update_language_table(self.language_list)


        print(f'WORDS COUNT IN LANGUAGE:{len(self.language_list)}')
        print(f'LANGUAGE LIST:\n{self.language_list}')

    def collect_alphabet_frequency(self):
        # TODO Снижать слишком большие значения частоты симовлов и лексем
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.alphabet += ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        self.alphabet += ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.alphabet_stats = {}
        for word in self.language_list:
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

        for word in self.language_list:
            average_frequency_in_word = 0
            for char in word:
                if char in self.alphabet:
                    average_frequency_in_word += self.alphabet_stats[char]
            # print(f'{word}:{average_frequency_in_word}')
            self.word_chars_average_frequency += average_frequency_in_word
        self.word_chars_average_frequency = self.word_chars_average_frequency / len(self.language_list)
        # print('AVERAGE ALPHABETIC FREQ', self.word_chars_average_frequency)

    def collect_dictionary_lexems(self, strafe):
        for word in self.language_list:
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
                            self.language_list,
                            self.alphabet,
                            self.alphabet_stats,
                            self.word_chars_average_frequency,
                            self.sensitivity
                            )

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
                    word.report_word()
            else:
                if word.lexems_amount > amount_gain_to_show:
                    word.report_word()

        words_total = good_words_total + odd_words_total
        percentage = odd_words_total / (words_total / 100)
        print(f'PERCENTAGE OF ODD WORDS {percentage}')
        print('COUNTERS')
        print(f'{self.input_list_counters}')
