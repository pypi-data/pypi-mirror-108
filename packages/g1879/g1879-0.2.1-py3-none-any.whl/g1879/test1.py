#!/usr/bin/env python
# -*- coding:utf-8 -*-
def auto_import(module: str, install_name: str = None):
    try:
        exec(f'import {module}')

    except ModuleNotFoundError:
        import os
        install_str = install_name or module
        os.system(f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {install_str}')
