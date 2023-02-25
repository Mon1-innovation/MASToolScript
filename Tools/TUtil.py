#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import TUtilLog
import requests
import time
import traceback
import zipfile
from tqdm import tqdm



_install_completed = None
ENABLE_SPEED = False

def set_proxy(port):
    os.environ["http_proxy"] = "http://127.0.0.1:{}".format(port)
    os.environ["https_proxy"] = "https://127.0.0.1:{}".format(port)
    print_info("代理地址设置为: '{}'".format("127.0.0.1:{}".format(port)))
def un_zip(file_name):
    """
    解压文件
    """
    import zipfile
    TUtilLog.info("解压文件：'{}'".format(file_name))
    try:
        zip_file = zipfile.ZipFile(file_name)
    except Exception as e:
        TUtilLog.error("解压文件失败：'{}'".format(e))
        return False
    try:
        if os.path.isdir(file_name + "_files"):
            pass
        else:
            os.mkdir(file_name + "_files")
        for names in tqdm(zip_file.namelist(), "解压文件"):
            zip_file.extract(names, file_name + "_files/")
        zip_file.close()
        return True
    except Exception as e:
        TUtilLog.error("解压文件失败：'{}'".format(e))
        zip_file.close()
        return False


def get_github_rate_limit():
    a = requests.get('https://api.github.com/rate_limit')
    a = a.json()
    try:
        if a['resources']['core']['limit'] - a['resources']['core']['used'] < 1:
            print("您已经到达Github请求上限，请等待一段时间后重试。")
            TUtilLog.warning('您已经到达Github请求上限，请等待一段时间后重试。')
            return False
        elif a['resources']['core']['limit'] - a['resources']['core']['used'] < 5:
            print("!!您即将到达Github请求上限，本次安装可能会失败。!!")
            TUtilLog.warning('您即将到达Github请求上限，本次安装可能会失败。')
            
            return False
    except KeyError as e:
        TUtilLog.error("{}".format(traceback.format_exc(e)))


def get_latest_release_tag(own, rep):
    """
    获取仓库最新release的tag
    IN:
        own - 拥有者
        rep - 存储库名称
        filename - 下载的文件名称
    Return:
        tag 类似于"v0.12.1"
    """
    url = requests.get(
        "https://api.github.com/repos/{}/{}/releases".format(own, rep))
    url = url.json()
    try:
        return url[0]['tag_name']
    except Exception as e:
        print('遇到致命错误，请查看log获取详细信息')
        TUtilLog.error(e)
        return('版本号获取失败')

def check_update(oldver, own, rep):
    """
    从github检查是否有更新

    IN:
        oldver - 当前版本号['0', '12', '11']
        own - 拥有者
        rep - 存储库

    RETURNS:
        False - 无更新
        新版本号 - 返回版本号 v0.12.11.3
    """
    def comp_version(old, new):
        length = len(old)
        if length > len(new):
            length = len(new)
        for i in range(length):
            if old[i] < new[i]:
                return True
        
    url = requests.get(
        "https://api.github.com/repos/{}/{}/releases".format(own, rep))
    try:
        ver = url.json()[0]['tag_name']
        versp = ver[1:].split('.')
        if comp_version(oldver, versp):
            return ver
        return False
    except Exception as e:
        TUtilLog.error("检查更新时发生异常: {}".format(e))
        return False

def get_latest_release_info(own, rep):
    """
    获取仓库最新release的更新信息
    IN:
        own - 拥有者
        rep - 存储库名称
        filename - 下载的文件名称
    Return:
        md 源文件
    """
    url = requests.get(
        "https://api.github.com/repos/{}/{}/releases".format(own, rep))
    url = url.json()
    try:
        return url[0]['body']
    except Exception as e:
        TUtilLog.error(e)
        return "更新信息获取失败"


