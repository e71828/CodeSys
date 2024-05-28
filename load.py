#!/bin/env python3
# encoding:utf-8
from __future__ import print_function
import os
import shutil
import clr
from System import Environment

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import FolderBrowserDialog, DialogResult


def check(func):
    def wrapper(proj, path, name):  # 指定宇宙无敌参数
        # call func
        func(proj, path, name)
        # check
        found = proj.find(name, False)
        assert (found is not None and len(found) == 1, 'No object with the name {0} found '.format(name))
        item = found[0]
        return item

    return wrapper  # 返回


def insert_text(proj, path, name):
    with open(path, 'r') as f:
        text = f.read()
        index = text.find('(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n')
        if index >= 0:
            t1 = text[index:].replace('(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n', '')
            proj.textual_implementation.replace(t1)
            try:
                t1 = text[:index].replace('(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n', '')
                proj.textual_declaration.replace(t1)
            except:
                pass
        else:
            t1 = text.replace('(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n', '')
            proj.textual_declaration.replace(t1)


def create_taskconfig(proj, path, name):
    proj = proj.create_task_configuration()
    return proj


def create_task(proj, path, name):
    proj.import_native(path)


@check
def create_dev(proj, path, name):
    with open(path, 'r') as f:
        type = int(f.readline().split("=")[1].strip())
        id = f.readline().split("=")[1].strip()
        ver = f.readline().split("=")[1].strip()
    devId = device_repository.create_device_identification(type, id, ver)
    devDesc = device_repository.get_device(devId)
    if devDesc is None:
        raise Exception('No WinV3 PLC available in device repo')
    proj.add(name, devId)


@check
def create_pou(proj, path, name):
    proj.create_pou(name, PouType.Program)


@check
def create_gvl(proj, path, name):
    proj.create_gvl(name)


@check
def create_property(proj, path, name):
    proj.create_property(name)


def create_method(proj, path, name):
    proj = proj.create_method(name)
    return proj


def create_act(proj, path, name):
    try:
        proj = proj.create_action(name)
    except:
        pass
    return proj


@check
def create_folder(proj, path, name):
    proj.create_folder(name)


@check
def create_fb(proj, path, name):
    proj.create_pou(name, PouType.FunctionBlock)


@check
def create_function(proj, path, name):
    proj.create_pou(name, PouType.Function)


@check
def create_itf(proj, path, name):
    proj.create_interface(name)


def create_dut(proj, path, name):
    item = proj.create_dut(name, DutType.Union)
    return item


def add_library(proj, path, name):
    proj.import_native(path)


def add_textlist(proj, path, name):
    try:
        proj = proj.find(name, False)[0]
    except ValueError:
        proj = proj.create_textlist()
    try:
        proj.importfile(path)
        # avoid error: This object is already in use.
    except Exception as error:
        print("An error occurred: {}".format(error))
        pass


@check
def add_prop_method(proj, path, name):
    pass


def walk_folder(proj, path, depth=0):
    for f_name in os.listdir(path):
        sub_path = os.path.join(path, f_name)
        is_folder = os.path.isdir(sub_path)
        try:
            name, f_ext = f_name.split('.')  # File extension
        except ValueError:
            name = f_name
            f_ext = ''

        if depth == 0:
            print('main device: {}'.format(name))
            try:
                dev_proj = proj.find(name, False)[0]
            except ValueError:
                return False
            logic_path = os.path.join(sub_path, 'Plc Logic')  # Corrected the path construction
            sub_proj = dev_proj.find('Plc Logic', False)[0]
            sub_path = os.path.join(logic_path, 'Application')  # Corrected the path construction
            sub_proj = sub_proj.find('Application', False)[0]
            walk_folder(sub_proj, sub_path, depth + 3)
        else:
            print('current project directory:    ', proj.get_name())
            if is_folder:
                print('input folder: {}{}'.format(' ' * 4, name))
                if f_ext == 'tc':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_taskconfig(proj, sub_path, name)
                    walk_folder(sub_proj, sub_path, depth + 1)
                elif f_ext == '':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_folder(proj, sub_path, name)
                    walk_folder(sub_proj, sub_path, depth + 1)
                else:
                    pass
            else:
                print('input file: {}{}.{}'.format(' ' * 40, name, f_ext))
                if f_ext == 'pou':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_pou(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'itf':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_itf(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'gvl':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_gvl(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'prop':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_property(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'pm':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = add_prop_method(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'm':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_method(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'act':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_act(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'dut':
                    try:
                        sub_proj = proj.find(name, False)[0]
                    except ValueError:
                        sub_proj = create_dut(proj, sub_path, name)
                    insert_text(sub_proj, sub_path, name)
                elif f_ext == 'task':
                    create_task(proj, sub_path, name)
                elif f_ext == 'lib':
                    add_library(proj, sub_path, name)
                elif f_ext == 'tl':
                    add_textlist(proj, sub_path, name)
                elif f_ext == 'gtl':
                    add_textlist(proj, sub_path, name)
                else:
                    pass
    return True


def search_folder():
    # 获取 MyDocuments 路径
    root = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)
    # 目标路径 CsysL
    default_path = os.path.join(root, 'CsysL')
    if not os.path.exists(default_path): default_path = os.path.join(root)

    def browse_directory_dialog(description, selected_path):
        dialog = FolderBrowserDialog()
        dialog.Description = description
        dialog.SelectedPath = selected_path  # 设置默认路径
        dialog.ShowNewFolderButton = True

        if dialog.ShowDialog() == DialogResult.OK:
            return dialog.SelectedPath
        return None

    has_repo = False  # git
    # 使用 browse_directory_dialog 函数
    selected_path = browse_directory_dialog("Choose a directory？ 简: 选择源代码位置。   ", default_path)
    print("Nice, you choose: '%s'" % selected_path)
    return selected_path

if __name__ == '__main__':
    source_folder = search_folder()
    if source_folder:
        status = walk_folder(projects.primary, source_folder)
        if status:
            system.ui.info(" All codes are loaded! ")
        else:
            system.ui.warning(" Something went wrong! ")
