#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import sys
import csv
from .settings import *
from .constants import *

idx = lambda x:FIELDS_IDX.get(x)

def get_file_path():
    if CSV_PATH:
        if not os.path.exists(CSV_PATH):
            os.makedirs(CSV_PATH)
        file_path = os.path.join(CSV_PATH, CSV_NAME)
    else:
        file_path = CSV_NAME
    if not os.path.isfile(file_path):
        os.mknod(file_path)
    return file_path

def read_csv():
    file_path = get_file_path()
    with open(file_path, 'r') as f:
        datas = csv.reader(f)
        return list(datas)

def write_csv(datas):
    file_path = get_file_path()
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for i in datas:
            writer.writerow(i)

def del_csv():
    file_path = get_file_path()
    os.remove(file_path)

def find_by(datas, **where):
    res = []
    for data in datas:
        for field in where.keys():
            if field in SEARCH_FIELDS + SEARCH_FIELDS_ABB:
                if str(data[idx(field)]).find(where[field]) == -1:
                    break
            else:
                if data[idx(field)] != where[field]:
                    break
        else:
            res.append(data)
    return res

def format_show(data, fields):
    res = []
    for field in fields:
        if field == 'path':
            res.append(data[idx('id')])
        elif field == 'status':
            res.append(STATUS[data[idx(field)]])
        else:
            res.append(data[idx(field)])
    return res

