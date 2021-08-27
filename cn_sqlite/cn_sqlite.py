import sqlite3

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

    def update_language_table(self, language_list):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.executemany(
                    """
                    INSERT INTO language VALUES(?);
                    """, language_list
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def get_language_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    # ALPHABET TABLE

    def create_alphabet_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def update_alphabet_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def get_alphabet_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    # LEXEMS TABLE

    def create_lexems_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def update_lexems_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    def get_lexems_table(self):
        with self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(
                    """

                    """
                )
                self.connection.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

    ###########

    def db_test(self):
        self.create_language_table()


db = CnSQLite('cn_sqlite/crazynames.sqlite')
# db.db_test()
