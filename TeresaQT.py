import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QLCDNumber, QScrollBar, QMessageBox
from PIL import ImageGrab
import base64
import websocket
import json
import ssl
import datetime
import hashlib
import hmac
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
import configparser
import io

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(383, 341)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(158, 158, 158))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(158, 158, 158))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(158, 158, 158))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, brush)
        Dialog.setPalette(palette)
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 50, 71, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 280, 101, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 210, 71, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 30, 251, 141))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(20, 180, 251, 151))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.lcdNumber = QtWidgets.QLCDNumber(parent=Dialog)
        self.lcdNumber.setGeometry(QtCore.QRect(300, 310, 71, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, brush)
        self.lcdNumber.setPalette(palette)
        self.lcdNumber.setProperty("value", 1.0)
        self.lcdNumber.setProperty("intValue", 1)
        self.lcdNumber.setObjectName("lcdNumber")
        self.pushButton.clicked.connect(self.ImageUnderstand)
        self.pushButton_2.clicked.connect(self.open_life_tool)
        # self.pushButton_3.clicked.connect(self.image_understand)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "询问"))
        self.pushButton_2.setText(_translate("Dialog", "TRSTool 工具箱"))
        self.pushButton_3.setText(_translate("Dialog", "屏幕理解"))

    def take_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            screenshot.save("screenshot.png")
            QMessageBox.information(self, "截图成功", "截图已保存为 screenshot.png")
        except Exception as e:
            QMessageBox.critical(self, "截图失败", f"发生错误: {str(e)}")

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

    def open_life_tool(self):
        from LifeTool.mainGUI import GUI
        GUI()

class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()