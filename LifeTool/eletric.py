def electric():
    print("欢迎使用万能表")
    print("请选择挡位：1.安培挡 2.电压挡 3. 欧姆挡")
    choose=input()
    if choose=="1":
        anpei()
    elif choose=="2":
        volt()
    elif choose=="3":
        omegacal()

def anpei():
    print("请输入电阻 电压")
    a=input()
    b=a.split()
    omega = float(b[0])
    volt = float(b[1])
    anpei=volt/omega
    print(str(anpei)+"安")
    exit()
def volt():
    print("请输入电阻 电流")
    a=input()
    b=a.split()
    omega = float(b[0])
    anpei = float(b[1])
    volt=anpei*omega
    print(str(volt)+"伏")
    exit()
def omegacal():
    print("请输入电流 电压")
    a=input()
    b=a.split()
    anpei = float(b[0])
    volt = float(b[1])
    omega=volt/anpei
    print(str(omega)+"欧")
    exit()