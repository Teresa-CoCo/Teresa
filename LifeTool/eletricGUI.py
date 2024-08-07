import tkinter as tk
from tkinter import messagebox

class ElectricMeterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("电子万用表")

        # 创建标签和输入框
        self.label_intro = tk.Label(root, text="请选择挡位：")
        self.label_intro.grid(row=0, column=0, padx=10, pady=10)

        self.choose_var = tk.StringVar()
        self.choose_var.set("1")  # 默认选择安培挡

        self.radio_anpei = tk.Radiobutton(root, text="安培挡", variable=self.choose_var, value="1")
        self.radio_anpei.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.radio_volt = tk.Radiobutton(root, text="电压挡", variable=self.choose_var, value="2")
        self.radio_volt.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.radio_omega = tk.Radiobutton(root, text="欧姆挡", variable=self.choose_var, value="3")
        self.radio_omega.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.label_input = tk.Label(root, text="请输入数据（用空格分隔）：")
        self.label_input.grid(row=4, column=0, padx=10, pady=10)

        self.entry_data = tk.Entry(root)
        self.entry_data.grid(row=5, column=0, padx=10, pady=5)

        self.btn_calculate = tk.Button(root, text="计算", command=self.calculate)
        self.btn_calculate.grid(row=6, column=0, padx=10, pady=10)

        # 添加输入提示标签
        self.label_anpei = tk.Label(root, text="输入格式：电阻 安培", fg="blue")
        self.label_anpei.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.label_volt = tk.Label(root, text="输入格式：电阻 电流", fg="blue")
        self.label_volt.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.label_omega = tk.Label(root, text="输入格式：电流 电压", fg="blue")
        self.label_omega.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

    def calculate(self):
        choose = self.choose_var.get()
        data = self.entry_data.get()

        try:
            b = data.split()
            if choose == "1":  # 安培挡
                if len(b) != 2:
                    raise ValueError("请输入正确的数据")
                omega = float(b[0])
                volt = float(b[1])
                result = volt / omega
                messagebox.showinfo("计算结果", f"安培挡计算结果：{result:.2f} 安")
            elif choose == "2":  # 电压挡
                if len(b) != 2:
                    raise ValueError("请输入正确的数据")
                omega = float(b[0])
                anpei = float(b[1])
                result = omega * anpei
                messagebox.showinfo("计算结果", f"电压挡计算结果：{result:.2f} 伏")
            elif choose == "3":  # 欧姆挡
                if len(b) != 2:
                    raise ValueError("请输入正确的数据")
                anpei = float(b[0])
                volt = float(b[1])
                result = volt / anpei
                messagebox.showinfo("计算结果", f"欧姆挡计算结果：{result:.2f} 欧")
        except ValueError as e:
            messagebox.showerror("错误", str(e))

def GUI():
    # 创建主窗口
    root = tk.Tk()
    app = ElectricMeterGUI(root)
    root.mainloop()
