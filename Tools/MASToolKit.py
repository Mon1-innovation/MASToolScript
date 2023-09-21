#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pickle import TRUE
import sys, time
from tkinter import N
import traceback, requests, tqdm
import TUtil
import TUtilLog
from TUtilLog import info, debug, warning, error
import TTranslation
import TLogo
DOWNLOAD_DDLC_URL = None
PATH = '.'#sys.path[0]
CACHE_PATH = PATH + "/cache"
GAME_PATH = PATH + "/game"
MAS_OWN = "Mon1-innovation"#"Monika-After-Story"
MAS_REP = "MonikaModDev-zhCN"

MON1_REP = "MAS-Simplified-Chinese-Patch"
MON1_OWN = "Mon1-innovation"

debug('文件路径: {}'.format(PATH))
TLogo.moyu()
def print_info(str):
    print(str)
    TUtilLog.info(str)

TUtil.mkdir('./CACHE')

mas_installed = TUtil.is_exists(PATH + "/game/masrun")
FileData = None
#print("选择语言/Select Language")
#print("")
#print("1 - 简体中文 (Default)")
#print("2 - English")
#
import requests

def check_link_access(link):
    try:
        response = requests.head(link)
        if response.status_code in [200, 301, 302]:
            return True
        else:
            return False
    except Exception as e:
        error(e.__str__())
        return False
def get_base_file():
    global DOWNLOAD_DDLC_URL
    global FileData
    # 获取基础文件信息
    print_info("获取基础文件信息")
    try:
        FileData = requests.get("http://releases.0721play.top/" + 'https://raw.githubusercontent.com/Mon1-innovation/MAS-Simplified-Chinese-Patch/main/extra_file.json')
    except Exception as e:
        error(e)
        FileData = requests.get('http://sp2.0721play.icu/d/MAS/MAS-PC/extra_file.json')
    FileData = FileData.json()
    for file in tqdm.tqdm(FileData["base_files"], desc="基础文件"):
        if DOWNLOAD_DDLC_URL != None:
            continue
        if file[0] == "ddlc.zip":
            if (check_link_access(file[1])):
                DOWNLOAD_DDLC_URL = file[1]
                print_info("设置DDLC链接为：{}".format(file[1]))
                continue
            else:
                print_info("访问失败, 正在尝试更换备用链接")
    if DOWNLOAD_DDLC_URL == None:
        raise Exception("所有DDLC链接全部尝试失败, 无法进行安装!")
#print_info("是否启用github release加速")
#print_info("然而如果你没有梯子，加速效果依然不明显，白花我9块钱, 只不过从连不上变成能连上而已")
#print_info("Y（默认）/N")
#a = input()
TUtil.ENABLE_SPEED = True
if TUtil.ENABLE_SPEED:
    print_info("启用基于Cloudflare Workers的github开源项目hunshcn/gh-proxy进行加速")

def tool_box():
    def cn_update():
        print_info('准备下载汉化补丁')
        print_info("汉化补丁当前版本：{}".format(TUtil.get_latest_release_tag(MON1_OWN, MON1_REP)))
        print_info('==========================================')
        print_info('更新说明：\n\n' + TUtil.get_latest_release_info(MON1_OWN, MON1_REP))
        print_info('==========================================')
        time.sleep(2)
        url = TUtil.get_latest_release_dl(MON1_OWN, MON1_REP)

        debug(url)
        for name, dl in url:
            if name == "chs.rpa":
                print_info('准备下载chs.rpa...')
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, GAME_PATH, 'chs.rpa')
                except Exception as e:
                    error("下载失败：\n{}".format(e))
                    print("下载失败，准备重试...")
                    print("从github下载可能需要加速器...")
                    try:
                        if TUtil.ENABLE_SPEED:
                            dl = "http://releases.0721play.top/"+dl
                        TUtil.download(dl, GAME_PATH, 'chs.rpa')
                    except Exception as e:
                        print("下载失败，查看MASToolKit.log获取更多信息")
                        raise e
            if name == 'chs_gui.rpa':
                print_info('准备下载chs_gui.rpa...')
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, GAME_PATH, 'chs_gui.rpa')
                except Exception as e:
                    error("下载失败：\n{}".format(e))
                    print("下载失败，准备重试...")
                    print("从github下载可能需要加速器...")
                    try:
                        if TUtil.ENABLE_SPEED:
                            dl = "http://releases.0721play.top/"+dl
                        TUtil.download(dl, GAME_PATH, 'chs_gui.rpa')
                    except Exception as e:
                        print("下载失败，查看MASToolKit.log获取更多信息")
                        raise 
    print("===============================")
    print_info("请选择功能")
    print_info("1. 重装最新版汉化")
    print_info("2. 安装扩展内容（未实现）")
    print_info("3. 退出（默认）")
    a = input()
    if a == '1':
        cn_update()
    elif a == '2':
        pass
    else:
        pass



