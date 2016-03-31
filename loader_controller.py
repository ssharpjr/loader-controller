#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# Sanity Checks
# [X] Verify the API is available (wo_api_request)
# [ ] Verify the Press matches
# [ ] Verify the Raw Material matches


import sys
import requests
import json


# CONSTANTS
PRESS_ID = '125'  # Should be 125 for test.  This does not change!


def get_wo_scan():
    wo_scan = input("Scan Workorder: ")
    # wo_scan = '9934386'  # Should be 9934386 for test.
    return wo_scan


def wo_api_request(wo_id):
    url = 'http://localhost:5000/wo/' + wo_id
    response = requests.get(url=url)
    data = json.loads(response.text)
    try:
        if data['error']:
                print("Invalid Workorder!")
                run_or_exit_program('run')
    except:
        pass
    press_api = data['press']
    rmat_api = data['rmat']
    return press_api, rmat_api


def get_rmat_scan():
    rmat_scan = input("Scan Raw Material: ")
    # rmat_scan = str('UFPPCP-CSBLACK')
    return rmat_scan


def start_loader():
    # GPIO control for PST2 and CT
    input("Loader is running.  Press ENTER to exit test.")
    print("Exiting")
    sys.exit()


def run_or_exit_program(status):
    if status == 'run':
        print("Starting over...")
        run()
    elif status == 'exit':
        print("Exiting")
        sys.exit()


def main():
    # Scan the Workorder barcode.
    wo_id = get_wo_scan()

    # Request the Press and Raw Material Item Number from the API.
    press_api, rmat_api = wo_api_request(wo_id)

    # Verify the Press Number.
    print("Checking if workorder is currently running on this press...")
    if not press_api == PRESS_ID:
        print("Incorrect Workorder!")
        run_or_exit_program('run')
    else:
        print("Good Workorder.  Continuing...")

    # Scan the Raw Material barcode.
    rmat_scan = get_rmat_scan()
    print("Checking if raw material matches this workorder...")
    if not rmat_scan == rmat_api:
        print("Invalid Material!")
        run_or_exit_program('run')
    else:
        print("Material matches workorder.  Continuing...")
        print("Starting the Loader!")
        start_loader()


def run():
    while True:
        main()


if __name__ == '__main__':
    run()
