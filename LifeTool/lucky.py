import random
import time
def lucky():
    print("欢迎使用幸运数\n快看看你的幸运数是多少！")
    time.sleep(1)
    random.seed(114514)
    randomnumber = random.randint(1, 9)
    print("生成好了，今天您的幸运数字是："+str(randomnumber))
    time.sleep(1)
    print("您需要判断您今天的运气吗?")
    choose = input("是/否")
    if choose == "是":
        luck()
        quit()
    else :
        quit()
def luck():
    randomnumber = random.randint(1, 10)
    if randomnumber == 1:
        print("大吉")
    if randomnumber == 2:
        print("中吉")
    if randomnumber == 3:
        print("小吉")
    if randomnumber == 4:
        print("吉")
    if randomnumber == 5:
        print("半吉")
    if randomnumber == 6:
        print("末吉")
    if randomnumber == 7:
        print("凶")
    if randomnumber == 8:
        print("半凶")
    if randomnumber == 9:
        print("小凶")
    if randomnumber == 10:
        print("大凶")