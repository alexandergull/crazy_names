from cn_word import Word
import cn_sqlite
from icecream import ic


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
        self.db = cn_sqlite.db

    # DATABASE PART

    def add_dictionary_file_to_db(self):
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
                self.db.insert_language_words(result)

    def add_alphabet_to_db(self):
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        alphabet += ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        alphabet += ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        # ic(alphabet)
        formatted_alphabet = list(map(lambda x: tuple(x), alphabet))
        # ic(formatted_alphabet)
        self.db.insert_alphabet_chars(formatted_alphabet)

    def update_lexems_table(self):
        formatted_lexems_dict_to_update = []
        for twin in self.twins_dict:
            formatted_lexems_dict_to_update.append((self.twins_dict[twin], 2, twin,))
            pass
        for trine in self.trines_dict:
            formatted_lexems_dict_to_update.append((self.trines_dict[trine], 3, trine,))
            pass
        self.db.update_lexems_table(formatted_lexems_dict_to_update)

    # COLLECTING

    def collect_lang_lexems(self, strafe):
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

    # CALCULATING

    def calculate_lang_alphabetic_frequency(self):
        # TODO Снижать слишком большие значения частоты симовлов и лексем

        # self.add_alphabet_to_db()

        self.alphabet_stats = {}

        self.alphabet = self.db.select_alphabet_chars()

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

        formatted_alphabet = list(map(lambda x, y:
                                      (y, x,),
                                      self.alphabet_stats.keys(),
                                      self.alphabet_stats.values()))

        self.db.update_alphabet_frequency(formatted_alphabet)

        for word in self.language_list:
            average_frequency_in_word = 0
            for char in word:
                if char in self.alphabet:
                    average_frequency_in_word += self.alphabet_stats[char]
            # print(f'{word}:{average_frequency_in_word}')
            self.word_chars_average_frequency += average_frequency_in_word
        self.word_chars_average_frequency = self.word_chars_average_frequency / len(self.language_list)
        # print('AVERAGE ALPHABETIC FREQ', self.word_chars_average_frequency)

    def calculate_lang_lexems_frequency(self):
        for twin in self.twins_list:
            if twin not in self.twins_dict:
                self.twins_dict[twin] = self.twins_list.count(twin)
        # print(self.twins_dict)

        for trine in self.trines_list:
            if trine not in self.trines_dict:
                self.trines_dict[trine] = self.trines_list.count(trine)
        # print(self.trines_dict)

        formatted_lexems_dict_to_insert = []
        for twin in self.twins_dict:
            formatted_lexems_dict_to_insert.append((twin, self.twins_dict[twin], 2,))
            pass
        for trine in self.trines_dict:
            formatted_lexems_dict_to_insert.append((trine, self.trines_dict[trine], 3,))
            pass
        self.db.insert_lexems(formatted_lexems_dict_to_insert)

    def normalize_lang_lexems_dicts(self, normal):
        for twin in self.twins_dict:
            if self.twins_dict[twin] > normal:
                self.twins_dict[twin] = self.twins_dict[twin] // 3
        self.update_lexems_table()
    # INIT

    def init_language_list(self):
        self.language_list = self.db.select_language_words()
        print(f'WORDS COUNT IN LANGUAGE DB:{len(self.language_list)}')
        # print(f'LANGUAGE LIST DB:\n{self.language_list}')

    def init_data(self):
        # if needs to update DB
        # self.add_dictionary_file_to_db()

        # init language from db
        self.init_language_list()

        # collect lexems with strafes
        self.collect_lang_lexems(0)
        self.collect_lang_lexems(1)
        self.collect_lang_lexems(2)

        # collect alphabet
        self.calculate_lang_alphabetic_frequency()

        self.calculate_lang_lexems_frequency()

        self.normalize_lang_lexems_dicts(100)

        ic(self.db.select_lexem_value('as', 'lexem_count_in_language'))

    # bulk check

    def bulk_check_words_from_file(self, filepath):
        file = open(filepath, 'r', encoding='UTF-8')
        word_list = []
        while True:
            line = file.readline()
            self.word_input_list.append(Word(line.lower()))
            if not line:
                break
        file.close()

        print(f'WORDS COUNT IN FILE "{filepath}":{len(self.word_input_list)}')

        self.bulk_check_file_filtration()

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

    def bulk_check_file_filtration(self):
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

    def bulk_report_words_stat(self, show_odds_only=1, amount_gain_to_show=100):
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
