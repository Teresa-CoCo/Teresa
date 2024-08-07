import os
ghostname = ("google.com")
lhostname=("baidu.com")
def ping():
    print("欢迎使用ping工具，请问您是需要ping国外还是ping国内？")
    choose = input("1.国外 2.国内")
    if choose == "1":
        response = os.system("ping  " + ghostname)
    if choose == "2":
        response = os.system("ping  " + lhostname)

    check(response)
def check(response):
    if response == 0:
        pingstatus = "网络有效"
    else:
        pingstatus = "网络无效"