language = None#input()
if language != '2':
    TTranslation.TARGET_LANG = TTranslation.zhCN
else:
    TTranslation.TARGET_LANG = TTranslation.en
_ = TTranslation.get_tl

if mas_installed:
    info(_("MAS 已经安装"))
    print(_("MAS 已经安装"))
    #print("删除masrun文件即可让本程序覆盖重装")
    tool_box()
else:
    try:
        TUtil.get_github_rate_limit()
    except:
        pass
    info(_("未安装 MAS"))
    print(_("未安装 MAS"))
    print(_("准备安装MAS..."))
    print("获取DDLC下载链接...")
    get_base_file()
    info("开始下载DDLC: {}".format(CACHE_PATH))
    TUtil.download(DOWNLOAD_DDLC_URL, CACHE_PATH, 'ddlc.zip')
    print('开始下载MAS最新版本')
    info("开始下载MAS最新版本")
    masver1 = TUtil.get_latest_release_tag(MAS_OWN, MAS_REP)
    print_info("MAS最新版本为：" + masver1)
    info('==========================================')
    info('Monika After Story '+ masver1 +' 更新内容：\n\n')
    info('\n'+TUtil.get_latest_release_info(MAS_OWN, MAS_REP))
    info('\n\n')
    info('==========================================')
    print_info('更新内容已经保存至log文件中')
    print_info('获取下载链接...')
    url = TUtil.get_latest_release_dl(MAS_OWN, MAS_REP)
    debug(url)
    for name, dl in url:
        if name == "Monika_After_Story-{}-Mod.zip".format(masver1[1:]):
            print_info('准备下载MAS...')
            try:
                if TUtil.ENABLE_SPEED:
                    dl = "http://releases.0721play.top/"+dl
                TUtil.download(dl, CACHE_PATH, 'mas.zip')
            except Exception as e:
                error("下载失败：\n{}".format(e))
                print("下载失败，准备重试...")
                print("从github下载可能需要加速器...")
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, CACHE_PATH, 'mas.zip')
                except Exception as e:
                    print("下载失败，查看MASToolKit.log获取更多信息")
                    error("下载失败：\n{}".format(e))
                    TUtil.tool_clear()
        if name == 'spritepacks.zip':
            print('是否下载官方精灵包?（未汉化）')
            print('不下载则需要手动安装精灵包')
            print("Y(默认)/N")
            spdl = input()
            if spdl.lower() == 'n':
                print_info('跳过精灵包下载')
                spdl = False
                continue
            try:
                print_info('准备下载精灵包')
                if TUtil.ENABLE_SPEED:
                    dl = "http://releases.0721play.top/"+dl
                TUtil.download(dl, CACHE_PATH, 'spritepacks.zip')
            except Exception as e:
                error("下载失败：\n{}".format(e))
                print("下载失败，准备重试...")
                print("从github下载可能需要加速器...")
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, CACHE_PATH, 'spritepacks.zip')
                except Exception as e:
                    print("下载失败，查看MASToolKit.log获取更多信息")
                    error("下载失败：\n{}".format(e))
                    TUtilLog.warning("{}".format(traceback.format_exc(e)))
                    print_info('跳过精灵包下载')
                    break
    print_info('准备下载汉化补丁')
    print_info("汉化补丁当前版本：{}".format(TUtil.get_latest_release_tag(MON1_OWN, MON1_REP)))
    print_info('==========================================')
    print_info('更新说明：\n\n' + TUtil.get_latest_release_info(MON1_OWN, MON1_REP))
    print_info('==========================================')
    time.sleep(2)
    url = TUtil.get_latest_release_dl(MON1_OWN, MON1_REP)
    debug(url)
    for name, dl in url:
        if name == "chs.rpa":
            print_info('准备下载chs.rpa...')
            try:
                if TUtil.ENABLE_SPEED:
                    dl = "http://releases.0721play.top/"+dl
                TUtil.download(dl, CACHE_PATH, 'chs.rpa')
            except Exception as e:
                error("下载失败：\n{}".format(e))
                print("下载失败，准备重试...")
                print("从github下载可能需要加速器...")
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, CACHE_PATH, 'chs.rpa')
                except Exception as e:
                    TUtilLog.warning("{}".format(traceback.format_exc(e)))
                    print("下载失败，查看MASToolKit.log获取更多信息")
                    raise e
        if name == 'chs_gui.rpa':
            print_info('准备下载chs_gui.rpa...')
            try:
                if TUtil.ENABLE_SPEED:
                    dl = "http://releases.0721play.top/"+dl
                TUtil.download(dl, CACHE_PATH, 'chs_gui.rpa')
            except Exception as e:
                error("下载失败：\n{}".format(e))
                print("下载失败，准备重试...")
                print("从github下载可能需要加速器...")
                try:
                    if TUtil.ENABLE_SPEED:
                        dl = "http://releases.0721play.top/"+dl
                    TUtil.download(dl, CACHE_PATH, 'chs_gui.rpa')
                except Exception as e:
                    TUtilLog.warning("{}".format(traceback.format_exc(e)))
                    print("下载失败，查看MASToolKit.log获取更多信息")
                    raise 
  
    print_info('开始解压文件')
    print_info('解压ddlc')
    if TUtil.is_exists(CACHE_PATH + '/ddlc.zip'):
        TUtil.un_zip(CACHE_PATH + '/ddlc.zip')
    print_info('解压MAS')
    if TUtil.is_exists(CACHE_PATH + '/mas.zip'):
        TUtil.un_zip(CACHE_PATH + '/mas.zip')
    
    
    print_info('安装MAS...')
    #TUtil.copy_dir(CACHE_PATH + '/mas.zip_files', CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc')
    TUtil.dir_check(CACHE_PATH + '/mas.zip', CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc')
    print_info('安装MAS汉化补丁...')
    TUtil.copy(CACHE_PATH + '/chs.rpa', CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc/game')
    TUtil.copy(CACHE_PATH + '/chs_gui.rpa', CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc/game')
    if TUtil.is_exists(CACHE_PATH + '/spritepacks.zip'):
        TUtil.un_zip(CACHE_PATH + '/spritepacks.zip')
        print_info('安装精灵包...')
        TUtil.dir_check(CACHE_PATH + '/spritepacks.zip', CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc')
    try:
        TUtil.get_extra_file(FileData)
    except Exception as e:
        print_info("安装额外内容失败, 跳过")
        TUtilLog.warning("{}".format(traceback.format_exc(e)))
    print_info('移出缓存文件夹...')
    TUtil.copy_dir(CACHE_PATH + '/ddlc.zip_files/DDLC-1.1.1-pc', PATH)
    print_info('MAS安装完成~')
    print_info('ENJOY 你的莫妮卡~')
    print("======================================")