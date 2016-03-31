#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# Sanity Checks
# [X] Verify the API is available (wo_api_request)
# [ ] Verify the Press matches
# [ ] Verify the Raw Material matches


import sys
import urllib.request
import json


# CONSTANTS
PRESS_ID = '125'  # Should be 125 for test.  This does not change!


def get_wo_scan():
    wo_scan = input("Scan Workorder: ")
    # wo_scan = '9934386'  # Should be 9934386 for test.
    return wo_scan


def wo_api_request(wo_id):

    try:
        url = 'http://localhost:5000/wo/' + wo_id
        response = urllib.request.urlopen(url)
        str_response = response.readall().decode('utf-8')
    except:
        response = json.dumps({"error": "Not found"})
        str_response = response

    obj = json.loads(str_response)

    try:
        press = obj['press']
        rmat = obj['rmat']
        error = ''
        return press, rmat, error
    except:
        press = ''
        rmat = ''
        error = obj['error']
        return press, rmat, error


def get_rmat_scan():
    rmat_scan = input("Scan Raw Material: ")
    # rmat_scan = str('UFPPCP-CSBLACK')
    return rmat_scan


def start_loader():
    # GPIO control for PST2 and CT
    input("Loader is running.  Press ENTER to exit test.")
    print("Exiting")
    sys.exit()


def exit_program():
    # print("Exiting")
    # sys.exit()
    run()


def main():
    # Scan the Workorder barcode.
    wo_id = get_wo_scan()

    # Request the Press and Raw Material Item Number from the API.
    press, rmat, error = wo_api_request(wo_id)
    if error:
        print("Not a valid Workorder!")
        exit_program()

    # Verify the Press Number.
    print("Checking if workorder is currently running on this press...")
    if not press == PRESS_ID:
        print("Workorder is not running on this press!")
        exit_program()
    else:
        print("Good Workorder.  Continuing...")

    # Scan the Raw Material barcode.
    rmat_scan = get_rmat_scan()
    print("Checking if raw material matches this workorder...")
    if not rmat_scan == rmat:
        print("Invalid Material!")
        exit_program()
    else:
        print("Material matches workorder.  Continuing...")
        print("Starting the Loader!")
        start_loader()


def run():
    while True:
        main()


if __name__ == '__main__':
    run()
