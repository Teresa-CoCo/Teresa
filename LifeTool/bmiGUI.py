import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(entry_weight.get()) # type: ignore
        height = float(entry_height.get()) # type: ignore
        bmi = weight / (height * height)
        
        if bmi < 18.5:
            result = f"你的BMI是{bmi:.2f}，有点瘦"
        elif bmi >= 18.5 and bmi < 24:
            result = f"你的BMI是{bmi:.2f}，不错"
        elif bmi >= 24:
            result = f"你的BMI是{bmi:.2f}，有点肥胖"
        
        messagebox.showinfo("BMI计算结果", result)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的体重和身高！")

def GUI():
        # 创建主窗口
    root = tk.Tk()
    root.title("BMI计算器")

    # 添加标签和输入框
    label_weight = tk.Label(root, text="体重（kg）：")
    label_weight.grid(row=0, column=0, padx=10, pady=10)
    entry_weight = tk.Entry(root)
    entry_weight.grid(row=0, column=1, padx=10, pady=10)

    label_height = tk.Label(root, text="身高（m）：")
    label_height.grid(row=1, column=0, padx=10, pady=10)
    entry_height = tk.Entry(root)
    entry_height.grid(row=1, column=1, padx=10, pady=10)

    # 添加计算按钮
    calculate_button = tk.Button(root, text="计算BMI", command=calculate_bmi)
    calculate_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # 运行主循环
    root.mainloop()
