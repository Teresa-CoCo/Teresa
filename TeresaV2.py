import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from main_window import MainWindow
from config import config

def setup_application():
    """设置应用程序"""
    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Teresa V2")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Teresa Development Team")
    
    # 设置全局字体
    font = QFont(config.appearance.font_family, config.appearance.font_size)
    app.setFont(font)
    
    return app

def check_dependencies():
    """检查依赖项"""
    try:
        import openai
        return True
    except ImportError:
        QMessageBox.critical(
            None, "Missing Dependencies",
            "Required package 'openai' is not installed.\n"
            "Please install it using: pip install openai"
        )
        return False

def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建应用
    app = setup_application()
    
    try:
        # 检查API密钥
        if not config.api.api_key or config.api.api_key == "******":
            QMessageBox.information(
                None, "API Key Required",
                "Please configure your API key in Settings (Ctrl+,) to start using Teresa V2."
            )
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 运行应用
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(
            None, "Error",
            f"An error occurred while starting the application:\n{str(e)}"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())