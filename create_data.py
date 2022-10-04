import json


data = {}
data['extra_files'] = []
data['extra_files'].append(
    # 名称, 下载链接, 下载到相对路径, 额外操作
    # 额外操作：
    # 0. None - 不指定额外操作
    # 2. "EXTRACT_EXTRA" - 解压，并以扩展内容安装
    # 只在安装时下载
    ("汉化说明.txt", r"https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/%E6%B1%89%E5%8C%96%E8%AF%B4%E6%98%8E.txt", "./", None)
    )
data['extra_files'].append(
    ("sp_zhcn.zip", r"https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/sp_cn_0.12.9.zip", "./cache", "EXTRACT_EXTRA")
    )

with open('extra_file.json', 'w', encoding='utf-8') as files:
    files.write(json.dumps(data))