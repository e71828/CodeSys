import codecs
import os
import sys
import xml.etree.ElementTree as ET
from multiprocessing import Pool, Manager


def is_called_by_box(et_root, name='gongkuangzu'):
    # 遍历所有 Single 节点
    for parent in et_root.findall('.//Single[@Type="{d9a99d73-b633-47db-b876-a752acb25871}"]'):
        # 查找 Name="BoxType" 的子节点
        box_type = parent.find('.//Single[@Name="BoxType"]')
        out_commented = parent.find('Single[@Name="OutCommented"]')
        # 判断是否符合条件
        if box_type is not None and box_type.text == name and out_commented is not None:
            if out_commented.text == 'False':
                print("%s is called" % name)
            else:
                print("%s is commented" % name)
            return out_commented.text == 'False'
    print("%s is not called by box" % name)
    return False


def deal_detect(project, root_dir):
    filename, _ = os.path.splitext(os.path.basename(project))  # 分离文件名和扩展
    decision = {'Series': os.path.relpath(project, root_dir), 'Model': filename, 'AutoHook': 0,
                'AutoTele': 0,
                'AntiSwing': 0}
    # print("Opening:", '-' * 27)
    # print("Opening:", os.path.relpath(project, root_dir))
    try:
        is_called_by_box(ET.parse(project).getroot())
        # print("Success!", '-' * 27)
    except Exception as e:
        decision['Exception'] = str(e)  # 文件打不开或不可写入
        # print('-' * 27, "Failed!  " * 3)
    finally:
        return decision


def collect_result(result, result_list):
    # 回调函数，将结果添加到共享列表
    result_list.append(result)


if __name__ == '__main__':
    print("sys.argv: ", len(sys.argv), " elements:")
    for arg in sys.argv:
        print(" - ", arg)
    if len(sys.argv) == 2:
        native_exported_path = sys.argv[1]
        current_dir = native_exported_path

        found = False  # 标志变量
        valid_projects = []  # 用于存储符合条件的文件名的列表
        if os.path.isdir(current_dir):
            for root, _, files in os.walk(current_dir):
                for file in files:
                    if file.endswith(".export") and "E107" not in file and "5040" in file:  # 排除包含 "E107" 的文件
                        project_path = os.path.join(root, file)
                        valid_projects.append(project_path)  # 存入列表
                        print("Found:", os.path.relpath(project_path, current_dir))
                        found = True  # 设为 True，表示找到至少一个合格的文件

            # 如果没有找到任何符合条件的 .export 文件，则退出
            if not found:
                print("No valid project files found. Exiting...")
                sys.exit(0)  # 正常退出
        else:
            print("Path error!!")
            sys.exit(1)
        print(len(valid_projects), 'projects found. Please confirm again!')

        # 创建进程池和共享结果列表
        manager = Manager()
        decision_table = manager.list()  # 进程安全的列表
        p = Pool(8)
        # 为每个项目启动异步任务，并指定回调函数
        for proj in valid_projects:
            p.apply_async(deal_detect, args=(proj, current_dir), callback=lambda r: collect_result(r, decision_table))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')

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
            with codecs.open('seek3_decision.csv', 'w', encoding='utf-8') as f:
                f.write(','.join(header))
                f.write('\n')
                f.write('\n'.join(rows) + '\n')

    else:
        tree = ET.parse(r"C:\Users\admin\Documents\ZAT4000VS863-1_5040_V01_f.export")
        found = is_called_by_box(tree.getroot())
        tree = ET.parse(r"C:\Users\admin\Documents\ZAT4000VS863-1_5040_V01远程下载+工况簇_fa.export")
        is_called_by_box(tree.getroot())
