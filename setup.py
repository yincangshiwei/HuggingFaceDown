# -*- coding:utf-8 -*-
# @Time: 2025/1/22 0022 16:49
# @Author: cxd
# @File: pack_run.py
# @Remark:
# 在 setup.py 中定义
import os
from distutils.core import setup
import py2exe

options = {
    'py2exe': {
        'bundle_files': 1,  # 打包成一个文件
        'compressed': True,  # 压缩可执行文件
        'optimize': 2,
    }
}

# 找到所有静态文件
data_files = []
for root, dirs, files in os.walk('./resources'):
    for file in files:
        data_files.append((root, [os.path.join(root, file)]))

setup(
    options=options,
    windows=[{'script': 'main.py', 'dest_base': 'HuggingFaceDownApp'}],  # 如果是 GUI 程序，使用 windows 替换 console
    zipfile=None,  # 不创建独立的 zip 文件
    data_files=data_files  # 添加静态文件
)
