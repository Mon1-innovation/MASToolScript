import TUtil, os
VER = "0.0.4"
MOYU = R"""

          _____                   _______               _____                    _____
         /\    \                 /::\    \             |\    \                  /\    \
        /::\____\               /::::\    \            |:\____\                /::\____\
       /::::|   |              /::::::\    \           |::|   |               /:::/    /
      /:::::|   |             /::::::::\    \          |::|   |              /:::/    /
     /::::::|   |            /:::/~~\:::\    \         |::|   |             /:::/    /
    /:::/|::|   |           /:::/    \:::\    \        |::|   |            /:::/    /
   /:::/ |::|   |          /:::/    / \:::\    \       |::|   |           /:::/    /
  /:::/  |::|___|______   /:::/____/   \:::\____\      |::|___|______    /:::/    /      _____
 /:::/   |::::::::\    \ |:::|    |     |:::|    |     /::::::::\    \  /:::/____/      /\    \
/:::/    |:::::::::\____\|:::|____|     |:::|    |    /::::::::::\____\|:::|    /      /::\____\
\::/    / ~~~~~/:::/    / \:::\    \   /:::/    /    /:::/~~~~/~~      |:::|____\     /:::/    /
 \/____/      /:::/    /   \:::\    \ /:::/    /    /:::/    /          \:::\    \   /:::/    /
             /:::/    /     \:::\    /:::/    /    /:::/    /            \:::\    \ /:::/    /
            /:::/    /       \:::\__/:::/    /    /:::/    /              \:::\    /:::/    /
           /:::/    /         \::::::::/    /     \::/    /                \:::\__/:::/    /
          /:::/    /           \::::::/    /       \/____/                  \::::::::/    /
         /:::/    /             \::::/    /                                  \::::::/    /
        /:::/    /               \::/____/                                    \::::/    /
        \::/    /                 ~~                                           \::/____/
         \/____/                                                                ~~


----------------------------------------------------------------------------------------
欢迎使用 MASTookKit by Sir.P v{}
当提示选项时，输入对应的选项，然后按下回车键确定选项。
如果程序卡住，可以尝试点一下回车来继续。（通常这种情况发生时，标题栏会出现“选择”二字）
本程序一般不需要加速器，开启加速器可能会导致异常
----------------------------------------------------------------------------------------
Monika After Story本次安装的目标位置由本可执行文件所在的位置决定。
目标位置：{}
""".format(VER, os.path.abspath('.'))

QA = """
1. 异常 "ValueError: check_hostname requires server_hostname"

A: 关闭梯子


2. 异常中出现关键词 "[SSL: CERTIFICATE_VERIFY_FAILED]" "requests.exceptions.SSLError" 
完整：requests.exceptions.SSLError: HTTPSConnectionPool(host='api.github.com', port=443): Max retries exceeded with url: /repos/Mon1-innovation/MASToolScript/releases/latest (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)')))

A: 关闭Steam++ / Watt Toolkit / 梯子


3. 出现意义不明的异常

A: 发送MASToolKit.log到Discord/QQ/Github issue等地寻求帮助
Github issue：https://github.com/Mon1-innovation/MASToolScript/issues

"""

def moyu():
    print(MOYU)
    out_files()
    a = self_checkupdate()
    try:
        if a:
            print("MASToolKit有更新 -> {}".format(VER))
            print("====================================")
            print(TUtil.get_latest_release_info("Mon1-innovation", "MASToolScript"))
            print("你可以在 https://github.com/Mon1-innovation/MASToolScript/releases/latest 更新 MASToolKit")
    except:
        pass
        

def self_checkupdate():
    try:
        return TUtil.check_update(VER.split('.'), "Mon1-innovation", "MASToolScript")
    except:
        pass


def out_files():
    a = open("MASToolKit常见问题QA.txt", 'w', encoding='utf-8')
    a.write(QA)
    