def get_latest_release_dl(own, rep):
    """
    获取仓库的最新release

    IN:
        own - 拥有者
        rep - 存储库名称
        filename - 下载的文件名称
    Return:
        (文件名, 下载链接)
    """
    url = requests.get(
        "https://api.github.com/repos/{}/{}/releases".format(own, rep))
    url = url.json()
    assets = url[0]['assets']
    result = []
    for items in assets:
        result.append((items['name'], items['browser_download_url']))
    return result


def is_exists(path):
    try:
        return os.path.exists(path)
    except Exception as e:
        TUtilLog.error("{}".format(traceback.format_exc(e)))
        return False


def mkdir(str):
    os.makedirs(str, exist_ok=True)

# https://blog.csdn.net/weixin_43347550/article/details/105248223


def download(url, path, name):
    TUtilLog.debug("request.get: '{}'".format(url))
    if not os.path.exists(path):   # 看是否有该文件夹，没有则创建文件夹
        os.mkdir(path)
    failtime=5
    while True:
        try:
            response = requests.get(url, stream=True)
            TUtilLog.debug(response.headers) # 打印查看基本头信息
            data_size=int(response.headers['Content-Length'])/1024/1024 # 字节/1024/1024=MB
            with open(os.path.join(path, name),'wb') as f:
                for data in tqdm(iterable=response.iter_content(1024*1024),total=int(data_size+1),desc=name,unit='MB'):
                    f.write(data)
            break
        except Exception as e:
            print('出现异常!自动重试中...')
            TUtilLog.warning("{}".format(traceback.format_exc(e)))
            failtime-=1
            if failtime<0:
                raise Exception("资源获取失败！请稍后再试！")
            continue


def tool_clear():
    import shutil
    try:
        print("清除缓存...")
        TUtilLog.info("清除缓存...")
        shutil.rmtree('./cache')
    except:
        TUtilLog.exception()
    finally:
        import os
        os._exit(0)

def print_info(message):
    print(message)
    TUtilLog.info(message)

def check_zip(path="./", targetdir = './'):
    dirs = os.listdir(path)

    for _file in tqdm(dirs, desc="安装内容"):
        if _file.find('.zip'):
            if un_zip(_file):
                pass
            else:
                print_info("精灵包文件处理失败")
                os.remove(path + _file)
                TUtilLog.error("\n处理出错的文件: '{}'\n".format(_file))
                continue
            dir_check(path + _file,  targetdir)


