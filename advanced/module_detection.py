#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import codecs
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import type_dist, declaration_intro
from extract_archive import naive

folder_specify = ['Auto_hook_control_system', 'anti_swing_contorl', 'super_tower_condition_tele']
abbr_mapping = {
    folder_specify[0]: 'AutoHook',
    folder_specify[1]: 'AntiSwing',
    folder_specify[2]: 'AutoTele'
}
feature_mapping = {
    folder_specify[0]: '	rope_length_theory_standardization_sub:REAL;'
}


def detect():
    global info

    # 直接查找文件夹
    for name_spec in folder_specify:
        res = [obj for obj in proj.find(name_spec, True) if obj.is_folder]
        if res:
            decision[abbr_mapping.get(name_spec)] = 1

        # 找到文件夹还需要找某个特殊文件
        if decision[abbr_mapping.get(name_spec)] != 0:
            feature_sentence = feature_mapping.get(name_spec)
            if feature_sentence:
                for child in res[0].get_children(True):
                    guid = child.type.ToString()
                    if type_dist.get(guid) == 'pou':
                        text = child.textual_declaration.text
                        if feature_sentence in text.encode('utf-8'):
                            print("在内容中发现特征声明语句: '%s'" % feature_sentence)
                            decision[abbr_mapping.get(name_spec)] += 1
                            continue
                        else:
                            print('已进入文件夹，正在查找')
                    elif type_dist.get(guid) is None:
                        info[guid] = child.get_name()
            else:
                print('此次检测没有特征语句，正在查找')


if __name__ == '__main__':
    info = {}
    print("sys.argv: ", len(sys.argv), " elements:")
    for arg in sys.argv:
        print(" - ", arg)
    decision_table = []
    if len(sys.argv) > 1:
        current_dir = sys.argv[1]

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
                system.exit(0)  # 正常退出
        print(len(valid_projects), 'projects found. Please confirm again!')

        for project in valid_projects:
            filename, _ = os.path.splitext(os.path.basename(project))  # 分离文件名和扩展

            decision = {'Series': os.path.relpath(project, current_dir), 'Model': filename, 'AutoHook': 0,
                        'AutoTele': 0,
                        'AntiSwing': 0}
            print("Opening:", '-' * 27)
            print("Opening:", os.path.relpath(project, current_dir))
            try:
                proj = projects.open(project, password=naive(filename, 100)[0])
                if proj:
                    detect()
                    print("Success!", '-' * 27)
                    proj.close()  # close open project if necessary
                decision_table.append(decision)
            except Exception as e:
                decision['Exception'] = str(e)  # 文件打不开或不可写入
                print('-' * 27, "Failed!  " * 3)

        print(len(decision_table), 'decisions detected. Please confirm again!')
    else:
        proj = projects.primary
        if proj:
            decision = {'AutoHook': 0, 'AutoTele': 0, 'AntiSwing': 0}
            detect()
            print(decision)

    if len(sys.argv) > 1:
        rows = []
        header = ['Model', 'AutoTele', 'AutoHook', 'AntiSwing', 'Series', 'Exception']
        for row in decision_table:
            if row.get('Exception'):
                row['AutoHook'] = -1
                row['AutoTele'] = -1
                row['AntiSwing'] = -1
            else:
                row['Exception'] = ''
            # rows.append(','.join(str(x) for x in row.values()))  # 注意：row.values() 的顺序在 Python 2.7 中不可靠，可能因环境不同而变化
            rows.append(','.join(str(row.get(k)) for k in header))  # 先缓存数据
        # 打开 CSV 文件并使用 utf-8 编码
        with codecs.open('decision.csv', 'w', encoding='utf-8') as f:
            f.write(','.join(header))
            f.write('\n')
            f.write('\n'.join(rows) + '\n')

    if info: system.write_message(Severity.FatalError, str(info))
