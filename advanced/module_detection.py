#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import type_dist, declaration_intro
from extract_archive import naive

folder_specify = ['Auto_hook_control_system', 'anti_swing_contorl', 'super_tower_condition_tele']
feature_sentence = '	rope_length_theory_standardization_once:REAL;'


def check(text):
    if decision['AutoHook'] != 0:
        if feature_sentence in text.encode('utf-8'):
            print("在内容中发现特征声明语句: '%s'" % feature_sentence)
            decision['AutoHook'] += 1
        else:
            print('已进入文件夹，正在查找')


def print_tree(treeobj, depth, path, verbose=False):
    global count
    global info

    # record current Path
    cur_path = path

    content = ''  # text
    type_spec = ''  # type

    # get object name
    name = treeobj.get_name(False)
    id = treeobj.type.ToString()

    if not folder_specify: verbose = True

    if id in type_dist:
        type_spec = type_dist[id]
    else:
        info[id] = name

    if treeobj.is_device:
        deviceid = treeobj.get_device_identification()
        content = 'type=' + str(deviceid.type) + '\nid=' + str(deviceid.id) + '\nver=' + str(deviceid.version)
    elif treeobj.is_folder:
        pass
    elif treeobj.is_task_configuration:
        pass
        # exports=[treeobj]
        # projects.primary.export_native(exports,os.path.join(cur_path,name+'.tc'))
    elif treeobj.is_task:
        exports = [treeobj]
        if verbose: projects.primary.export_native(exports, os.path.join(cur_path, name + '.task'))
    elif treeobj.is_libman:
        exports = [treeobj]
        if verbose: projects.primary.export_native(exports, os.path.join(cur_path, name + '.lib'))
    elif treeobj.is_textlist:
        if verbose:  treeobj.export(os.path.join(cur_path, name + '.tl'))
    else:
        if treeobj.has_textual_declaration:
            content = content + declaration_intro
            a = treeobj.textual_declaration
            content = content + a.text

        # if treeobj.has_textual_implementation:
        #     content = content + implementation_intro
        #     a = treeobj.textual_implementation
        #     content = content + a.text

    children = treeobj.get_children(False)

    # 根据需要新建文件夹
    if children:
        if type_spec:
            cur_path = os.path.join(cur_path, name + '.' + type_spec)
        else:
            cur_path = os.path.join(cur_path, name)
        if name in folder_specify:
            verbose = True
            # if not os.path.exists(cur_path):
            #     os.makedirs(cur_path)
            folder_mapping = {
                folder_specify[0]: 'AutoHook',
                folder_specify[1]: 'AntiSwing',
                folder_specify[2]: 'AutoTele'
            }
            decision[folder_mapping.get(name)] = 1
        else:
            verbose = False

    if content and verbose:
        check(content)
        count += 1

    for child in children:
        print_tree(child, depth + 1, cur_path, verbose)


if __name__ == '__main__':
    info = {}
    count = 0

    print("sys.argv: ", len(sys.argv), " elements:")
    for arg in sys.argv:
        print(" - ", arg)
    if len(sys.argv) > 1:
        current_dir = sys.argv[1]
    else:
        current_dir = r'C:\Users\13ANH\Downloads\emergent\智能化功能配置(非发布版本)\ZAT8000V863\CR720S'

    found = False  # 标志变量
    valid_projects = []  # 用于存储符合条件的文件名的列表
    if os.path.isdir(current_dir):
        for root, _, files in os.walk(current_dir):
            for file in files:
                if file.endswith(".project") and "E107" not in file:  # 排除包含 "E107" 的文件
                    project_path = os.path.join(root, file)
                    valid_projects.append(project_path)  # 存入列表
                    print("Found:", os.path.relpath(project_path, current_dir))
                    found = True  # 设为 True，表示找到至少一个合格的文件

        # 如果没有找到任何符合条件的 .project 文件，则退出
        if not found:
            print("No valid .project files found. Exiting...")
            sys.exit(0)  # 正常退出
    print(len(valid_projects), 'projects found. Please confirm again!')

    decision_table = []  #
    for project in valid_projects:
        filename, _ = os.path.splitext(os.path.basename(project))  # 分离文件名和扩展

        decision = {'Series': os.path.relpath(project, current_dir), 'Model': filename, 'AutoHook': 0, 'AutoTele': 0,
                    'AntiSwing': 0}
        print("Opening:", '-' * 27)
        print("Opening:", os.path.relpath(project, current_dir))
        proj = projects.open(project, password=naive(filename)[0])
        for obj in proj.get_children():
            print_tree(obj, 0, '')
        if proj:
            print("Success!", '-' * 27)
            proj.close()  # close open project if necessary
        else:
            print('-' * 27, "Open Failed!  " * 3)
            decision['AutoHook'] = -1
            decision['AutoTele'] = -1
            decision['AntiSwing'] = -1
        decision_table.append(decision)

    print(len(decision_table), 'decisions detected. Please confirm again!')

    if len(sys.argv) > 1:
        # 打开 CSV 文件并使用 utf-8 编码
        with open('decision.csv', 'w') as f:
            f.write(','.join(decision_table[0].keys()))
            f.write('\n')
            for row in decision_table:
                f.write(','.join(str(x) for x in row.values()).encode('utf-8'))
                f.write('\n')
