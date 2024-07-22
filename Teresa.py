import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import io
import json
import sys
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from PIL import ImageGrab
import tkinter as tk
from tkinter import messagebox
import websocket  # 使用websocket_client
import os
import sys
import configparser
original_stdout = sys.stdout
output = io.StringIO()
sys.stdout = output

'''

在运行根目录下创建一个secret.ini格式如下：

[Credentials]
appid = *****
api_secret = *****
api_key = ****

'''

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    
    # 读取配置文件中的账号密码
    appid = config.get('Credentials', 'appid')
    api_secret = config.get('Credentials', 'api_secret')
    api_key = config.get('Credentials', 'api_key')
    
    return appid, api_secret, api_key
base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
configs = os.path.join(base_path, 'secret.ini')
logo = os.path.join(base_path, 'logo.ico')
appid, api_secret, api_key = read_config(configs)
SPARKAI_APP_ID = appid
SPARKAI_API_SECRET = api_secret
SPARKAI_API_KEY = api_key

imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"  # 识图云端环境的服务地址
answer =" "
def take_screenshot():
    try:
        # 使用PIL的ImageGrab模块进行屏幕截图
        screenshot = ImageGrab.grab()

        screenshot.save("screenshot.png")

        messagebox.showinfo("截图成功", "截图已保存为 screenshot.png")
    except Exception as e:
        messagebox.showerror("截图失败", f"发生错误: {str(e)}")

def ImageUnderstand(url1):
    def imageUnderstanding(url):
        imagedata = open(url, 'rb').read()

        text = [{"role": "user", "content": str(base64.b64encode(imagedata), 'utf-8'), "content_type": "image"}]

        class Ws_Param(object):
            # 初始化
            def __init__(self, APPID, APIKey, APISecret, imageunderstanding_url):
                self.APPID = APPID
                self.APIKey = APIKey
                self.APISecret = APISecret
                self.host = urlparse(imageunderstanding_url).netloc
                self.path = urlparse(imageunderstanding_url).path
                self.ImageUnderstanding_url = imageunderstanding_url

            # 生成url
            def create_url(self):
                # 生成RFC1123格式的时间戳
                now = datetime.now()
                date = format_date_time(mktime(now.timetuple()))

                # 拼接字符串
                signature_origin = "host: " + self.host + "\n"
                signature_origin += "date: " + date + "\n"
                signature_origin += "GET " + self.path + " HTTP/1.1"

                # 进行hmac-sha256进行加密
                signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                         digestmod=hashlib.sha256).digest()

                signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

                authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

                authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

                # 将请求的鉴权参数组合为字典
                v = {
                    "authorization": authorization,
                    "date": date,
                    "host": self.host
                }
                # 拼接鉴权参数，生成url
                url = self.ImageUnderstanding_url + '?' + urlencode(v)
                # print(url)
                # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
                return url

        # 收到websocket错误的处理
        def on_error(ws, error):
            print("### error:", error)

        # 收到websocket关闭的处理
        def on_close(ws, one, two):
            print(" ")

        # 收到websocket连接建立的处理
        def on_open(ws):
            thread.start_new_thread(run, (ws,))

        def run(ws, *args):
            data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
            ws.send(data)

        # 收到websocket消息的处理
        def on_message(ws, message):
            # print(message)
            data = json.loads(message)
            code = data['header']['code']
            if code != 0:
                print(f'请求错误: {code}, {data}')
                ws.close()
            else:
                choices = data["payload"]["choices"]
                status = choices["status"]
                content = choices["text"][0]["content"]
                print(content, end="")
                global answer
                answer += content
                # print(1)
                if status == 2:
                    ws.close()

        def gen_params(appid, question):
            """
            通过appid和用户的提问来生成请参数
            """

            data = {
                "header": {
                    "app_id": appid
                },
                "parameter": {
                    "chat": {
                        "domain": "image",
                        "temperature": 0.5,
                        "top_k": 4,
                        "max_tokens": 2028,
                        "auditing": "default"
                    }
                },
                "payload": {
                    "message": {
                        "text": question
                    }
                }
            }

            return data

        def main(appid, api_key, api_secret, imageunderstanding_url, question):

            wsParam = Ws_Param(appid, api_key, api_secret, imageunderstanding_url)
            websocket.enableTrace(False)
            wsUrl = wsParam.create_url()
            ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close,
                                        on_open=on_open)
            ws.appid = appid
            # ws.imagedata = imagedata
            ws.question = question
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        def getText(role, content):
            jsoncon = {}
            jsoncon["role"] = role
            jsoncon["content"] = content
            text.append(jsoncon)
            return text

        def getlength(text):
            length = 0
            for content in text:
                temp = content["content"]
                leng = len(temp)
                length += leng
            return length

        def checklen(text):
            # print("text-content-tokens:", getlength(text[1:]))
            while (getlength(text[1:]) > 8000):
                del text[1]
            return text

        if __name__ == '__main__':
            a = 1
            # text.clear
            while (a == 1):
                Input = "请详细描述图内的信息"
                question = checklen(getText("user", Input))
                answer = ""
                print("答:", end="")
                main(appid, api_key, api_secret, imageunderstanding_url, question)
                getText("assistant", answer)
                # daan = getText("assistant", answer)
                a = 0
                # sys.stdout = original_stdout
                # output_text = output.getvalue()
                # return output_text

                # print(str(text))

    imageUnderstanding(url1)
    sys.stdout = original_stdout
    output_text = output.getvalue()
    print(output_text)
    return output_text
