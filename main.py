from cn_api import Api
import time
from cn_main_class import CrazyName

# TODO Handle usernames with spaces
# TODO API method


CONSOLE = 1

if __name__ == '__main__':
    start_time = time.time()
    crazy = CrazyName(dict_filepath='utf.txt', sensitivity=1300, trine_multiplier=20, twin_multiplier=2)
    crazy.init_data()
    if CONSOLE == 1:
        api = Api()
        api.run_console(cn_main=crazy, detailed=1)
    else:
        crazy.bulk_check_words_from_file('ct_usernames.txt')
        crazy.bulk_report_words_stat(show_odds_only=1, amount_gain_to_show=0)
    print(f'EXEC TIME: {time.time() - start_time}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
