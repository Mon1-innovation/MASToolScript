#!/usr/bin/env python
#-*- coding: utf-8 -*-

import TUtilLog

def get_tl(str):
    try:
        return TARGET_LANG[str]
    except KeyError:
        TUtilLog.warning("缺失翻译：{}".format(str))
        return str
en = {
    "选择语言/Select Language": "",
    "1 - 简体中文 (Default)": "",
    "MAS 已经安装": "",
    "未安装 MAS": ""
}

zhCN = {}

TARGET_LANG = None