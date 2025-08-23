"""
Teresa V2 启动器 - 简化版本
用于测试基本功能
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

def main():
    """主函数"""
    print("Starting Teresa V2...")
    
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("Teresa V2")
    
    try:
        # 导入主窗口
        from main_window import MainWindow
        
        # 创建主窗口
        window = MainWindow()
        
        # 显示窗口
        window.show()
        
        print("Teresa V2 started successfully!")
        print("Close the application window to exit.")
        
        # 运行应用
        return app.exec()
        
    except Exception as e:
        print(f"Error starting Teresa V2: {e}")
        
        # 显示错误对话框
        QMessageBox.critical(
            None, "Startup Error",
            f"Failed to start Teresa V2:\n\n{str(e)}\n\nPlease check the console for more details."
        )
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
