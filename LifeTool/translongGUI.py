import tkinter as tk
from tkinter import messagebox

class LengthConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("长度换算系统工具")

        self.label_intro = tk.Label(root, text="欢迎使用长度换算系统工具")
        self.label_intro.pack(pady=10)

        self.label_units = tk.Label(root, text="请选择输入单位：")
        self.label_units.pack()

        self.unit_options = ["米", "英尺", "英寸", "英里", "码"]
        self.input_unit = tk.StringVar(root)
        self.input_unit.set(self.unit_options[0])  # 默认选择第一个单位

        self.dropdown_units = tk.OptionMenu(root, self.input_unit, *self.unit_options)
        self.dropdown_units.pack(pady=10)

        self.label_input_value = tk.Label(root, text="请输入要换算的数值：")
        self.label_input_value.pack()

        self.entry_value = tk.Entry(root)
        self.entry_value.pack(pady=10)

        self.btn_convert = tk.Button(root, text="进行换算", command=self.convert)
        self.btn_convert.pack(pady=10)

    def convert(self):
        try:
            input_value = float(self.entry_value.get())
            chosen_unit = self.input_unit.get()

            if chosen_unit == "米":
                meter = input_value
                foot = meter * 3.2808
                inch = meter * 39.370
                mile = meter / 1000 * 0.621
                yard = meter * 1.0936

                result_message = f"{meter}米 = {foot:.2f}英尺 = {inch:.2f}英寸 = {mile:.2f}英里 = {yard:.2f}码"
                messagebox.showinfo("换算结果", result_message)

            elif chosen_unit == "英尺":
                foot = input_value
                meter = foot * 0.3048
                inch = meter * 39.370
                mile = meter / 1000 * 0.621
                yard = meter * 1.0936

                result_message = f"{meter:.2f}米 = {foot}英尺 = {inch:.2f}英寸 = {mile:.2f}英里 = {yard:.2f}码"
                messagebox.showinfo("换算结果", result_message)

            elif chosen_unit == "英寸":
                inch = input_value
                meter = inch * 0.0254
                foot = meter * 3.2808
                mile = meter / 1000 * 0.621
                yard = meter * 1.0936

                result_message = f"{meter:.2f}米 = {foot:.2f}英尺 = {inch}英寸 = {mile:.2f}英里 = {yard:.2f}码"
                messagebox.showinfo("换算结果", result_message)

            elif chosen_unit == "英里":
                mile = input_value
                meter = mile * 1609.34
                foot = meter * 3.2808
                inch = meter * 39.370
                yard = meter * 1.0936

                result_message = f"{meter:.2f}米 = {foot:.2f}英尺 = {inch:.2f}英寸 = {mile}英里 = {yard:.2f}码"
                messagebox.showinfo("换算结果", result_message)

            elif chosen_unit == "码":
                yard = input_value
                meter = yard * 0.9144
                foot = meter * 3.2808
                inch = meter * 39.370
                mile = meter / 1000 * 0.621

                result_message = f"{meter:.2f}米 = {foot:.2f}英尺 = {inch:.2f}英寸 = {mile:.2f}英里 = {yard}码"
                messagebox.showinfo("换算结果", result_message)

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")

def GUI():
        # 创建主窗口
    root = tk.Tk()
    app = LengthConverterGUI(root)
    root.mainloop()
