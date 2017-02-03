#! /usr/bin/env python3

from iqapi import *

press_id = '136'

def get_wo_id_from_api(press_id):
    wo_id = wo_id_api_request(press_id)
    return wo_id


wo_id_from_api = get_wo_id_from_api(press_id)
print(wo_id_from_api)
