from cn_word import WordDB


class Api:
    def __init__(self):
        self.api_word_db = WordDB
        self.json_response = ''

    def counstruct_json_response(self):
        import json
        response = {}
        pass

    def init(self, input_word, cn_main):
        self.api_word_db = WordDB(input_word.lower())
        self.api_word_db.check_word_db(cn_main)

    def run_console(self, cn_main, detailed):
        input_word = input('ENTER THE WORD:\n')
        self.init(input_word, cn_main)
        self.api_word_db.report_word()
        self.run_console(cn_main, detailed)
