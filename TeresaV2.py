import sys
from PyQt6.QtWidgets import QApplication
from TeresaV2_UI import ChatWindow

def main():
    app = QApplication(sys.argv)
    
    # 从环境变量或配置文件获取API密钥
    api_key = "******"
    window = ChatWindow(api_key)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()