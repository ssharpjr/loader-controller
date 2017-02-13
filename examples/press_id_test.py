#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

# import os
# import sys


press_id_file = "/boot/PRESS_ID"


def get_press_id():
    # Get the press_id from /boot/PRESS_ID file
    try:
        with open(press_id_file) as f:
            PRESS_ID = f.read()
            if PRESS_ID is not None:
                return PRESS_ID
            else:
                raise ValueError("PRESS_ID is None!")
    except IOError:
        print(press_id_file + " Not Found!")
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    PRESS_ID = get_press_id()
    print("Press ID: " + str(PRESS_ID))
