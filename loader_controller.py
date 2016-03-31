#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# TODO: Setup LCD
# TODO: Setup Loader Controller


import sys
import requests
import json


# CONSTANTS
PRESS_ID = '125'  # Should be 125 for test.  This does not change!

# Variables
api_url = 'http://localhost:5000'


def get_wo_scan():
    wo_scan = input("Scan Workorder: ")
    # wo_scan = '9934386'  # Should be 9934386 for test.
    return wo_scan


def wo_api_request(wo_id):
    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    try:
        if data['error']:
                print("Invalid Workorder!")
                run_or_exit_program('run')
    except:
        pass
    press_from_wo = data['press']
    rmat_from_wo = data['rmat']
    return press_from_wo, rmat_from_wo


def serial_api_request(sn):
    url = api_url + '/serial/' + sn
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    try:
        if data['error']:
            print("Invalid Serial Number!")
            run_or_exit_program('run')
    except:
        pass
    rmat_from_api = data['itemno']
    return rmat_from_api


def get_rmat_scan():
    rmat_scan = str(input("Scan Raw Material Serial Number: "))
    # rmat_scan = 'S07234585' for test.
    if not rmat_scan.startswith('S'):
        print("Not a Serial Number!")
        run_or_exit_program('run')
    rmat_scan = rmat_scan[1:]  # Strip off the "S" Qualifier.
    return rmat_scan


def start_loader():
    # GPIO control for PST2 and CT
    input("Loader is running.  Press ENTER to exit test.")
    run_or_exit_program('exit')


def run_or_exit_program(status):
    if status == 'run':
        print("Starting over...")
        run()
    elif status == 'exit':
        print("Exiting")
        sys.exit()


#####################################################################


def main():
    # Scan the Workorder Number (ID) Barcode.
    wo_id_from_wo = get_wo_scan()

    # Request Press Number and Raw Material Item Number from the API.
    press_from_wo, rmat_from_wo = wo_api_request(wo_id_from_wo)

    # Verify the Press Number.
    print("Checking if workorder is currently running on this press...")
    if press_from_wo == PRESS_ID:
        print("Good Workorder.  Continuing...")
    else:
        print("Incorrect Workorder!")
        run_or_exit_program('run')

    # Scan the Raw Material Serial Number Barcode.
    serial_from_label = get_rmat_scan()

    # Request Raw Material Item Number from the API.
    rmat_from_api = serial_api_request(serial_from_label)

    # Verify the Raw Material Item Number.
    print("Checking if raw material matches this workorder...")
    if rmat_from_wo == rmat_from_api:
        print("Material matches workorder.  Continuing...")
        print("Starting the Loader!")
        start_loader()
    else:
        print("Invalid Material!")
        run_or_exit_program('run')


def run():
    while True:
        main()


if __name__ == '__main__':
    run()
