"""
Teresa V2 功能测试
验证核心模块是否正常工作
"""
import sys
import os

def test_imports():
    """测试导入"""
    print("Testing imports...")
    
    try:
        import PyQt6
        print("✓ PyQt6 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        from config import config
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from TeresaV2_HistoryUI import HistoryManager
        print("✓ HistoryManager imported successfully")
    except ImportError as e:
        print(f"✗ HistoryManager import failed: {e}")
        return False
    
    return True

def test_config():
    """测试配置系统"""
    print("\nTesting configuration system...")
    
    try:
        from config import config
        
        # 测试配置访问
        theme = config.appearance.theme
        print(f"✓ Current theme: {theme}")
        
        # 测试颜色获取
        colors = config.get_theme_colors()
        print(f"✓ Theme colors loaded: {len(colors)} colors")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_history_manager():
    """测试历史管理器"""
    print("\nTesting history manager...")
    
    try:
        from TeresaV2_HistoryUI import HistoryManager
        
        # 创建历史管理器实例
        history = HistoryManager()
        print("✓ HistoryManager created successfully")
        
        # 测试数据库初始化
        stats = history.get_statistics()
        print(f"✓ Database statistics: {stats}")
        
        return True
    except Exception as e:
        print(f"✗ History manager test failed: {e}")
        return False

def test_ui_components():
    """测试UI组件"""
    print("\nTesting UI components...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        
        # 创建应用实例（无GUI）
        app = QApplication([])
        
        from modern_ui import ModernButton, ChatScrollArea
        print("✓ Modern UI components imported successfully")
        
        app.quit()
        return True
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        return False

def main():
    """主测试函数"""
    print("Teresa V2 - System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_history_manager,
        test_ui_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Teresa V2 is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
