"""
控件探测脚本 —— 打印登录窗口和答题窗口的全部控件树。
使用方法：
  1. 先手动启动 EXE 并登录到答题界面
  2. 然后运行本脚本：python explore.py
  3. 会自动探测当前打开的所有相关窗口并打印控件信息
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pywinauto import Desktop
from pywinauto.application import Application
import config


def explore_window_by_title(title_keyword: str):
    """按标题关键词查找窗口并打印控件树"""
    desktop = Desktop(backend="uia")
    found = False

    for window in desktop.windows():
        try:
            wt = window.window_text()
            if wt and title_keyword in wt:
                found = True
                print(f"\n{'='*80}")
                print(f"窗口标题: {wt}")
                print(f"窗口类名: {window.class_name()}")
                print(f"窗口句柄: {window.handle}")
                print(f"窗口矩形: {window.rectangle()}")
                print(f"{'='*80}")
                print("\n控件树 (print_control_identifiers):\n")
                window.print_control_identifiers()
                print("\n")
        except Exception as e:
            pass

    if not found:
        print(f"\n[!] 未找到包含 '{title_keyword}' 的窗口")


def list_all_windows():
    """列出桌面上所有可见窗口"""
    print(f"\n{'='*80}")
    print("桌面所有可见窗口列表:")
    print(f"{'='*80}")
    desktop = Desktop(backend="uia")
    for i, window in enumerate(desktop.windows()):
        try:
            wt = window.window_text()
            if wt:
                print(f"  [{i}] 标题: {wt[:80]}")
                print(f"       类名: {window.class_name()}, 句柄: {window.handle}")
                print(f"       矩形: {window.rectangle()}")
        except Exception:
            pass


if __name__ == "__main__":
    # 先列出所有窗口
    list_all_windows()

    # 探测登录窗口
    print(f"\n\n>>> 探测登录窗口 (关键词: '{config.LOGIN_WINDOW_TITLE[:10]}...')")
    explore_window_by_title(config.LOGIN_WINDOW_TITLE[:10])

    # 探测答题窗口
    print(f"\n\n>>> 探测答题窗口 (关键词: '{config.MAIN_WINDOW_TITLE_PREFIX}')")
    explore_window_by_title(config.MAIN_WINDOW_TITLE_PREFIX)

    print("\n>>> 探测完成。请将上方输出完整复制给我，我会据此编写自动化代码。")
