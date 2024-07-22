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
            try:
                binary_number = int(input_value)
                decimal_number = self.convert_binary_to_decimal(binary_number)
                messagebox.showinfo("转换结果", f"二进制数 {binary_number} 转换为十进制为 {decimal_number}")
            except ValueError:
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

    def convert_binary_to_decimal(self, n):
        decimal_number = 0
        i = 0
        while n != 0:
            remainder = n % 10
            n //= 10
            decimal_number += remainder * pow(2, i)
            i += 1
        return decimal_number

    def convert_decimal_to_binary(self, n):
        binary_number = 0
        i = 1
        while n != 0:
            remainder = n % 2
            n //= 2
            binary_number += remainder * i
            i *= 10
        return binary_number

def GUI():
        # 创建主窗口
    root = tk.Tk()
    app = BinaryDecimalConverterGUI(root)
    root.mainloop()
