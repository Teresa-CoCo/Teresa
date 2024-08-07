import math


def convertBinaryToDecimal(n):
    decimalNumber = 0
    i = 0
    while n != 0:
        remainder = n % 10
        n //= 10
        decimalNumber += remainder * pow(2, i)
        i += 1
    return decimalNumber


def convertDecimalToBinary(n):
    binaryNumber = 0
    i = 1
    step = 1
    while n != 0:
        remainder = n % 2
        print(f"Step {step}: {n}/2, 余数 = {remainder}, 商 = {n // 2}")
        n //= 2
        binaryNumber += remainder * i
        i *= 10
        step += 1
    return binaryNumber


def twobit():
    print("欢迎使用十进制，二进制互转程序")
    choice = int(input("请输入您要使用的功能：1.二进制转十进制 2.十进制转二进制\n"))

    if choice == 1:
        n = int(input("输入一个二进制数: "))
        print(f"二进制数 {n} 转换为十进制为 {convertBinaryToDecimal(n)}")

    elif choice == 2:
        n = int(input("输入一个十进制数: "))
        print(f"十进制数 {n} 转换为二进制为 {convertDecimalToBinary(n)}")
