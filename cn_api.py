from cn_word import Word, WordDB


class Api:
    def __init__(self):
        self.api_word = Word
        self.api_word_db = WordDB
        self.json_response = ''

    def counstruct_json_response(self):
        import json
        response = {}
        pass

    def init(self, input_word, cn_main):
        self.api_word = input_word.lower()
        # self.api_word = Word(self.api_word)
        # self.api_word.check_word(cn_main.twins_dict,
        #                          cn_main.trines_dict,
        #                          cn_main.twin_multiplier,
        #                          cn_main.trine_multiplier,
        #                          cn_main.language_list,
        #                          cn_main.alphabet,
        #                          cn_main.alphabet_stats,
        #                          cn_main.language_chars_average_frequency,
        #                          cn_main.sensitivity
        #                          )
        self.api_word_db = WordDB(input_word.lower())
        self.api_word_db.check_word_db(cn_main)

    def run_console(self, cn_main, detailed):
        input_word = input('ENTER THE WORD:\n')
        self.init(input_word, cn_main)
        # self.api_word.report_word()
        self.api_word_db.report_word()

        self.run_console(cn_main, detailed)
