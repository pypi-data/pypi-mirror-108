# -*- coding:utf-8 -*-

import os
import shutil
import zipfile
from pathlib import Path

from files import get_valid_name


def unzip(zip_path: str, to_path: str, no_folder=None):
    乱码文件夹列表 = []  # 记录乱码的文件夹
    with zipfile.ZipFile(zip_path, 'r') as f:
        for fn in f.namelist():
            根目录 = Path(to_path)
            无乱码路径 = 根目录 / fn.encode("cp437").decode("gbk")
            解压路径 = Path(f.extract(fn, path=to_path))  # 解压并获取路径对象

            is_file = False if 解压路径.is_dir() else True
            if not is_file and 无乱码路径 != 解压路径:
                乱码文件夹列表.append(解压路径)

            路径 = 无乱码路径.parent / get_valid_name(无乱码路径.parent, 无乱码路径.name) if is_file else 无乱码路径
            解压路径.rename(路径)  # 重命名乱码文件

            if no_folder and is_file and 无乱码路径.parent != 根目录:
                # 移动文件到根目录
                文件名 = get_valid_name(根目录, 无乱码路径.name)
                无乱码路径.replace(根目录 / 文件名)

    for i in 根目录.iterdir():
        if i in 乱码文件夹列表 or no_folder:
            shutil.rmtree(str(i), ignore_errors=True)


def do_zip(源路径: str, 重命名: str = None, 包含文件夹: bool = False):
    目标 = Path(源路径).parent
    文件夹名 = Path(源路径).name
    起始 = 0 if 包含文件夹 else len(文件夹名)
    name = 文件夹名 if not 重命名 else 重命名
    文件名 = f'{str(目标 / name)}.zip'
    zipf = zipfile.ZipFile(文件名, 'w')
    pre_len = len(os.path.dirname(源路径))

    for 父路径, 文件夹s, 文件s in os.walk(源路径):
        for 文件 in 文件s:
            文件路径 = os.path.join(父路径, 文件)
            相对路径 = 文件路径[pre_len:].strip(os.path.sep)  # os.path.sep是路径分隔符，win是\
            zipf.write(文件路径, 相对路径[起始:])

    zipf.close()
    return 文件名


unzip(r"D:\tmp\test\test.zip", r'D:\tmp\test\新建文件夹', True)
