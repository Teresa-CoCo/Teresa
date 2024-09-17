import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QLCDNumber, QScrollBar, QMessageBox
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
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import re
import qdarkstyle
import subprocess
import sqlite3
history = []
# original_stdout = sys.stdout
# output = io.StringIO()
# sys.stdout = output

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    
    # 读取配置文件中的账号密码
    appid = config.get('Credentials', 'appid')
    api_secret = config.get('Credentials', 'api_secret')
    api_key = config.get('Credentials', 'api_key')
    # 加入Spark不同模型的版本
    
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

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("Teresa QT")
        TabWidget.setWindowIcon(QIcon("logo.ico"))
        TabWidget.resize(383, 358)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 30, 211, 131))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(parent=self.tab)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(20, 180, 211, 131))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton.setGeometry(QtCore.QRect(280, 30, 71, 121))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 190, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 240, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lcdNumber = QtWidgets.QLCDNumber(parent=self.tab)
        self.lcdNumber.setGeometry(QtCore.QRect(330, 280, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        TabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(parent=self.tab_2)
        self.plainTextEdit_5.setGeometry(QtCore.QRect(30, 60, 141, 191))
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(parent=self.tab_2)
        self.plainTextEdit_6.setGeometry(QtCore.QRect(220, 60, 141, 191))
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.label = QtWidgets.QLabel(parent=self.tab_2)
        self.label.setGeometry(QtCore.QRect(40, 30, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(230, 30, 49, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(260, 280, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 290, 181, 16))
        self.label_8.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        TabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(parent=self.tab_3)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(30, 60, 331, 231))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.label_3 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(40, 30, 141, 16))
        self.label_3.setObjectName("label_3")
        TabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(parent=self.tab_4)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(20, 30, 351, 271))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        TabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label_4 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_4.setGeometry(QtCore.QRect(160, 60, 111, 21))
        self.label_4.setObjectName("label_4")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.tab_5)
        self.graphicsView.setGeometry(QtCore.QRect(20, 10, 111, 131))
        self.graphicsView.setObjectName("graphicsView")
        self.label_5 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_5.setGeometry(QtCore.QRect(280, 60, 49, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_6.setGeometry(QtCore.QRect(160, 20, 49, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_7.setGeometry(QtCore.QRect(200, 20, 191, 16))
        self.label_7.setObjectName("label_7")
        self.comboBox = QtWidgets.QComboBox(parent=self.tab_5)
        self.comboBox.setGeometry(QtCore.QRect(150, 120, 211, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.tab_5)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 160, 75, 24))
        self.pushButton_5.setObjectName("pushButton_5")
        TabWidget.addTab(self.tab_5, "")
        self.command_ran = False
        # avatar

        self.scene = QtWidgets.QGraphicsScene()
        
        self.pixmap = QtGui.QPixmap("R.png")  # 替换为你的头像图片路径
        
        target_width = 100
        target_height = 125
        scaled_pixmap = self.pixmap.scaled(target_width, target_height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(scaled_pixmap)
        
        # 将头像添加到场景中
        self.scene.addItem(self.pixmapItem)
        
        # 设置 QGraphicsView 的场景
        self.graphicsView.setScene(self.scene)
                #Push buttons
        self.pushButton_3.clicked.connect(self.screenshot_and_ask)
        self.pushButton_2.clicked.connect(self.open_life_tool)
        self.pushButton.clicked.connect(self.talktospark)
        self.pushButton_5.clicked.connect(self.upgrade)
        self.pushButton_4.clicked.connect(self.helpmeoperate)


        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)


    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.pushButton.setText(_translate("TabWidget", "询问"))
        self.pushButton_3.setText(_translate("TabWidget", "屏幕理解"))
        self.pushButton_2.setText(_translate("TabWidget", "TRSTool生活工具箱"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "询问"))
        self.label.setText(_translate("TabWidget", "此处输入问题"))
        self.label_2.setText(_translate("TabWidget", "AI回答"))
        self.pushButton_4.setText(_translate("TabWidget", "询问AI"))
        self.label_8.setText(_translate("TabWidget", "为AI生成，请注意命令内容"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "帮我操作"))
        self.label_3.setText(_translate("TabWidget", "请在下方输入你的提示词"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3), _translate("TabWidget", "高级设置"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4), _translate("TabWidget", "聊天与操作历史"))
        self.label_4.setText(_translate("TabWidget", "您目前的用户等级："))
        self.label_5.setText(_translate("TabWidget", "TextLabel"))
        self.label_6.setText(_translate("TabWidget", "尊敬的"))
        self.label_7.setText(_translate("TabWidget", "TextLabel"))
        self.comboBox.setItemText(0, _translate("TabWidget", "可升级为："))
        self.comboBox.setItemText(1, _translate("TabWidget", "高级版（能够使用SparkMax模型（或Spark4.0 Ultra），具有完全态功能，提供客户支持。）"))
        self.pushButton_5.setText(_translate("TabWidget", "升级"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_5), _translate("TabWidget", "用户中心"))

    def setUsername(self,username):
        self.label_7.setText(username)
    def setUserGroup(self,username):
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        # 查询用户组
        cursor.execute('''
        SELECT user_group FROM users WHERE username = ?
        ''', (username,))
        # 获取结果
        user_group = cursor.fetchone()
        conn.close()
        # 检查是否找到匹配的记录
        if user_group:
            if user_group[0] =="Advanced":
                self.label_5.setText("高级版")
                self.comboBox.setEnabled(False)
                self.pushButton_5.setEnabled(False)
            else:
                self.label_5.setText("免费版")
        else:
            self.label_5.setText("未知")

    def take_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            screenshot.save("screenshot.png")
            QMessageBox.information(self.tab, "截图成功", "截图已保存为 screenshot.png")
        except Exception as e:
            QMessageBox.critical(self.tab, "截图失败", f"发生错误: {str(e)}")

    def ImageUnderstand(self,url1):
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
                    Input = "请详细描述图内的信息，为你后面回答我的问题提供更多准确信息"
                    question = checklen(getText("user", Input))
                    answer = ""

                    

                    print("", end="")
                    main(appid, api_key, api_secret, imageunderstanding_url, question)
                    getText("assistant", answer)
                    # daan = getText("assistant", answer)
                    a = 0
                    # sys.stdout = original_stdout
                    # output_text = output.getvalue()
                    # return output_text

                    # print(str(text))
        original_stdout = sys.stdout
        output = io.StringIO()
        sys.stdout = output
        imageUnderstanding(url1)
        sys.stdout = original_stdout
        output_text = output.getvalue()
        print(output_text)
        history_head="屏幕识别结果："
        history_content="AI识别结果："+output_text
        history.append(history_head)
        history.append(history_content)
        separator = "\n"
        text = separator.join(history)
        self.plainTextEdit_3.insertPlainText(text+"\n")
        return output_text

    def open_life_tool(self):
        from LifeTool.mainGUI import GUI
        GUI()
    def screenshot_and_ask(self):
        self.take_screenshot()
        # exe_dir = os.path.dirname(sys.executable)
        # file_path = os.path.join(exe_dir, 'screenshot.png')
        output_text = self.ImageUnderstand("screenshot.png")
        self.plainTextEdit_2.setPlainText(output_text + "\n")
        current_value = self.lcdNumber.value()
        new_value = current_value + 1
        self.lcdNumber.display(new_value)
    def spark(self,messages):
        # 星火认知大模型Spark Max的URL值（https://www.xfyun.cn/doc/spark/Web.html）
        if self.label_5 =="高级版":
            SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
            # 星火认知大模型Spark Max的domain值（https://www.xfyun.cn/doc/spark/Web.html）
            SPARKAI_DOMAIN = 'generalv3.5'
        else :
            # 对应Spark Lite版本
            SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
            SPARKAI_DOMAIN = 'general'
        


        if __name__ == '__main__':
            spark = ChatSparkLLM(
                spark_api_url=SPARKAI_URL,
                spark_app_id=SPARKAI_APP_ID,
                spark_api_key=SPARKAI_API_KEY,
                spark_api_secret=SPARKAI_API_SECRET,
                spark_llm_domain=SPARKAI_DOMAIN,
                streaming=True,
            )
            
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
    def talktospark(self):
        input_text = self.plainTextEdit.toPlainText()
        if input_text == "":
            QMessageBox.warning(self, 'Empty Input', '输入不能为空！')
        #Add prompt to the advanced tab
        prompt = self.plainTextEdit_4.toPlainText()

        messages=[ChatMessage(role="user",content=prompt)]
        messages.append(ChatMessage(role="user",content=input_text))
        output_text = self.spark(messages)  # 调用 self.spark 方法并传递输入文本
        # current_text = self.plainTextEdit_2.toPlainText()
        self.plainTextEdit_2.setPlainText(output_text + "\n")
        current_value = self.lcdNumber.value()
        new_value = current_value + 1
        self.lcdNumber.display(new_value)

        #Add history to the history tab
        history_head="您的问题："+input_text
        history_content="AI回答："+output_text
        history = []
        history.append(history_head)
        history.append(history_content)
        separator = "\n"
        text = separator.join(history)
        self.plainTextEdit_3.insertPlainText(text+"\n")
        new_message1 = ChatMessage(role="assistant", content=output_text)
        new_message2 = ChatMessage(role="assistant", content=output_text)
        messages.append(new_message1)
        messages.append(new_message2)
    # 设置标准输出编码为UTF-8
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    def getpythonandrun(self,user_input):
        # 提取所有反引号python反引号块中的内容
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, user_input, re.DOTALL)
        if matches:
            for idx, code_block in enumerate(matches, start=1):
                code_block = code_block.strip()
                filename = "python_code.py"
        # 匹配到的每个代码块写入到一个 Python 文件中并执行
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(code_block)
            # 执行文件，在新的cmd窗口中运行
            try:
                subprocess.Popen(['start', 'cmd', '/k', f'python {filename}'], shell=True)
                print(f"执行成功 {idx}: 已在新窗口中运行")
                
            except Exception as e:
                print(f"执行错误 {idx}: {str(e)}")
        ##Beta
    def helpmeoperate(self):
        messages=[]
        input_text = self.plainTextEdit_5.toPlainText()
        if input_text == "":
            QMessageBox.warning(self, 'Empty Input', '输入不能为空！')
        if self.command_ran == False:
            prompt = "你是 Teresa，一位世界级的程序员，可以通过执行代码来完成任何目标。用户输入的所有请求都是在Windows系统下的，对于高级请求，请从编写计划开始。当您执行代码时，它将在 **用户的机器** 上执行。用户已授予您 **完全权限** 来执行完成任务所需的任何代码。执行代码。您可以访问互联网。运行 **任何代码** 来实现目标，如果一开始没有成功，请不断重试。您可以安装新pip软件包，但请用bat来实现安装新pip软件包。当用户引用文件名时，他们很可能指的是您当前正在执行代码的目录中的现有文件。一般来说，尝试以尽可能少的步骤 **制定计划**。至于实际执行代码来执行该计划，对于 *有状态* 语言（如 python但不适用于每次都从 0 开始的 html）**重要的是不要尝试在一个代码块中完成所有事情。**您应该尝试一些事情，打印有关它的信息，然后从那里继续进行微小的、明智的步骤。你不可能第一次就成功，而且一次尝试往往会导致你看不到的错误。你有能力完成**任何**任务。请必须使用Python来处理问题。当遇到取决于用户本身或用户电脑本身的信息时，请尽可能用Python来获取（如当前用户的用户名）。谢谢。"
            messages=[ChatMessage(role="user",content=prompt)]
            self.spark(messages)
            self.command_ran = True
        messages.append(ChatMessage(role="user",content=input_text))
        output_text = self.spark(messages)  # 调用 self.spark 方法并传递输入文本
        # current_text = self.plainTextEdit_2.toPlainText()
        self.plainTextEdit_6.setPlainText(output_text + "\n")
        #Add history to the history tab
        history_head="您的问题："+input_text
        history_content="AI回答："+output_text
        history = []
        history.append(history_head)
        history.append(history_content)
        separator = "\n"
        text = separator.join(history)
        self.plainTextEdit_3.insertPlainText(text+"\n")
        new_message1 = ChatMessage(role="assistant", content=output_text)
        new_message2 = ChatMessage(role="assistant", content=output_text)
        messages.append(new_message1)
        messages.append(new_message2)
        reply = QMessageBox.question(self.tab, '确认执行', '您确定要执行操作吗？',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print('执行操作')
            self.getpythonandrun(output_text)
        else:
            print('取消操作')
    def upgrade(self):
        QMessageBox.information(self, "提示", f"升级功能暂未开放")



# TODO: 1.登入模块（已完成） 
# 2.头像部分 （已完成）
# 3.用SQLite写数据库（写两个用户）（已完成） 
# 4.优化“帮我操作”生成代码的过程 
# 5.如果还有时间，开发个安卓版本
# TODO: 免费版：能够免费使用SparkLite模型，但无法使用“帮我操作”功能，每个月能有几次试用高级版机会。
# 高级版：能够使用SparkMax模型（或Spark4.0 Ultra），具有完全态功能，提供客户支持。


# 1.登入模块

# 登入UI

# 数据库模块
def check_login(username, password):
    # 连接到数据库
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    # 查询用户
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    # 获取结果
    user = cursor.fetchone()
    conn.close()
    # 检查是否找到匹配的记录
    if user:
        return True
    else:
        return False

class LoginUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Teresa QT")
        Dialog.setWindowIcon(QIcon("logo.ico"))
        Dialog.resize(383,151)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(180, 30, 161, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 70, 161, 21))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(80, 30, 49, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 70, 49, 16))
        self.label_2.setObjectName("label_2")

        self.label.setText("用户名：")
        self.label_2.setText("密码：")
        self.buttonBox.accepted.connect(self.loginLogic)
        self.buttonBox.rejected.connect(self.close)
        Dialog.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

    def loginLogic(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if check_login(username, password):
            QMessageBox.information(self, "提示", f"登录成功，欢迎 {username}")
            self.close()  # 关闭登录界面
            self.open_teresa_ui(username)
        else:
            QMessageBox.warning(self, "提示", "登录失败，请检查用户名或密码")

    def open_teresa_ui(self,username):
        app = QtWidgets.QApplication.instance()  # 获取当前的应用实例
        if not app:
            app = QtWidgets.QApplication(sys.argv)
        self.teresa_ui = TeresaUI(username)
        self.teresa_ui.show()
        app.exec()



# 调用TeresaUI逻辑
class TeresaUI(QtWidgets.QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Teresa QT")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setGeometry(100, 100, 383, 358)
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.username = username

        # 使用 Ui_TabWidget 设置标签页内容
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self.tab_widget)
        # 传递用户名
        self.ui.setUsername(self.username)
        self.ui.setUserGroup(self.username)
        # 设置样式表
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_ui = LoginUI()
    login_ui.show()
    sys.exit(app.exec())
