#! /usr/bin/env python3
# -*- encoding: utf-8 -*-


import os


def get_press_id_from_env():
    try:
        PRESS_ID = os.environ['PRESS_ID']
        if PRESS_ID is not None:
            return PRESS_ID
    except KeyError:
        print("PRESS_ID environment variable is not set.")
    except BaseException as e:
        print(e)


def get_press_id_from_file():
    press_id_file = '/boot/PRESS_ID'
    if os.path.isfile(press_id_file):
        try:
            with open('/boot/PRESS_ID', 'r') as f:
                PRESS_ID = f.read().replace('\n', '')
            if len(PRESS_ID) < 1:
                print("PRESS_ID file is blank")
        except IOError:
            print("/boot/PRESS_ID file missing")
        except BaseException as e:
            print(e)
        return PRESS_ID
    else:
        print(press_id_file + " Not Found")


def get_press_id():
    try:
        PRESS_ID = get_press_id_from_env()
        if len(PRESS_ID) < 1:
            PRESS_ID = get_press_id_from_file()
            os.environ['PRESS_ID'] = PRESS_ID
            return PRESS_ID
    except BaseException as e:
        print("PRESS_ID could not be found")
        print(e)


if __name__ == '__main__':
    PRESS_ID = get_press_id()
    print(PRESS_ID)
