import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class BinaryDecimalConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("十进制、二进制互转程序")

        self.label_intro = tk.Label(root, text="欢迎使用十进制、二进制互转程序")
        self.label_intro.pack(pady=10)

        self.btn_bin_to_dec = tk.Button(root, text="二进制转十进制", command=self.binary_to_decimal)
        self.btn_bin_to_dec.pack(pady=10)

        self.btn_dec_to_bin = tk.Button(root, text="十进制转二进制", command=self.decimal_to_binary)
        self.btn_dec_to_bin.pack(pady=10)

    def binary_to_decimal(self):
        input_value = self.get_input("请输入一个二进制数:")
        if input_value is not None:
            if self.is_valid_binary(input_value):
                binary_number = input_value  # 输入的二进制数（字符串）
                decimal_number = self.convert_binary_to_decimal(binary_number)
                messagebox.showinfo("转换结果", f"二进制数 {binary_number} 转换为十进制为 {decimal_number}")
            else:
                messagebox.showerror("错误", "请输入有效的二进制数")

    def decimal_to_binary(self):
        input_value = self.get_input("请输入一个十进制数:")
        if input_value is not None:
            try:
                decimal_number = int(input_value)
                binary_number = self.convert_decimal_to_binary(decimal_number)
                messagebox.showinfo("转换结果", f"十进制数 {decimal_number} 转换为二进制为 {binary_number}")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的十进制数")

    def get_input(self, prompt):
        return tk.simpledialog.askstring("输入", prompt)

    def is_valid_binary(self, s):
        return all(c in '01' for c in s)  # 检查字符串是否只包含 '0' 和 '1'

    def convert_binary_to_decimal(self, binary_number):
        decimal_number = 0
        power = len(binary_number) - 1
        for digit in binary_number:
            decimal_number += int(digit) * (2 ** power)
            power -= 1
        return decimal_number

    def convert_decimal_to_binary(self, n):
        return bin(n)[2:]  # 使用内置函数 bin() 将十进制数转换为二进制字符串，并去除前缀 '0b'

def GUI():
    # 创建主窗口
    root = tk.Tk()
    app = BinaryDecimalConverterGUI(root)
    root.mainloop()
