import tkinter as tk
from tkinter import messagebox
import subprocess

class PingToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping工具")

        self.label_intro = tk.Label(root, text="欢迎使用Ping工具")
        self.label_intro.pack(pady=10)

        self.btn_ping_foreign = tk.Button(root, text="Ping国外", command=self.ping_foreign)
        self.btn_ping_foreign.pack(pady=10)

        self.btn_ping_domestic = tk.Button(root, text="Ping国内", command=self.ping_domestic)
        self.btn_ping_domestic.pack(pady=10)

    def ping_foreign(self):
        self.ping("google.com")

    def ping_domestic(self):
        self.ping("baidu.com")

    def ping(self, hostname):
        try:
            # 执行Ping命令，设定超时时间为4秒，只Ping一次
            result = subprocess.run(['ping', hostname], capture_output=True, text=True, timeout=5)
            
            # 检查Ping的输出
            if result.returncode == 0:
                messagebox.showinfo("Ping结果", f"{hostname}：网络有效")
            else:
                messagebox.showinfo("Ping结果", f"{hostname}：网络无效")
        except subprocess.TimeoutExpired:
            messagebox.showerror("错误", f"{hostname}：请求超时")

def GUI():
        # 创建主窗口
    root = tk.Tk()
    app = PingToolGUI(root)
    root.mainloop()
