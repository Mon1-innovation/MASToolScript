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
    # 2. "EXTRACT_EXTRA" - 解压，并以扩展内容安装
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
        "sp_zhcn.zip",
        r"https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/sp_cn_0.12.9.zip",
        "./cache",
        "EXTRACT_EXTRA"
    )
)
data['extra_files'].append(
    (
        "zz_cardgames.rpy",
        r"http://sp2.0721play.icu/d/MAS/MAS-PC/zz_cardgames.rpy",
        "./cache/ddlc.zip_files/DDLC-1.1.1-pc/game",
        "ASK_DOWNLOAD",
        "因为历史原因，NOU小游戏的最新版未翻译，本文件会将汉化过的旧版本用于替换新版，游戏内会提示检测到rpy文件，保留即可"
    )
)

with open('extra_file.json', 'w', encoding = 'utf-8') as files:
    files.write(json.dumps(data))
