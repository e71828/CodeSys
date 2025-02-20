#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import sys
import os


def naive(text, watershed=2000):
    if 'ZAT7000V8_5040D_V03防拆升级' in text:
        passwd = 'ZAT7000V863'
    elif 'Z125_CR720S' in text:
        passwd = 'ZAT8000V863'
    elif 'ZAT2500V753E_F501' in text:
        passwd = 'ZAT2500V753E'
    else:
        passwd = text.split('_')[0]
    # 从第4个字符开始（索引为3）查找数字到下一个字母之间的整数
    start_index = 3  # 从第4个字符开始
    # 找到第一个数字部分
    number_str = ""
    while start_index < len(passwd) and passwd[start_index].isdigit():
        number_str += passwd[start_index]
        start_index += 1
    category = int(number_str)
    if category <= watershed:  # 哪个吨位开始有密码，因为解压归档必须确定有无密码
        passwd = None
    else:
        passwd = passwd.lower()
    return passwd, category


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

    found = False  # 标志变量
    valid_projects = []  # 用于存储符合条件的文件名的列表
    if os.path.isdir(current_dir):
        for root, _, files in os.walk(current_dir):
            for file in files:
                if file.endswith(".projectarchive") and "E107" not in file and "工况簇" in file:  # 排除包含 "E107" 的文件
                    project_path = os.path.join(root, file)
                    valid_projects.append(project_path)  # 存入列表
                    print("Found:", os.path.relpath(project_path, current_dir))
                    found = True  # 设为 True，表示找到至少一个合格的文件

        # 如果没有找到任何符合条件的 .project 文件，则退出
        if not found:
            print("No valid project files found. Exiting...")
            sys.exit(0)  # 正常退出
    else:
        print("Path error!!")
        sys.exit(0)
    print(len(valid_projects), 'projects found. Please confirm again!')

    for project in valid_projects:
        filename, _ = os.path.splitext(os.path.basename(project))  # 分离文件名和扩展
        extracted_filepath = os.path.dirname(os.path.join(extract_to_path, os.path.relpath(project, current_dir)))
        if not os.path.exists(extracted_filepath):
            os.makedirs(extracted_filepath)
        print("Opening:", '-' * 27)
        print("Opening:", os.path.relpath(project, current_dir))
        proj = projects.open_archive(project, extracted_filepath, overwrite=True,
                                     encryption_password=naive(filename)[0])
        if proj:
            print("Success!", '-' * 27)
            proj.close()  # close open project if necessary
        else:
            print('-' * 27, "Open Failed!  " * 3)
