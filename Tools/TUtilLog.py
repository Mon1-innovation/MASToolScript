#!/usr/bin/env python
#-*- coding: utf-8 -*-

import platform
import logging
import time
import traceback, TLogo
logging.basicConfig(level=logging.DEBUG #设置日志输出格式
                    ,filename="./MASToolKit.log" #log日志输出的文件位置和文件名
                    ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                    ,format="%(asctime)s | %(levelname)s | %(message)s" #日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                    ,encoding='utf-8'
                    )
logging.info(
    """OS: {0} - {1} - {2}""".format(
        platform.system(),
        platform.release(),
        platform.version()
    )
)
logging.info("MASToolKit Version: " + TLogo.VER)

def debug(str):
    logging.debug("{}".format(str), )
def info(str):
    logging.info("{}".format(str))
def warning(str):
    logging.warning("{}".format(str))
def error(str):
    logging.error("{}".format(str))
def exception():
    #traceback.print_exc()
    logging.exception("\n" + traceback.format_exc())