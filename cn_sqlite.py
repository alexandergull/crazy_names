import sqlite3
from icecream import ic

import sqlite3
from sqlite3 import Error


class CnSQLite:
    """
        SQlite handling class.

        Structure:
            {
            connection: connection to SQlite,
            path: path to SQlite DB,
            create_connection: initialize connection method
            }
    """

    def __init__(self,
                 path,
                 ):
        self.connection = None
        self.path = path
        self.create_connection(path)

    # INIT

    def create_connection(self, path):
        """
        Init SQlite connection.
        Params:
            path - path to sqlite database
        """
        try:
            self.connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    # COMMON

    def select_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def executemany_query(self, query, many_list):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    query, many_list
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def execute_query(self, query):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(query)
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")


    # LANG TABLE

    def create_language_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS language(
                   word_id INT PRIMARY KEY,
                   word_text TEXT);
                """
        self.execute_query(query)

    def insert_language_word(self, word):
        query = "INSERT OR IGNORE INTO language(word_text) VALUES(?);"
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    query, (word,)
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def select_language_words(self):
        read_query = """
            SELECT word_text FROM language
        """
        return convert_tuples_list_to_string_list(self.select_query(read_query))

    # ALPHABET TABLE

    def create_alphabet_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS alphabet(
                   char_id INTEGER PRIMARY KEY,
                   char TEXT,
                   frequency_in_lang FLOAT);
                """
        self.execute_query(query)

    def insert_alphabet_chars(self, alphabet_dict):
        query = "INSERT OR IGNORE INTO alphabet(char) VALUES(?);"
        self.executemany_query(query, alphabet_dict)

    def update_alphabet_frequency(self, alphabet_dict):
        query = "UPDATE alphabet SET frequency_in_lang=? WHERE char=?;"
        self.executemany_query(query, alphabet_dict)

    def select_all_alphabet_chars(self):
        read_query = "SELECT char FROM alphabet"
        return convert_tuples_list_to_string_list(self.select_query(read_query))

    def select_alphabet_char_frequency(self, char):
        read_query = "SELECT frequency_in_lang FROM alphabet WHERE char='" + char + "'"
        return convert_tuples_list_to_string_list(self.select_query(read_query))

    # LEXEMS TABLE

    def create_lexems_table(self):

        query = """
                CREATE TABLE IF NOT EXISTS lexems(
                   lexem_id INTEGER PRIMARY KEY,
                   lexem TEXT,
                   lexem_length INTEGER,
                   lexem_count_in_language INTEGER);
                """
        self.execute_query(query)

    def insert_lexems(self, lexems_list):
        """
        :param lexems_list: lexem,lexem_length,lexem_count_in_language
        """
        query = "INSERT OR IGNORE INTO lexems(lexem,lexem_count_in_language,lexem_length) VALUES(?,?,?);"
        self.executemany_query(query, lexems_list)

    def update_lexems_table(self, lexems_list):
        """
        :param lexems_list: [tuple(lexem_count_in_language,lexem_length,lexem)]
        :return:
        """
        query = """UPDATE lexems SET lexem_count_in_language=?,lexem_length=? WHERE lexem=?;"""
        self.executemany_query(query, lexems_list)

    def select_lexem_value(self, lexem: str, value_name):
        """

        :param lexem:
        :param value_name:
        :return: list of strings
        """
        query = "SELECT " + value_name + " FROM lexems where lexem='" + lexem + "'"
        return convert_tuples_list_to_string_list(self.select_query(query))

    ###########

    def db_test(self):
        # self.create_language_table()
        # self.create_alphabet_table()
        # self.create_lexems_table()
        pass


def convert_tuples_list_to_string_list(tuples_list):
    string_list = []
    for record in list(tuples_list):
        string_list.append(list(record)[0])
    return string_list


db = CnSQLite('cn_sqlite/crazynames.sqlite')
db.db_test()
