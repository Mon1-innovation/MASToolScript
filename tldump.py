#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 输出所有包括中文的行

import re, os
pattern = r'[\u4e00-\u9fa5]'
pattern2 =  re.compile(r'\"(.*?)\"')
INPUT_FILE = "Tools/".replace('\\', '/')
filelist = ['MASToolKit.py']#os.listdir(INPUT_FILE)


def find_exist(str, list):
    for i in list:
        if str == i:
            return True
    return False
def main(file):
    with open(INPUT_FILE + "/" + files, 'r', encoding='utf-8') as file:
        news = []
        lines = file.readlines()
        for pos, line in enumerate(lines):
            if re.search(pattern, line) is not None:
                result = pattern2.findall(line)
                for i in result:
                    if re.search(pattern, i) is None:
                        continue
                    if find_exist(i, news):
                        continue
                    
                    outbase.writelines('"{}":"{}",\n'.format(i, i))
                    news.append(i)

for files in filelist:
    outbase = open('{}'.format(files), 'w', encoding='utf-8')
    outbase.writelines('# file: {}\n'.format(INPUT_FILE + "/" + files))
    try:
        main(files)
    except Exception as e:
        print(e)
    outbase.close()