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
        self.normal_word_probability = 0

    def calculate_word_lexems(self, lang_twins_dict, lang_trines_dict):

        for twin in self.twins_list:
            if twin in lang_twins_dict.keys():
                self.twins_amount += lang_twins_dict[twin]
                self.twins_detected_dict[twin] = lang_twins_dict[twin]

        for trine in self.trines_list:
            if trine in lang_trines_dict.keys():
                self.trines_amount += lang_trines_dict[trine]
                self.twins_detected_dict[trine] = lang_trines_dict[trine]

    def collect_word_lexems(self, strafe):
        # TODO добавить проверку четвёрок и пятёрок
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

    def calculate_word_alphabetical_frequency(self, alphabet, alphabet_stats):

        alphabet_stats_total_count = 0
        for char in self.word:
            if char in alphabet:
                alphabet_stats_total_count += alphabet_stats[char]

        self.alphabetical_frequency = alphabet_stats_total_count
        # print(f'WORD ALPHABET STATS {alphabet_stats_total_count}')

    def check_word(self, lang_twins_dict,
                   lang_trines_dict,
                   twin_multiplier,
                   trine_multiplier,
                   language_dict,
                   alphabet,
                   alphabet_stats,
                   word_chars_average_frequency,
                   sensitivity):

        # TODO Снижать lexem_amount за дубли в лексемах
        # TODO Разбить chek_word по функциям
        # TODO добавить все параметры аналитики в тело класса Word

        if self.word:

            self.word = self.word.replace('-', '')

            self.collect_word_lexems(strafe=0)
            self.collect_word_lexems(strafe=1)
            self.collect_word_lexems(strafe=2)

            self.calculate_word_lexems(lang_twins_dict, lang_trines_dict)

            x = len(self.word)

            power = -0.1 * x

            word_length_multiplier = 12 * pow(x, power)

            self.lexems_amount = word_length_multiplier * ((self.twins_amount * twin_multiplier) + (
                    self.trines_amount * trine_multiplier))

            self.calculate_word_alphabetical_frequency(alphabet, alphabet_stats)

            if self.alphabetical_frequency < word_chars_average_frequency:
                alphabetical_multiplier = abs(word_chars_average_frequency - self.alphabetical_frequency)
                print(self.alphabetical_frequency)
                print(alphabetical_multiplier)
                alphabetical_multiplier = alphabetical_multiplier / (word_chars_average_frequency / 100)

                if alphabetical_multiplier > 5:
                    alphabetical_multiplier = 0.2
                else:
                    alphabetical_multiplier = 1

            else:
                alphabetical_multiplier = 1
            print(alphabetical_multiplier)

            self.lexems_amount = self.lexems_amount * alphabetical_multiplier

            if language_dict.count(self.word):
                print('WORD IN LANG DICT ', self.word)
                self.lexems_amount += 1300
            else:
                for word in language_dict:
                    if self.word.find(word) != -1:
                        containment_multiplier = len(self.word.replace(word, '')) / (len(self.word) / 100)
                        containment_addiction = sensitivity * (containment_multiplier / 100)
                        print('containment_multiplier', containment_multiplier)
                        print('containment_addiction', containment_addiction)
                        self.lexems_amount += containment_addiction
                        break

            if self.lexems_amount > sensitivity:
                self.normal_word_probability = 100
            else:
                self.normal_word_probability = 100 - ((sensitivity - self.lexems_amount) / (sensitivity / 100))

    def report_word(self):
        result = \
            f'=================\n' + \
            f'WORD: {self.word}\n' + \
            f'TWINS: {self.twins_list}: TTL {self.twins_amount}\n' + \
            f'DETECTED TWINS DICT: {self.twins_detected_dict}\n' + \
            f'TRINES: {self.trines_list}: TTL {self.trines_amount}\n' + \
            f'DETECTED TRINES DICT: {self.trines_detected_dict}\n' + \
            f'AMOUNT: {self.lexems_amount}\n' + \
            f'PROBABILITY THAT WORD IS FINE: {self.normal_word_probability}\n' + \
            f'================='
        print(result)
        return result