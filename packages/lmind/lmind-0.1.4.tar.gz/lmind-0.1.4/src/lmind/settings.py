#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

ID_SPLIT_STR = '-'
SPLIT_STR = '&&'
CSV_PATH = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = 'tasks.csv'
CONF_NAME = 'conf.csv'
TIME_FORMAT = '%Y-%m-%d'
DATE_FORMAT = ['%Y-%m-%d', '%Y%m%d', '%Y/%m/%d', '%Y.%m.%d']

FIELDS = ['id', 'parent_id', 'name', 'executor', 'description', 'deadline', 
              'status', 'display', 'finish_date', 'create_date']
FIELDS_ABB = ['id', 'pid', 'na', 'exe', 'desc', 'dl', 'sta', 'dis', 'fd', 'cd']
FIELDS_IDX = {field:index for index, field in enumerate(FIELDS)}
FIELDS_IDX.update(
    {field:index for index, field in enumerate(FIELDS_ABB)}
)
SHOW_FIELDS = ['path', 'name', 'executor', 'deadline', 'status']
SHOW_FIELDS_ABB = ['id'] + [FIELDS_ABB[FIELDS_IDX[field]] for field in SHOW_FIELDS[1:]]
SHOW_ALL_FIELDS = ['path', 'name', 'executor', 'description',  'deadline', 
                   'status', 'display', 'finish_date', 'create_date']
SHOW_ALL_FIELDS_ABB = ['id'] + [FIELDS_ABB[FIELDS_IDX[field]] for field in SHOW_ALL_FIELDS[1:]]
UPDATE_FIELDS = ['name', 'executor', 'description', 'deadline']
UPDATE_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in UPDATE_FIELDS]
WHERE_FIELDS = ['name', 'executor', 'description', 'deadline', 'status']
WHERE_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in WHERE_FIELDS]
ORDER_FIELDS = ['deadline', 'finish_date', 'create_date']
ORDER_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in ORDER_FIELDS]
SEARCH_FIELDS = ['name', 'executor', 'description']
SEARCH_FIELDS_ABB = [FIELDS_ABB[FIELDS_IDX[field]] for field in SEARCH_FIELDS]

CONF_TYPE = ['show-info']
