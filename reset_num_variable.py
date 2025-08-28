 # reset_num_variable.py

import os
import time


def reset_variable():
    current_date = time.strftime("%Y%m%d")[2:]
    with open('.\\num_variable.txt', 'w') as f:
        f.write(current_date + '0000')


if __name__ == '__main__':
    reset_variable()
