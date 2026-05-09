"""点击操作 —— 点击提交答案和下一题按钮"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyautogui
from utils.logger import setup_logger

logger = setup_logger("clicker")


def click_submit(wm, submit_pos):
    """点击"提交答案"按钮"""
    wm.activate_main_window()
    time.sleep(0.2)
    logger.info("点击: 提交答案")
    pyautogui.click(*submit_pos)


def click_next(wm, next_pos):
    """点击"下一题"按钮"""
    wm.activate_main_window()
    time.sleep(0.2)
    logger.info("点击: 下一题")
    pyautogui.click(*next_pos)