def dir_check(filedir, path):
    """
    精灵包文件检查流程
    IN:
        filedir - 检查的扩展包压缩包名（先调用解压函数完成后）
        path - MAS所在的文件夹，类似于renpy.config.basedir
    """
    path=path.replace('//', '/')
    subfile = os.listdir(filedir+"_files")
    for i in tqdm(subfile, desc="复制文件"):
        ifull = filedir + "_files" + "/" + i
        if copy_dir_m(i, ifull, path):
            # 处理成功
            continue
        else:
            # 处理名字不正常的文件
            # 进入文件夹后再遍历文件进行处理
            TUtilLog.info("进入文件夹 '{}' 处理内部文件".format(ifull))
            if not os.path.isdir(ifull):
                TUtilLog.info("不是文件夹 '{}' ".format(ifull))
                continue
            subi = os.listdir(ifull)
            for subifile in subi:
                subifile_full = ifull + "/" + subifile
                if copy_dir_m(subifile, subifile_full, path ):
                    continue
                else:
                    TUtilLog.info(
                        "2 - 进入文件夹 '{}' 处理内部文件".format(subifile_full))
                    if not os.path.isdir(subifile_full):
                        TUtilLog.info(
                            "不是文件夹 '{}' ".format(subifile_full))
                        continue
                    subi2 = os.listdir(subifile_full)
                    for subifile in subi2:
                        subifile_full2 = subifile_full + "/" + subifile
                        if copy_dir_m(subifile, subifile_full2, path):
                            continue
                        else:
                            TUtilLog.info(
                                "3 - 进入文件夹 '{}' 处理内部文件".format(subifile_full2))
                            if not os.path.isdir(subifile_full2):
                                TUtilLog.info(
                                    "不是文件夹 '{}' ".format(subifile_full2))
                                continue
                            subi3 = os.listdir(subifile_full2)
                            for subifile in subi3:
                                subifile_full3 = subifile_full2 + "/" + subifile
                                if copy_dir_m(subifile, subifile_full3, path):
                                    continue
                                else:
                                    TUtilLog.info(
                                        "4 - 进入文件夹 '{}' 处理内部文件".format(subifile_full3))
                                    if not os.path.isdir(subifile_full3):
                                        TUtilLog.info(
                                            "不是文件夹 '{}' ".format(subifile_full3))
                                        continue
                                    subi4 = os.listdir(
                                        subifile_full3)
                                    for subifile in subi4:
                                        subifile_full4 = subifile_full3 + "/" + subifile
                                        if copy_dir_m(subifile, subifile_full4, path):
                                            continue
                                        else:
                                            TUtilLog.info(
                                                "5 - 进入文件夹 '{}' 处理内部文件".format(subifile_full4))
                                            if not os.path.isdir(subifile_full4):
                                                TUtilLog.info(
                                                    "不是文件夹 '{}' ".format(subifile_full4))
                                                continue
                                            subi5 = os.listdir(
                                                subifile_full4)
                                            for subifile in subi5:
                                                subifile_full5 = subifile_full4 + "/" + subifile
                                                if copy_dir_m(subifile, subifile_full5, path):
                                                    continue
                                                else:
                                                    TUtilLog.info(
                                                        "6 - 进入文件夹 '{}' 处理内部文件".format(subifile_full5))
                                                    if not os.path.isdir(subifile_full5):
                                                        TUtilLog.info(
                                                            "不是文件夹 '{}' ".format(subifile_full5))
                                                        continue
                                                    subi6 = os.listdir(
                                                        subifile_full5)
                                                    for subifile in subi6:
                                                        subifile_full6 = subifile_full5 + "/" + subifile
                                                        if copy_dir_m(subifile, subifile_full6, path):
                                                            continue
                                                        else:
                                                            TUtilLog.warning(
                                                                "达到最深深度6，不再继续处理")
                                                            continue

def copy(src, tgp):
    shutil.copy(src, tgp)


def copy_dir(src_path, target_path):
    """
    复制文件 网上找的代码:))))))
    """
    global _install_completed
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copy_dir(path, path1)
            else:
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)
        _install_completed = True
        return True
    else:
        return False


def copy_dir_m(dirs, file_name, path):
    """
    处理文件夹
    in:
        dirs - 文件夹,短名
        file_name - 文件夹绝对路径
        path - 根目录
    """
    TUtilLog.info("准备复制文件：'{}'".format(dirs))
    # bak_file_name =
    # if inseconddir == False:
    # files = os.listdir(file_name)
    # for dirs in files:
    if dirs == 'game':
        check_json(file_name + "/mod_assets", path)
        copy_dir(file_name, path + "/game")
        return True
    elif dirs == 'lib':
        copy_dir(file_name, path + "/lib")
        return True
    elif dirs == 'log':
        copy_dir(file_name, path + "/log")
        return True
    elif dirs == 'piano_songs':
        copy_dir(file_name, path + "/piano_songs")
        return True
    elif dirs == 'custom_bgm':
        copy_dir(file_name, path + "/custom_bgm")
        return True
    elif dirs == 'characters':
        TUtilLog.info("忽略该文件夹: '{}'".format(dirs))
        return True  # 什么都不做, 我不希望做一个一键解锁精灵包的东西--至少要手动移动文件.
    elif dirs == 'gift':
        TUtilLog.info("忽略该文件夹: '{}'".format(dirs))
        return True  # 什么都不做, 我不希望做一个一键解锁精灵包的东西--至少要手动移动文件.
    elif dirs == 'gifts':
        TUtilLog.info("忽略该文件夹: '{}'".format(dirs))
        return True  # 什么都不做, 我不希望做一个一键解锁精灵包的东西--至少要手动移动文件.
    # game下文件夹
    elif dirs == 'Submods':
        copy_dir(file_name, path + "/game/Submods")
        return True
    elif dirs == 'mod_assets':
        check_json(file_name, path)
        copy_dir(file_name, path + "/game/mod_assets")
        return True
    elif dirs == 'python-packages':
        copy_dir(file_name, path + "/game/python-packages")
        return True
    elif dirs == 'gui':
        copy_dir(file_name, path + "/game/gui")
        return True
    else:
        if os.path.isfile(file_name):
            if file_name.find('rpy') != -1:  # 如果是rpy文件
                if not os.path.exists(path + "/game/Submods/UnGroupScripts"):
                    os.mkdir(path + "/game/Submods/UnGroupScripts")
                shutil.move(file_name, os.path.join(
                    path + "/game/Submods/UnGroupScripts"))
                TUtilLog.warning(
                    "这是个脚本文件，复制到 'Submods/UnGroupScripts'：{}".format(file_name))
                return True
    TUtilLog.info("不符合任何常规子模组应有的文件夹： '{}'".format(file_name))
    return False


