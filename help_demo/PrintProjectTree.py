# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import type_dist

# Prints out all branches in the currently open project.
print("--- Printing the tree of the project: ---")


def print_tree(branch, level=0, prefix=""):
    try:
        tp = type_dist[branch.type.ToString()]
    except KeyError:
        tp = 'unknown'

    # 选择合适的连接符
    connector = "└── " if level > 0 else ""  # 根节点
    if branch.is_device:
        deviceid = branch.get_device_identification()
        print(prefix + connector + branch.get_name(), ", device_id:", deviceid)
    else:
        print(prefix + connector + branch.get_name(), ", type:", tp)

    # 获取子节点
    children = branch.get_children(False)
    child_count = len(children)

    for i, child in enumerate(children):
        is_last = (i == child_count - 1) and child_count != 1  # 判断是否是最后一个子节点
        new_prefix = prefix + ("│%" if is_last else "│   ")
        print_tree(child, level + 1, new_prefix)


proj = projects.primary
assert (proj.is_root == True)
# We iterate over all top level objects and call the print_tree function for them.
for obj in proj.get_children():
    print_tree(obj)

print("--- Script finished. ---")
