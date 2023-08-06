#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: Json file
'''
import os
import json


def get_from_json(filename: str, dirpath: str) -> dict:
    '''
    Summary: 从json文件中获得默认chem data
    NOTE : open 的 'r' 只读模式必须判断是否存在文件
    '''
    file = f'{filename}.json'
    json_path = os.path.join(dirpath, file)
    if not os.path.exists(json_path):
        print(f'{file} 不存在')
        return {}
    with open(json_path, 'r', encoding='utf-8') as f:
        st = f.read()
        if st:
            return json.loads(st)
        else:
            return {}


def save_to_json(data: dict, filename: str, dirpath: str):
    '''
    Summary: 将修改过的json内容保存到自定义的json文件
    NOTE : open 的 'w' 如果文件不存在会自己创建
    '''
    try:
        file = f'{filename}.json'
        js = json.dumps(data, ensure_ascii=False)  # 生成json str
        json_path = os.path.join(dirpath, file)
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(js)
    except Exception as e:
        print(e)
