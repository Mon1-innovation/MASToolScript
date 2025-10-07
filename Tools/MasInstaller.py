import TUtilLog, TUtil, time
import argparse
import sys

def main(silent=False):
    try:
        # 导入MASToolKit时传入silent参数
        import MASToolKit
        MASToolKit.SILENT_MODE = silent

        if not silent:
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

        if not silent:
            print("--按下回车后退出--")
            input()

        TUtil.tool_clear(True)

if __name__ == '__main__':
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='MAS Tool Installer')
    parser.add_argument('--silent', action='store_true', help='运行时不需要用户输入')

    # 解析参数
    args = parser.parse_args()

    # 调用主函数，传入silent标志
    main(silent=args.silent)

    #pyinstaller -F .\Tools\MasInstaller.py