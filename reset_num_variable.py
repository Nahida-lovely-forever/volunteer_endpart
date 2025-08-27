 # reset_num_variable.py

import os
import time


def reset_variable():
    current_date = time.strftime("%Y%m%d")
    with open('.\\num_variable.txt', 'w') as f:
        f.write(current_date + '1')


if __name__ == '__main__':
    reset_variable()
