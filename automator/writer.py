"""数据写入 —— 将AI生成的代码写入答案区域"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyautogui
import pyperclip
from utils.logger import setup_logger

logger = setup_logger("writer")


def write_code(wm, answer_pos, code: str):
    """将代码写入答案区域（第二栏）"""
    wm.activate_main_window()
    time.sleep(0.2)

    # 点击答案区域
    pyautogui.click(*answer_pos)
    time.sleep(0.2)

    # 全选已有内容
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)

    # 将新代码放入剪贴板
    # 确保代码使用空格缩进
    code = code.replace("\t", "    ")
    pyperclip.copy(code)
    time.sleep(0.1)

    # 粘贴
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)

    logger.info(f"已写入代码 ({len(code)} 字符)")
