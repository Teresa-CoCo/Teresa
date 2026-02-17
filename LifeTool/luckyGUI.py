import tkinter as tk
from tkinter import messagebox
import random

class LuckyNumberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("幸运数与运气测试")

        self.label_intro = tk.Label(root, text="欢迎使用幸运数与运气占卜")
        self.label_intro.pack(pady=10)

        self.btn_generate_lucky_number = tk.Button(root, text="生成幸运数字", command=self.generate_lucky_number)
        self.btn_generate_lucky_number.pack(pady=10)

        self.btn_check_luck = tk.Button(root, text="判断今日运气", command=self.check_luck)
        self.btn_check_luck.pack(pady=10)

    def generate_lucky_number(self):
        randoseed = random.randint(1, 114514)
        random.seed(randoseed)
        randomnumber = random.randint(1, 9)
        messagebox.showinfo("幸运数字", f"您的幸运数字是：{randomnumber}")

    def check_luck(self):
        randomnumber = random.randint(1, 10)
        luck_levels = {
            1: "大吉",
            2: "中吉",
            3: "小吉",
            4: "吉",
            5: "半吉",
            6: "末吉",
            7: "凶",
            8: "半凶",
            9: "小凶",
            10: "大凶"
        }
        luck_result = luck_levels.get(randomnumber, "未知")
        messagebox.showinfo("今日运气", f"今天的运气是：{luck_result}")

def GUI():
        # 创建主窗口
    root = tk.Tk()
    app = LuckyNumberGUI(root)
    root.mainloop()
