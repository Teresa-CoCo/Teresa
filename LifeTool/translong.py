def translong():
    print("欢迎使用长度换算系统工具")
    print("请输入你要输入的单位：\n1.米  2.英尺  3.英寸  4.英里  5.码")

    chose = int(input())
    print("请输入你要换算的数字：")
    input_value = float(input())

    if chose == 1:
        meter = input_value
        foot = meter * 3.2808
        inch = meter * 39.370
        mile = meter / 1000 * 0.621
        yard = meter * 1.0936

        print(f"{meter}米={foot}英尺={inch}英寸={mile}英里={yard}码")

    elif chose == 2:
        foot = input_value
        meter = foot * 0.3048
        inch = meter * 39.370
        mile = meter / 1000 * 0.621
        yard = meter * 1.0936

        print(f"{meter}米={foot}英尺={inch}英寸={mile}英里={yard}码")

    elif chose == 3:
        inch = input_value
        meter = inch * 0.0254
        foot = meter * 3.2808
        mile = meter / 1000 * 0.621
        yard = meter * 1.0936

        print(f"{meter}米={foot}英尺={inch}英寸={mile}英里={yard}码")

    elif chose == 4:
        mile = input_value
        meter = mile * 1609.34
        foot = meter * 3.2808
        inch = meter * 39.370
        yard = meter * 1.0936

        print(f"{meter}米={foot}英尺={inch}英寸={mile}英里={yard}码")

    elif chose == 5:
        yard = input_value
        meter = yard * 0.9144
        foot = meter * 3.2808
        inch = meter * 39.370
        mile = meter / 1000 * 0.621

        print(f"{meter}米={foot}英尺={inch}英寸={mile}英里={yard}码")