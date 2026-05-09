"""窗口管理 —— 启动EXE、登录、定位答题窗口"""
import time
import sys
import os
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyautogui
import pyperclip
from pywinauto import Desktop, Application
import config
from utils.logger import setup_logger

logger = setup_logger("window_mgr")

# 确保 pyautogui 有安全逃生机制
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class WindowManager:
    def __init__(self):
        self.login_window = None
        self.main_window = None

    def start_app(self):
        """启动 EXE 程序"""
        logger.info(f"启动程序: {config.EXE_PATH}")
        subprocess.Popen(config.EXE_PATH, shell=False)
        time.sleep(2)

    def find_window_by_title(self, title_keyword: str, timeout=None):
        """按标题查找窗口，返回 pywinauto 窗口对象"""
        if timeout is None:
            timeout = config.WINDOW_WAIT_TIMEOUT
        desktop = Desktop(backend="win32")
        start = time.time()
        while time.time() - start < timeout:
            for w in desktop.windows():
                try:
                    if title_keyword in w.window_text():
                        return w
                except Exception:
                    pass
            time.sleep(0.5)
        return None

    def login(self, account=None, password=None):
        """登录软件"""
        account = account or config.ACCOUNT
        password = password or config.PASSWORD

        logger.info("等待登录窗口...")
        self.login_window = self.find_window_by_title("课堂管理系统")
        if not self.login_window:
            raise RuntimeError("未找到登录窗口")

        self.login_window.set_focus()
        time.sleep(0.5)

        # 使用 Tab 导航 + 键盘输入的方式填写账号密码
        # Tkinter 窗口，采用剪贴板粘贴方式输入
        logger.info("填写账号...")
        pyperclip.copy(account)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)

        # Tab 切换到密码框
        pyautogui.press("tab")
        time.sleep(0.2)

        logger.info("填写密码...")
        pyperclip.copy(password)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)

        # Tab 到登录按钮，然后 Enter
        pyautogui.press("tab")
        time.sleep(0.2)
        pyautogui.press("enter")

        logger.info("已点击登录，等待答题窗口...")
        time.sleep(3)

        # 登录窗口应该在登录后关闭或隐藏，等待答题窗口出现
        self.main_window = self.find_window_by_title(
            config.MAIN_WINDOW_TITLE_PREFIX, timeout=20
        )
        if not self.main_window:
            # 可能登录失败，再等一下
            time.sleep(5)
            self.main_window = self.find_window_by_title(
                config.MAIN_WINDOW_TITLE_PREFIX, timeout=10
            )
        if not self.main_window:
            raise RuntimeError("登录后未找到答题窗口")

        logger.info(f"答题窗口已就绪: {self.main_window.window_text()}")

    def activate_main_window(self):
        """激活答题窗口，使其获得焦点"""
        if self.main_window:
            self.main_window.set_focus()

    def get_window_rect(self):
        """获取答题窗口的屏幕矩形 (left, top, right, bottom)"""
        if self.main_window:
            return self.main_window.rectangle()
        return None
