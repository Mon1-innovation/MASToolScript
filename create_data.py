#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
data = {}
# 基础文件
data['base_files'] = []
data['base_files'].append(
    (
        "ddlc.zip",
        "http://sp2.0721play.icu/d/MAS/DDLC/ddlc-win.zip"
    )
)
data['extra_files'] = []
    # 名称, 下载链接, 下载到相对路径, 额外操作
    # 额外操作：
    # 0. None - 不指定额外操作
    # 1. ASK_DOWNLOAD - 下载前进行询问，在旧版中会直接下载
    # 2. EXTRACT_EXTRA - 解压，并以扩展内容安装
    # 只在安装时下载
data['extra_files'].append(
    (
        "汉化说明.txt",
        r"https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/%E6%B1%89%E5%8C%96%E8%AF%B4%E6%98%8E.txt", 
        "./",
        None
    )
)
data['extra_files'].append(
    (
        "如何更新.txt",
        r"https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/%E5%A6%82%E4%BD%95%E6%9B%B4%E6%96%B0.txt", 
        "./",
        None
    )
)
data['extra_files'].append(
    (
        "sp_zhcn.zip",
        r"http://sp2.0721play.icu/d/MAS/MAS-PC/%E7%B2%BE%E7%81%B5%E5%8C%85%E6%B1%89%E5%8C%96.zip",
        "./cache",
        "EXTRACT_EXTRA"
    )
)


with open('extra_file.json', 'w', encoding = 'utf-8') as files:
    files.write(json.dumps(data))
