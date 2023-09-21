import TUtilLog, TUtil, time
if __name__ == '__main__':
    try:
        import MASToolKit
        print("--按下回车后退出--")
        input()
        TUtil.tool_clear()

    except Exception as e:
        TUtil.print_info("=========================================")
        TUtil.print_info('发生异常，MASTookKit即将退出...')
        TUtil.print_info('查看MASToolKit.log获取详细信息...')
        TUtil.print_info("=========================================")
        TUtil.print_info("异常原因：{}".format(e))
        TUtilLog.exception() 
        
        print("--按下回车后退出--")
        input()
        TUtil.tool_clear()
        
        #pyinstaller -F .\Tools\MasInstaller.py