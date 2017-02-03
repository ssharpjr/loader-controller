#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

import requests
import json


# Variables
api_url = 'http://10.130.0.42'  # Web API URL


def wo_id_api_request(press_id):
    url = api_url + '/press/' + press_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        wo_id = data['wo_id']
        return wo_id
    except:
        print("\nAPI Data is incomplete")
        print(data)


def press_api_request(press_id):
    url = api_url + '/press/' + press_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        press_id = data['press']
        wo_id = data['wo_id']
        itemno = data['itemno']
        descrip = data['descrip']
        itemno_mat = data['itemno_mat']
        descrip_mat = data['descrip_mat']
        return press_id, wo_id, itemno, descrip, itemno_mat, descrip_mat
    except:
        print("\nAPI Data is incomplete")
        print(data)


def wo_api_request(wo_id):
    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        press_from_api_wo = data['press']
        rmat_from_api_wo = data['rmat']
        return press_from_api_wo, rmat_from_api_wo
    except:
        print("\nAPI Data is incomplete")
        print(data)


def serial_api_request(sn):
    url = api_url + '/serial/' + sn
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        rmat_from_api = data['itemno']
    except:
        print("\nAPI Data is incomplete")
        print(data)
    return rmat_from_api


def test_press_api_request(press_id):
    press_id, wo_id, itemno, descrip,\
    itemno_mat, descrip_mat = press_api_request(press_id)

    print("Testing Press API Request")
    print("\nPress: " + press_id)
    print("Work Order: " + wo_id)
    print("Item Number: " + itemno)
    print("Item Description: " + descrip)
    print("Raw Material Item Number: " + itemno_mat)
    print("Raw Material Description: " + descrip_mat)


def test_wo_api_request(wo_id):
    press, rmat = wo_api_request(wo_id)

    print("Testing WO API Request")
    print("Press: " + press)
    print("\nWork Order: " + wo_id)
    print("Raw Material Item Number: " + rmat)

if __name__ == '__main__':
    test_press_api_request('136')
    test_wo_api_request('10284800')
