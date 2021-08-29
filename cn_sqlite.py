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

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    # REQUESTS TABLE

    def query_if_user_exists(self, request_id):
        """
        """

        cur = self.connection.cursor()
        cur.execute("""SELECT request_id FROM requests WHERE request_id=?""", (request_id,))
        exists = cur.fetchall()
        if exists:
            return True
        else:
            return False

    def query_set_new_event(self, tg_user_id, event_text, event_timestamp):
        is_forced = False
        forcing_period = self.execute_read_query(
            f"""SELECT forcing_period FROM users WHERE tg_user_id = {tg_user_id}"""
        )
        last_forced = 0
        initial_timestamp = event_timestamp
        forcing_count = 0
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """
                    INSERT INTO events
                    (tg_user_id,event_text,event_timestamp,is_forced,forcing_period,last_forced,initial_timestamp,forcing_count)
                    VALUES
                    (?,?,?,?,?,?,?,?)
                    """,
                    (tg_user_id, event_text, event_timestamp, is_forced,
                     forcing_period, last_forced, initial_timestamp, forcing_count)
                )
                self.connection.commit()
                print(f'Event "{event_text}" successfully saved.')
            except Error as e:
                print(f"The error '{e}' occurred")

    def query_get_user_events(self, user_id):
        query = f"SELECT * FROM events WHERE tg_user_id = '{user_id}'"
        events_list = self.execute_read_query(query)
        return events_list

    def query_set_new_user(self, data):
        with self.connection:
            try:
                cur = self.connection.cursor()
                print(data)
                cur.execute(
                    """
                    INSERT INTO users VALUES
                    (?,?,?,?,?)
                    """,
                    data
                )
                self.connection.commit()
                print(f'User {data} successfully saved.')
            except Error as e:
                print(f"The error '{e}' occurred")

    def query_update_user(self, tg_user_id, forcing_period, timezone, user_name):
        with self.connection:
            try:
                print(tg_user_id, forcing_period, timezone, user_name)
                cur = self.connection.cursor()
                cur.execute(
                    """
                    UPDATE users SET
                    forcing_period=?,timezone=?,user_name=?
                    WHERE tg_user_id=?
                    """,
                    (forcing_period, timezone, user_name, tg_user_id)
                )
                self.connection.commit()
                print(f'User id={tg_user_id} ({user_name}) successfully updated.')
            except Error as e:
                print(f"The error '{e}' occurred")

    # LANG TABLE

    def create_language_table(self):
        with self.connection:
            print('SQL: create_language_table...')
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS language(
                       word_id INT PRIMARY KEY,
                       word_text TEXT);
                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def insert_language_words(self, word):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """
                    INSERT OR IGNORE INTO language(word_text) VALUES(?);
                    """, (word,)
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def select_language_words(self):
        read_query = """
            SELECT word_text FROM language
        """
        return convert_tuples_list_to_string_list(self.execute_read_query(read_query))

    # ALPHABET TABLE

    def create_alphabet_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS alphabet(
                       char_id INTEGER PRIMARY KEY,
                       char TEXT,
                       frequency_in_lang FLOAT);
                    """
                )
                self.connection.commit()
                print(f'TABLE ALPHABET CREATED')
            except Error as e:
                print(f"The error '{e}' occurred")

    def insert_alphabet_chars(self, alphabet_dict):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    """
                    INSERT OR IGNORE INTO alphabet(char) VALUES(?);
                    """, alphabet_dict
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def update_alphabet_frequency(self, alphabet_dict):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    """
                    UPDATE alphabet SET frequency_in_lang=? WHERE char=?;
                    """, alphabet_dict
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def select_alphabet_chars(self):
        read_query = """
            SELECT char FROM alphabet
        """
        return convert_tuples_list_to_string_list(self.execute_read_query(read_query))

    # LEXEMS TABLE

    def create_lexems_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS lexems(
                       lexem_id INTEGER PRIMARY KEY,
                       lexem TEXT,
                       lexem_length INTEGER,
                       lexem_count_in_language INTEGER);
                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def insert_lexems(self, lexems_list):
        """

        :param lexems_list: lexem,lexem_length,lexem_count_in_language
        :return:
        """
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    """
                    INSERT OR IGNORE INTO lexems(lexem,lexem_count_in_language,lexem_length) VALUES(?,?,?);
                    """, lexems_list
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def update_lexems_table(self, lexems_list):
        """
        :param lexems_list: [tuple(lexem_count_in_language,lexem_length,lexem)]
        :return:
        """
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    """
                    UPDATE lexems SET lexem_count_in_language=?,lexem_length=? WHERE lexem=?;
                    """, lexems_list
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def select_lexem_value(self, lexem: str, value_name):
        with self.connection:
            try:
                query = "SELECT " + value_name + " FROM lexems where lexem='" + lexem + "'"
                ic(query)
                cur = self.connection.cursor()
                cur.execute(query)
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

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
