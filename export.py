#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import os
import shutil
import clr
from System import Environment

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import FolderBrowserDialog, DialogResult

declaration_intro = '%' + '-' * 75 + '%\n%->> Declaration\n' + '%' + '-' * 75 + '%\n'
implementation_intro = '%' + '-' * 75 + '%\n%->> Implementation\n' + '%' + '-' * 75 + '%\n'

'''
prop_method		= Guid('792f2eb6-721e-4e64-ba20-bc98351056db')
dut				= Guid('2db5746d-d284-4425-9f7f-2663a34b0ebc') # struct
libm			= Guid('adb5cb65-8e1d-4a00-b70a-375ea27582f3')
method_no_ret	= Guid('f89f7675-27f1-46b3-8abb-b7da8e774ffd')
act				= Guid('8ac092e5-3128-4e26-9e7e-11016c6684f2')
fb				= Guid('6f9dac99-8de1-4efc-8465-68ac443b7d08')
itf				= Guid('6654496c-404d-479a-aad2-8551054e5f1e')
folder			= Guid('738bea1e-99bb-4f04-90bb-a7a567e74e3a')
gvl				= Guid('ffbfa93a-b94d-45fc-a329-229860183b1d')
prop			= Guid('5a3b8626-d3e9-4f37-98b5-66420063d91e')
textlist		= Guid('2bef0454-1bd3-412a-ac2c-af0f31dbc40f')
global_textlist	= Guid('63784cbb-9ba0-45e6-9d69-babf3f040511')
Device			= Guid('225bfe47-7336-4dbc-9419-4105a7c831fa')
task_config		= Guid('ae1de277-a207-4a28-9efb-456c06bd52f3')
method			= Guid('f8a58466-d7f6-439f-bbb8-d4600e41d099')
gvl_Persistent	= Guid('261bd6e6-249c-4232-bb6f-84c2fbeef430')
Project_Settings	=Guid('8753fe6f-4a22-4320-8103-e553c4fc8e04')
Plc_Logic			=Guid('40b404f9-e5dc-42c6-907f-c89f4a517386')
Application			=Guid('639b491f-5557-464c-af91-1471bac9f549')
Task				=Guid('98a2708a-9b18-4f31-82ed-a1465b24fa2d')
Task_pou			=Guid('413e2a7d-adb1-4d2c-be29-6ae6e4fab820')
Visualization		=Guid('f18bec89-9fef-401d-9953-2f11739a6808')
Visualization_Manager=Guid('4d3fdb8f-ab50-4c35-9d3a-d4bb9bb9a628')
TargetVisualization	=Guid('bc63f5fa-d286-4786-994e-7b27e4f97bd5')
WebVisualization	=Guid('0fdbf158-1ae0-47d9-9269-cd84be308e9d')
__VisualizationStyle=Guid('8e687a04-7ca7-42d3-be06-fcbda676c5ef')
ImagePool			=Guid('bb0b9044-714e-4614-ad3e-33cbdf34d16b')
Project_Information	=Guid('085afe48-c5d8-4ea5-ab0d-b35701fa6009')
SoftMotion_General_Axis_Pool=Guid('e9159722-55bc-49e5-8034-fbd278ef718f')

'''

type_dist = {
    '792f2eb6-721e-4e64-ba20-bc98351056db': 'pm',  # property method
    '2db5746d-d284-4425-9f7f-2663a34b0ebc': 'dut',  # dut
    'adb5cb65-8e1d-4a00-b70a-375ea27582f3': 'lib',  # lib manager
    'f89f7675-27f1-46b3-8abb-b7da8e774ffd': 'm',  # method no ret
    '8ac092e5-3128-4e26-9e7e-11016c6684f2': 'act',  # action
    '6f9dac99-8de1-4efc-8465-68ac443b7d08': 'pou',  # pou
    '6654496c-404d-479a-aad2-8551054e5f1e': 'itf',  # interface
    '738bea1e-99bb-4f04-90bb-a7a567e74e3a': '',  # folder
    'ffbfa93a-b94d-45fc-a329-229860183b1d': 'gvl',  # global var
    '5a3b8626-d3e9-4f37-98b5-66420063d91e': 'prop',  # property
    '2bef0454-1bd3-412a-ac2c-af0f31dbc40f': 'tl',  # textlist
    '63784cbb-9ba0-45e6-9d69-babf3f040511': 'gtl',  # global textlist
    '225bfe47-7336-4dbc-9419-4105a7c831fa': 'dev',  # device
    'ae1de277-a207-4a28-9efb-456c06bd52f3': 'tc',  # task configuration
    'f8a58466-d7f6-439f-bbb8-d4600e41d099': 'm',  # method with ret
    '261bd6e6-249c-4232-bb6f-84c2fbeef430': 'gvl',  # gvl_Persistent
    '98a2708a-9b18-4f31-82ed-a1465b24fa2d': 'task',
    '413e2a7d-adb1-4d2c-be29-6ae6e4fab820': '',  # Task_pou
    '40b404f9-e5dc-42c6-907f-c89f4a517386': '',  # Plc Logic
    '639b491f-5557-464c-af91-1471bac9f549': '',  # Application
    'c3fc9989-e24b-4002-a2c7-827a0a2595f4': ''  # CheckDivLReal
}


