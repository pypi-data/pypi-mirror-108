#coding:utf-8

import os
import copy
import sys
from datetime import datetime
from prettytable import PrettyTable
from .settings import *
from .constants import *
from .utils import *
from .task import Task
pt = PrettyTable()


def show(origs, origs_dict, ids, is_all=None, where=None):
    '''显示任务列表'''
    if not where:
        where = dict()
    if is_all:
        pt.field_names = SHOW_ALL_FIELDS
        # pt.add_row(['abbr'] + SHOW_ALL_FIELDS_ABB[1:])
    else:
        # 读取用户自定义字段
        conf_datas =  read_conf_file()
        if conf_datas and conf_datas[0]:
            pt.field_names = conf_datas[0]
        else:
            pt.field_names = SHOW_FIELDS
        # pt.add_row(['abbr'] + SHOW_FIELDS_ABB[1:])
    if 'path' in pt.field_names:
        pt.align["path"] = "l"
    if 'name' in pt.field_names:
        pt.align["name"] = "l"
    show_tasks = list()
        
    def show_child(parent_id, l):
        if is_all:
            # 显示所有
            tasks = find_by(origs, parent_id=parent_id)
        else:
            # 只显示可显示的
            tasks = find_by(origs, parent_id=parent_id, display='1')
        for n, i in enumerate(tasks):
            path = l*'│   ' + (
                    '└── ' if n==len(tasks)-1 else '├── '
                ) + i[0]
            show_tasks.append((
                i[0],
                format_show([path] + i[1:], pt.field_names)))

            show_child(i[idx('id')], l+1)
    for task_id in ids:
        if task_id != '0':
            show_tasks.append((
                task_id,
                format_show(origs_dict[task_id], pt.field_names)
            ))
        show_child(task_id, 0)
    if where:
        filter_tasks = find_by(origs, **where)
        filter_id_set = set()
        # 增加所有父节点

        for i in filter_tasks:
            task = i
            while True:
                filter_id_set.add(task[idx('id')])
                if task[idx('parent_id')] == '0':
                    break
                task = origs_dict[task[idx('parent_id')]]

        # 过滤掉不满足条件的
        show_tasks = [i for i in show_tasks if i[0] in filter_id_set]

    for i in show_tasks:
        pt.add_row(i[1])

    # show
    print(pt)
    return 1

def create(origs, name):
    '''新建项目'''
    task = Task()
    task.id = str(int(origs[-1][idx('id')])+1) if origs else '1'
    task.parent_id = '0'
    task.name = name
    origs.append(task.to_list())
    write_csv(origs)
    return 1

def add_tasks(origs, parent_id, names):
    '''增加任务'''
    for name in names:
        task = Task()
        task.id = str(int(origs[-1][idx('id')])+1)
        task.parent_id = parent_id
        task.name = name
        origs.append(task.to_list())
    write_csv(origs)
    return 1

def rm_tasks(origs, origs_dict, task_ids):
    '''移除任务, 使任务不显示'''
    def rm_children(parent_id):
        nonlocal origs
        nonlocal origs_dict
        tasks = find_by(origs, parent_id=parent_id, display='1')
        for task in tasks:
            origs_dict[task[idx('id')]][idx('display')] = '0'
            rm_children(task[idx('id')])
    for task_id in task_ids:
        origs_dict[task_id][idx('display')] = '0'
        # 如果存在子任务，那么也要把所有子任务隐藏
        rm_children(task_id)

    write_csv(origs_dict.values())
    return 1

def bk_tasks(origs, origs_dict, task_ids):
    '''召回任务, 使任务显示'''
    for task_id in task_ids:
        origs_dict[task_id][idx('display')] = '1'
        # 如果父任务是隐藏的，那么也要把父任务显示出来
        task = origs_dict[task_id]
        while True:
            if task[idx('parent_id')] == '0':
                break
            parent_task = origs_dict[task[idx('parent_id')]]
            if parent_task[idx('display')] == '1':
                break
            origs_dict[parent_task[idx('id')]][idx('display')] = '1'
            task = parent_task

    write_csv(origs_dict.values())
    return 1

def del_tasks(origs, origs_dict, task_ids, is_all=False):
    '''删除任务'''
    if is_all:
        del_csv()
        return 1
    def del_children(parent_id):
        nonlocal origs
        nonlocal origs_dict
        tasks = find_by(origs, parent_id=parent_id, display='1')
        for task in tasks:
            del origs_dict[task[idx('id')]]
            del_children(task[idx('id')])
    for task_id in task_ids:
        del origs_dict[task_id]
        # 如果存在子任务，那么也要把所有子任务删除
        del_children(task_id)

    write_csv(origs_dict.values())
    return 1

def mv_tasks(origs_dict, task_ids, target_parent_id):
    '''转移任务'''
    for task_id in task_ids:
        origs_dict[task_id][idx('parent_id')] = target_parent_id
    write_csv(origs_dict.values())
    return 1

def update_tasks(origs, origs_dict, task_ids, values):
    '''修改任务，修改名称，创建者，执行者, 计划时间'''
    def update_children_status(parent_id, value):
        nonlocal origs
        nonlocal origs_dict
        tasks = find_by(origs, parent_id=parent_id)
        for task in tasks:
            origs_dict[task[idx('id')]][idx('status')] = value
            if value == DONE:
                # 更新完成时间
                origs_dict[task[idx('id')]][idx('finish_date')] \
                    = datetime.now().strftime(TIME_FORMAT)
            if value == WORKING:
                # 清除完成时间
                origs_dict[task[idx('id')]][idx('finish_date')] = ''
            update_children_status(task[idx('id')], value)

    for task_id in task_ids:
        for key in values.keys():
            origs_dict[task_id][idx(key)] = values[key]
            if key == 'status' or key == FIELDS_ABB[idx('status')]:
                if values[key] == DONE:
                    # 更新完成时间
                    origs_dict[task_id][idx('finish_date')] \
                        = datetime.now().strftime(TIME_FORMAT)
                if values[key] == WORKING:
                    # 清除完成时间
                    origs_dict[task_id][idx('finish_date')] = ''
                update_children_status(task_id, values[key])
    write_csv(origs_dict.values())
    return 1

def conf_show_fields(fields=''):
    '''设置自定义字段'''
    conf_datas = read_conf_file()
    if conf_datas:
        conf_datas[0] = fields
    else:
        conf_datas = [fields]
    write_conf_file(conf_datas)
    

