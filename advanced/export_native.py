#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import os
import pickle
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract_archive import naive

if __name__ == '__main__':
    print("sys.argv: ", len(sys.argv), " elements:")
    for arg in sys.argv:
        print(" - ", arg)
    if len(sys.argv) > 2:
        current_dir = sys.argv[1]
        extract_to_path = sys.argv[2]
    else:
        current_dir = r''
        extract_to_path = r''
        sys.exit()

    decision_table = []
    checksum_table = []
    found = False  # 标志变量
    valid_projects = []  # 用于存储符合条件的文件名的列表
    if os.path.isdir(current_dir):
        for root, _, files in os.walk(current_dir):
            for file in files:
                if file.endswith(".project") and "E107" not in file and "5040" in file:  # 排除包含 "E107" 的文件
                    project_path = os.path.join(root, file)
                    valid_projects.append(project_path)  # 存入列表
                    print("Found:", os.path.relpath(project_path, current_dir))
                    found = True  # 设为 True，表示找到至少一个合格的文件

        # 如果没有找到任何符合条件的 .project 文件，则退出
        if not found:
            print("No valid project files found. Exiting...")
            system.exit(0)  # 正常退出
    else:
        print("Path error!!")
        system.exit(1)
    print(len(valid_projects), 'projects found. Please confirm again!')

    try:
        with open(os.path.expanduser(os.sep.join(["~", "My Documents", "project_checksum.pkl"])), 'r') as pkl_file:
            checksum_file = pickle.load(pkl_file)
    except:
        checksum_file = {}

    for project in valid_projects:
        filename, _ = os.path.splitext(os.path.basename(project))  # 分离文件名和扩展
        export_native_dir = os.path.dirname(os.path.join(extract_to_path, os.path.relpath(project, current_dir)))
        if not os.path.exists(export_native_dir):
            os.makedirs(export_native_dir)

        decision = {'Series': os.path.relpath(project, current_dir), 'Model': filename, 'exported': 0}
        if checksum_file.get(project) == os.path.getmtime(project):
            print("Skipping:", os.path.relpath(project, current_dir))
            continue
        checksum_file[project] = os.path.getmtime(project)
        print("Opening:", '-' * 27)
        print("Opening:", os.path.relpath(project, current_dir))
        try:
            proj = projects.open(project, password=naive(filename, 100)[0])
            if proj:
                treeobj = [obj for obj in proj.get_children() if obj.is_device]
                proj.export_native(treeobj, os.path.join(export_native_dir, filename + '.export'), recursive=True,
                                   one_file_per_subtree=False)
                decision['exported'] = 1
                print("Success!", '-' * 27)
                proj.close()  # close open project if necessary
        except Exception as e:
            print('-' * 27, "Failed!  " * 3)
            decision['Exception'] = str(e)  # 文件打不开或不可写入
            checksum_file[project] = -1
        finally:
            decision_table.append(decision)
    print(len(decision_table), 'decisions detected. Please confirm again!')

with open(os.path.expanduser(os.sep.join(["~", "My Documents", "project_checksum.pkl"])), 'w') as pkl_file:
    pickle.dump(checksum_file, pkl_file, -1)