def spark(input):
    from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
    from sparkai.core.messages import ChatMessage
    import re
    # 星火认知大模型Spark Max的URL值（https://www.xfyun.cn/doc/spark/Web.html）
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    # 星火认知大模型调用秘钥信息（https://console.xfyun.cn/services/bm35）

    # 星火认知大模型Spark Max的domain值（https://www.xfyun.cn/doc/spark/Web.html）
    SPARKAI_DOMAIN = 'generalv3.5'

    if __name__ == '__main__':
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        messages = [ChatMessage(
            role="user",
            content=input
        )]
        handler = ChunkPrintHandler()
        result = spark.generate([messages], callbacks=[handler])
        a = str(result)
        pattern = r"text='(.*?)'"
        match = re.search(pattern, a)

        if match:
            extracted_text = match.group(1)
            extracted_text = extracted_text.replace('\\n', '\n')

            rresult = extracted_text
            return rresult
            print(extracted_text)
        else:
            print("Error 1")

def run_python_program():
    input_text = input_textbox.get("1.0", "end-1c")  # 获取输入文本框中的内容
    output_text =spark(input_text)
    output_textbox.insert(tk.END, output_text + "\n")  # 在输出文本框中显示结果

def clear_input():
    input_textbox.delete("1.0", tk.END)

def clear_output():
    output_textbox.delete("1.0", tk.END)

def screenshot_and_ask():
    take_screenshot()
    # exe_dir = os.path.dirname(sys.executable)
    # file_path = os.path.join(exe_dir, 'screenshot.png')
    output_text = ImageUnderstand("screenshot.png")
    output_textbox.insert(tk.END, output_text + "\n")

def LifeTool():
    from LifeTool.mainGUI import GUI
    GUI()




# 创建主窗口
root = tk.Tk()
root.title("Teresa")

root.iconbitmap(logo)

root.resizable(False, False)

root.configure(bg="#E0E0E0")  # 使用十六进制颜色码表示灰色

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)  # 设置字体大小
root.option_add("*Font", default_font)

# 创建输入文本框和按钮区域
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10)

input_label = tk.Label(input_frame, text="请输入你想问的问题:")
input_label.grid(row=0, column=0, sticky=tk.W)

input_textbox = scrolledtext.ScrolledText(input_frame, height=10, width=30)
input_textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

clear_input_button = tk.Button(input_frame, text="清空输入", command=clear_input)
clear_input_button.grid(row=2, column=0, padx=5, pady=5)

# 创建输出文本框和按钮区域
output_frame = tk.Frame(root)
output_frame.grid(row=0, column=1, padx=10, pady=10)

output_label = tk.Label(output_frame, text="结果:")
output_label.grid(row=0, column=0, sticky=tk.W)

output_textbox = scrolledtext.ScrolledText(output_frame, height=10, width=30)
output_textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

clear_output_button = tk.Button(output_frame, text="清空输出", command=clear_output)
clear_output_button.grid(row=2, column=0, padx=5, pady=5)

# 创建运行按钮和新添加的两个按钮
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

run_button = tk.Button(button_frame, text="询问", command=run_python_program)
run_button.grid(row=0, column=0, padx=5, pady=5)

# new_button1 = tk.Button(button_frame, text="帮助我操作（正在开发）")
# new_button1.grid(row=0, column=1, padx=5, pady=5)

new_button2 = tk.Button(button_frame, text="截图并理解当前屏幕内容（beta）",command=screenshot_and_ask)
new_button2.grid(row=0, column=2, padx=5, pady=5)

new_button3 = tk.Button(button_frame, text="生活小工具",command=LifeTool)
new_button3.grid(row=0, column=3, padx=5, pady=5)

# 运行主循环
root.mainloop()