def check_json(filename, path, movedir=None):
    import json
    """
    用于检查json并生成gift文件
    vars:
        filename - mod_assets文件夹
        movedir - 失败后删除的文件夹
        path - 根目录
    """
    TUtilLog.info("检测精灵包json文件：'{}'".format(filename))
    if not os.path.exists(filename + "/monika/j"):
        TUtilLog.info("未找到的json文件夹，跳过检测礼物：'{}'".format(filename))
        return
    filename = filename + "/monika/j"
    files = os.listdir(filename)
    for jsonfile in files:
        if jsonfile.find('json') != -1:
            try:
                json_file = filename + "/" + jsonfile
                json_data = open(json_file).read()
                output_json = json.loads(json_data)
            except:
                # move_files(movedir,False)
                
                TUtilLog.error("在尝试读取 '{}' 出现异常，跳过".format(json_file))
                continue
            try:
                giftname = output_json['giftname']
                try:
                    gtype = "/" + output_json['select_info']['group'] + "/"
                except:
                    TUtilLog.warning(
                        "在尝试获取的礼物分组时出现异常，使用空分组： '{}' ".format(json_file))
                    gtype = "/"
                try:
                    if not os.path.exists(path + '/AvailableGift'):
                        os.mkdir(path + '/AvailableGift')
                    if not os.path.exists(path + '/AvailableGift' + gtype):
                        os.mkdir(path + '/AvailableGift' + gtype)
                    giftfile = open(path + '/AvailableGift' +
                                    gtype + giftname + '.gift', 'w')
                    giftfile.close()
                    TUtilLog.info("生成了礼物文件：'{}'".format(
                        'AvailableGift' + gtype + giftname + '.gift'))
                except Exception as e:
                    TUtilLog.error('生成礼物文件出现异常！{}'.format(e))
            except:
                TUtilLog.warning(
                    "在尝试获取礼物文件名时出现异常，可能未设置giftname，跳过该文件：'{}'".format(json_file))
                continue

def get_extra_file():
    # 下载额外内容仅在第一次安装时进行
    print_info("下载额外内容")
    try:
        a = requests.get('https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/extra_file.json')
    except:
        a = requests.get('http://sp2.0721play.icu/d/MAS/MAS-PC/extra_file.json')    
    a = a.json()
    for file in tqdm(a["extra_files"], desc="额外内容"):
        if file[3] == "EXTRACT_EXTRA":
            download(file[1], file[2], file[0])
            un_zip(file[2] + "/" + file[0])
            dir_check(file[2] + "/" + file[0], path = "./CACHE" + '/ddlc.zip_files/DDLC-1.1.1-pc')
        elif file[3] == "ASK_DOWNLOAD":
            print_info("是否下载{}, 默认为N".format(file[1]))
            print_info(file[5])
            a = input().lower()
            if a != 'y':
                print_info("取消下载")
            else:
                download(file[1], file[2], file[0])
        else:
            download(file[1], file[2], file[0])

