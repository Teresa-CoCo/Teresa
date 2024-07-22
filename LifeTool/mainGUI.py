import tkinter as tk
from tkinter import messagebox
import os

class TRSToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TRSTool Python版 Beta1")

        self.label_intro = tk.Label(root, text="欢迎使用TRSTool Python版 Beta1")
        self.label_intro.pack(pady=10)

        self.btn_bmi = tk.Button(root, text="BMI计算", command=self.open_bmi_calculator)
        self.btn_bmi.pack()

        self.btn_multimeter = tk.Button(root, text="万能表", command=self.open_multimeter)
        self.btn_multimeter.pack()

        self.btn_lucky = tk.Button(root, text="幸运与运势", command=self.open_lucky)
        self.btn_lucky.pack()

        self.btn_ping_tool = tk.Button(root, text="Ping网络工具", command=self.open_ping_tool)
        self.btn_ping_tool.pack()

        self.btn_length_converter = tk.Button(root, text="长度转换工具", command=self.open_length_converter)
        self.btn_length_converter.pack()

        self.btn_binary_converter = tk.Button(root, text="十进制二进制转换工具", command=self.open_binary_converter)
        self.btn_binary_converter.pack()

        self.btn_exit = tk.Button(root, text="退出", command=self.exit_program)
        self.btn_exit.pack(pady=20)

    def open_bmi_calculator(self):
        #必须相对于主main函数的目录
        from LifeTool import bmiGUI
        bmiGUI.GUI()

    def open_multimeter(self):
        from LifeTool import eletricGUI
        eletricGUI.GUI()

    def open_lucky(self):
        from LifeTool import luckyGUI
        luckyGUI.GUI()

    def open_ping_tool(self):
        from LifeTool import pingGUI
        pingGUI.GUI()

    def open_length_converter(self):
        from LifeTool import translongGUI
        translongGUI.GUI()

    def open_binary_converter(self):
        from LifeTool import twobitGUI
        twobitGUI.GUI()

    def exit_program(self):
        self.root.quit()

def GUI():
        # 创建主窗口
    root = tk.Tk()
    app = TRSToolGUI(root)
    root.mainloop()