def save(text, path, name, extension):
    if not extension:
        extension = ''
    else:
        extension = '.' + extension
    with open(os.path.join(path, name + extension), 'w') as f:
        f.write(text.encode('utf-8'))


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

        if treeobj.has_textual_implementation:
            content = content + implementation_intro
            a = treeobj.textual_implementation
            content = content + a.text

    children = treeobj.get_children(False)

    # 根据需要新建文件夹
    if children:
        if type_spec:
            cur_path = os.path.join(cur_path, name + '.' + type_spec)
        else:
            cur_path = os.path.join(cur_path, name)
        if name in folder_specify:
            verbose = True
            if not os.path.exists(cur_path):
                os.makedirs(cur_path)
        else:
            verbose = False

    if content and verbose:
        save(content, cur_path, name, type_spec)
        count = count + 1

    for child in children:
        print_tree(child, depth + 1, cur_path, verbose)


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
    selected_path = browse_directory_dialog("Choose a directory？ 简: 选择保存位置。   ", default_path)
    print("Nice, you choose: '%s'" % selected_path)
    list_dir = os.listdir(selected_path)
    if selected_path:
        if not [fd for fd in list_dir if not fd.startswith('.')]:
            return selected_path
        else:
            res = system.ui.prompt("'" + selected_path + " ', Not empty. ???  Delete ??? ", PromptChoice.YesNo,
                                   PromptResult.No)
            if res == PromptResult.Yes:
                # 非空文件夹 删除多余
                for f in list_dir:
                    if not f.startswith("."):  # 保留 svn,git 目录
                        sub_path = os.path.join(selected_path, f)
                        if os.path.isdir(sub_path):
                            shutil.rmtree(sub_path)
                        else:
                            os.remove(sub_path)
                    elif f == ".git":
                        has_repo = True
                return selected_path
            else:
                return selected_path
    else:
        return


if __name__ == '__main__':
    info = {}
    count = 0
    print("--- Saving files in the project: ---")
    print("Now we query a single line string: specified folder name")
    folder_specify = system.ui.query_string("Which folder to export?  简: 指定代码目录？英半角逗号分隔", text='cal_height_hook')
    print("Nice, I get the folder name: %s." % folder_specify)

    # 使用 split 分割字符串并去除空格
    if folder_specify:
        folder_specify = [part.strip() for part in folder_specify.split(',')]

    save_folder = search_folder()
    # print(save_folder)
    if save_folder:
        for obj in projects.primary.get_children():
            print_tree(obj, 0, save_folder)
        if not folder_specify:
            system.ui.info(' All {} codes are exported! '.format(count))
        else:
            system.ui.info(' Specified {} codes are exported! '.format(count))


        # with open(os.path.join(save_folder, 's.txt'), 'w') as f:
        #     f.write(str(info))
    else:
        system.ui.warning("   Just Aborted!  ")
        print("--- Script exit before saving files. ---")

    # if has_repo:
    #     os.chdir(save_folder)
    #     si = subprocess.STARTUPINFO()
    #     si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #     subprocess.call('"C:\\Program Files\\Git\\bin\\git.exe" add .', startupinfo=si)
    #     subprocess.call('"C:\\Program Files\\Git\\bin\\git.exe" commit -m "'+time.strftime('%Y-%m-%d %H:%M',
    #     time.localtime(time.time()))+'"', startupinfo=si)
    # else:
    #     os.chdir(save_folder)
    #     si = subprocess.STARTUPINFO()
    #     si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #     subprocess.call('"C:\\Program Files\\Git\\bin\\git.exe" init', startupinfo=si)#'cd '+ save_folder + "
    #     && " +
    #     'git init')
    #     subprocess.call('"C:\\Program Files\\Git\\bin\\git.exe" add .', startupinfo=si)
    #
    #     subprocess.call('"C:\\Program Files\\Git\\bin\\git.exe" commit -m "'+time.strftime('%Y-%m-%d %H:%M',
    #     time.localtime(time.time()))+'"', startupinfo=si)
