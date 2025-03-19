#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function
import sys
import os
import codecs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import type_dist
from load import implementation_intro, declaration_intro
from extract_archive import naive


def access_content(path):
    with codecs.open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        text = "\n".join(text.splitlines()) + ("\n" if text.endswith("\n") else "") # replacing "\r\n" or "\r" or with "\n"
        part1 = None
        part2 = None
        if path.endswith('.act'):
            part2 = text.replace(implementation_intro, '')
        elif path.endswith('.gvl'):
            part1 = text.replace(declaration_intro, '')
        elif path.endswith('.pou') or path.endswith('.meth'):
            index = text.find(implementation_intro)
            part2 = text[index:].replace(implementation_intro, '')
            part1 = text[:index].replace(declaration_intro, '')
        else:
             pass
    file_name, _ = os.path.splitext(os.path.basename(path))  # 分离文件名和扩展
    return file_name, part1, part2



def proof():
    # 直接查找文件夹
    res = [obj for obj in proj.find(pou_name, True) if not obj.is_folder]
    if res:
        pou = res[0]
        guid = pou.type.ToString()
        tp = type_dist.get(guid)
        if tp == 'pou' or tp == 'meth':
            pou.textual_implementation.replace(implementation)
            pou.textual_declaration.replace(declaration)
            decision['overwrite'] = 1
        elif tp == 'gvl':
            pou.textual_declaration.replace(declaration)
            decision['overwrite'] = 1
        elif tp == 'act':
            pou.textual_implementation.replace(implementation)
            decision['overwrite'] = 1
        elif not tp:
            system.write_message(Severity.FatalError, pou.get_name())
        else:
            pass


if __name__ == '__main__':
    print("sys.argv: ", len(sys.argv), " elements:")
    for arg in sys.argv:
        print(" - ", arg)
    decision_table = []

    if len(sys.argv) > 2:
        current_dir = sys.argv[1]
        pou_name, declaration, implementation = access_content(sys.argv[2])
        if not pou_name:
            system.exit(1)

        found = False  # 标志变量
        valid_projects = []  # 用于存储符合条件的文件名的列表
        if os.path.isdir(current_dir):
            for root, _, files in os.walk(current_dir):
                for file in files:
                    if file.endswith(".project") and "E107" not in file and "工况簇" in file:  # 排除包含 "E107" 的文件
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

            decision = {'Series': os.path.relpath(project, current_dir), 'Model': filename, 'overwrite': 0}
            print("Opening:", '-' * 27)
            print("Opening:", os.path.relpath(project, current_dir))
            try:
                proj = projects.open(project, password=naive(filename, 100)[0])
                if proj:
                    proof()
                    print("Success!", '-' * 27)
                    proj.save()
                    proj.close()  # close open project if necessary
                decision_table.append(decision)
            except Exception as e:
                decision['Exception'] = str(e)  # 文件打不开或不可写入
                print('-' * 27, "Failed!  " * 3)

        print(len(decision_table), 'decisions detected. Please confirm again!')
    else:
        proj = projects.primary
        if proj:
            decision = {'overwrite': 0}
            sel_path = system.ui.open_file_dialog("Choose multiple files:",
                                                  filter="CodeSys Structured Text files|*.pou;*.m;*.act;*.gvl|All files (*.*)|*.*",
                                                  filter_index=0, multiselect=False)
            pou_name, declaration, implementation = access_content(sel_path)
            if not pou_name:
                sys.exit(1)
            proof()
    if len(sys.argv) > 2:
        rows = []
        header = ['Model', 'overwrite', 'Series', 'Exception']
        for row in decision_table:
            if row.get('Exception'):
                row['overwrite'] = -1
            else:
                row['Exception'] = ''
            rows.append(','.join(str(row.get(k)) for k in header))  # 先缓存数据
        # 打开 CSV 文件并使用 utf-8 编码
        with codecs.open('decision.csv', 'w', encoding='utf-8') as f:
            f.write(','.join(header))
            f.write('\n')
            f.write('\n'.join(rows) + '\n')
