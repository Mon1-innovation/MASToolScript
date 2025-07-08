#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import TUtilLog
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import traceback
import zipfile
from tqdm import tqdm
import threading



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
    a = requests.get('https://api.github.com/rate_limit', verify=False)
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
        "https://api.github.com/repos/{}/{}/releases".format(own, rep), verify=False)
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
        "https://api.github.com/repos/{}/{}/releases".format(own, rep), verify=False)
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
        "https://api.github.com/repos/{}/{}/releases".format(own, rep), verify=False)
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
        "https://api.github.com/repos/{}/{}/releases".format(own, rep), verify=False)
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

import os
import requests
import traceback
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def single_thread_download(final_url, file_path, name, chunk_size=1024*1024):
    print("开始单线程普通下载...")
    with requests.get(final_url, stream=True, verify=False, allow_redirects=True) as response:
        if 'Content-Length' in response.headers:
            data_size = int(response.headers['Content-Length']) / 1024 / 1024
        else:
            data_size = None
        with open(file_path, 'wb') as f:
            for data in tqdm(
                iterable=response.iter_content(chunk_size),
                total=int(data_size + 1) if data_size else None,
                desc=name,
                unit='MB'
            ):
                f.write(data)
    print(f"单线程下载完成，文件已保存至: {file_path}")

def download(url, path, name, chunk_size=1024*1024, thread_count=8):
    if ENABLE_SPEED:
        if ("github.com" in url or "raw.githubusercontent.com" in url) and "0721play.top" not in url:
            url = "http://releases.0721play.top/" + url
    TUtilLog.debug("请求下载链接: '{}'".format(url))

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, name)
    failtime = 5

    while True:
        try:
            head_resp = requests.head(url, verify=False, allow_redirects=True)
            file_size = int(head_resp.headers.get('Content-Length', 0))
            accept_ranges = head_resp.headers.get('Accept-Ranges', '').lower()
            final_url = head_resp.url
            TUtilLog.debug(f"HEAD 响应头: {head_resp.headers}")
            TUtilLog.debug(f"最终跳转后的下载链接: {final_url}")

            if accept_ranges == 'bytes' and file_size > 0:
                print(f"服务器支持断点续传，尝试多线程下载（{thread_count}线程）")

                def download_chunk(start, end, idx):
                    headers = {'Range': f'bytes={start}-{end}'}
                    part_file = f"{file_path}.part{idx}"
                    with requests.get(final_url, headers=headers, stream=True, verify=False, timeout=30) as r:
                        if r.status_code != 206:
                            raise Exception(f"服务器未正确返回分段内容，状态码: {r.status_code}")
                        if 'Content-Range' not in r.headers:
                            raise Exception("服务器未返回 Content-Range，可能不支持分段下载")
                        with open(part_file, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                if chunk:
                                    f.write(chunk)

                try:
                    # 大小<1MB 直接单线程下载
                    if file_size < chunk_size:
                        print("文件小于最小分块大小，使用单线程下载...")
                        single_thread_download(final_url, file_path, name, chunk_size)
                        return
                    part_size = file_size // thread_count
                    ranges = [
                        (i * part_size, (i + 1) * part_size - 1 if i < thread_count - 1 else file_size - 1, i)
                        for i in range(thread_count)
                    ]

                    with ThreadPoolExecutor(max_workers=thread_count) as executor:
                        futures = {executor.submit(download_chunk, start, end, idx): idx for start, end, idx in ranges}

                        pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=name)
                        try:
                            while True:
                                downloaded = sum(
                                    os.path.getsize(f"{file_path}.part{i}") if os.path.exists(f"{file_path}.part{i}") else 0
                                    for i in range(thread_count)
                                )
                                pbar.n = downloaded
                                pbar.refresh()
                                if all(f.done() for f in futures):
                                    break
                        finally:
                            pbar.close()

                        for future in futures:
                            if future.exception():
                                raise future.exception()

                    # 合并
                    print("所有分段下载完成，开始合并文件...")
                    with open(file_path, 'wb') as outfile:
                        for i in range(thread_count):
                            part_file = f"{file_path}.part{i}"
                            with open(part_file, 'rb') as infile:
                                outfile.write(infile.read())
                            os.remove(part_file)
                    print(f"下载完成，文件已保存至: {file_path}")

                except Exception as e:
                    print(f"多线程下载失败: {e}\n自动切换到单线程普通下载...")
                    single_thread_download(final_url, file_path, name, chunk_size)

            else:
                # 直接单线程
                single_thread_download(final_url, file_path, name, chunk_size)

            break
        except Exception as e:
            print('出现异常! 自动重试中...')
            TUtilLog.warning("{}".format(traceback.format_exc()))
            failtime -= 1
            if failtime < 0:
                raise Exception("资源获取失败！请稍后再试！")
def tool_clear(ask = False):
    import shutil
    clear = False
    if ask:
        print("清除缓存？(Y/N，默认N)")
        a = input().lower()
        if a != 'y':
            clear = True

    try:
        if (ask and clear) or not ask:
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
            if file_name in ['CustomIconMac.icns', 'CustomIconWindows.ico', 'README.html']:
                shutil.move(file_name, os.path.join(
                    path + "/"))
                return True
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

def get_extra_file(data = None):
    # 下载额外内容仅在第一次安装时进行
    print_info("下载额外内容")
    if not data:
        try:
            a = requests.get("http://releases.0721play.top/" + 'https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/extra_file.json', verify=False)
        except:
            a = requests.get('http://sp2.0721play.icu/d/MAS/MAS-PC/extra_file.json', verify=False)    
            a = a.json()
    else:
        a = data
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

