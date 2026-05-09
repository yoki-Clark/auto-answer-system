"""数据采集 —— 读取题目、已有代码、结果反馈

策略（根据实测调整）：
  - 题目区: Ctrl+A 会闪退选中 → 改用鼠标拖选 → Ctrl+C → 读取剪贴板 → 失败则 OCR 兜底
  - 答案区: Ctrl+A 正常 → 剪贴板读取
  - 结果区: Ctrl+A 正常 → 剪贴板读取 → 失败则 OCR 兜底
"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyautogui
import pyperclip
import pytesseract
from PIL import Image
import config
from utils.logger import setup_logger

logger = setup_logger("reader")

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH


# ==================== 工具函数 ====================

def _region_center(region: dict) -> tuple:
    """区域中心坐标"""
    cx = (region["x1"] + region["x2"]) // 2
    cy = (region["y1"] + region["y2"]) // 2
    return (cx, cy)


def _screenshot_region(region: dict) -> Image.Image:
    """根据校准的双点区域截图"""
    left = min(region["x1"], region["x2"])
    top = min(region["y1"], region["y2"])
    width = abs(region["x2"] - region["x1"])
    height = abs(region["y2"] - region["y1"])
    return pyautogui.screenshot(region=(left, top, width, height))


def _ocr_from_image(image: Image.Image) -> str:
    """PIL Image → OCR 文本"""
    try:
        text = pytesseract.image_to_string(image, lang=config.OCR_LANG)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR 失败: {e}")
        return ""


def _get_clipboard() -> str:
    """安全读取剪贴板"""
    try:
        return pyperclip.paste() or ""
    except Exception:
        return ""


# ==================== 剪贴板读取方式 ====================

def _clipboard_read_ctrl_a(wm, x, y):
    """点击坐标 → Ctrl+A → Ctrl+C → 读取剪贴板
    适用于 Ctrl+A 能正常全选的控件（答案区、结果区）
    """
    wm.activate_main_window()
    time.sleep(0.2)
    pyautogui.click(x, y)
    time.sleep(0.15)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.15)
    return _get_clipboard()


def _clipboard_read_drag(wm, region: dict):
    """鼠标拖选区域 → Ctrl+C → 读取剪贴板
    适用于 Ctrl+A 会闪退的控件（题目区）
    从区域左上角拖到右下角来选中文本
    """
    wm.activate_main_window()
    time.sleep(0.2)

    x1 = region["x1"]
    y1 = region["y1"]
    x2 = region["x2"]
    y2 = region["y2"]

    # 鼠标拖选
    pyautogui.moveTo(x1, y1)
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.moveTo(x2, y2, duration=0.3)
    time.sleep(0.05)
    pyautogui.mouseUp()
    time.sleep(0.15)

    # 复制
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.15)
    return _get_clipboard()


# ==================== 公开接口 ====================

def read_question(wm, question_region: dict) -> str:
    """读取第一栏——题干内容
    策略：鼠标拖选 → 剪贴板（优先）→ OCR（兜底）
    """
    logger.info("读取题目...")
    text = _clipboard_read_drag(wm, question_region)

    if text.strip():
        logger.info(f"题目(拖选): {len(text)} 字符")
        return text

    # 拖选失败，尝试 Ctrl+A 方式（万一有时能行）
    cx, cy = _region_center(question_region)
    text = _clipboard_read_ctrl_a(wm, cx, cy)
    if text.strip():
        logger.info(f"题目(Ctrl+A): {len(text)} 字符")
        return text

    # 剪贴板方式都失败，降级到 OCR
    logger.info("剪贴板为空，降级到 OCR...")
    image = _screenshot_region(question_region)
    debug_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "screenshots", "question_debug.png"
    )
    image.save(debug_path)
    text = _ocr_from_image(image)
    logger.info(f"题目(OCR): {len(text)} 字符")
    return text or ""


def read_question_number(wm, number_pos: tuple) -> str:
    """读取题号（题号框 Ctrl+A 可用，用户确认）"""
    logger.info("读取题号...")
    text = _clipboard_read_ctrl_a(wm, number_pos[0], number_pos[1])
    # 清洗：去空白，如果是 "第X题" 提取数字
    text = text.strip()
    # 去掉可能的 "第" "题" 前缀后缀
    text = text.lstrip("第题").rstrip("题")
    logger.info(f"题号: '{text}'")
    return text


def read_current_code(wm, answer_pos: tuple) -> str:
    """读取第二栏——已有代码（答案区 Ctrl+A 可用）"""
    logger.info("读取已有代码...")
    text = _clipboard_read_ctrl_a(wm, answer_pos[0], answer_pos[1])
    if text.strip():
        logger.info(f"已有代码: {len(text)} 字符")
    else:
        logger.info("已有代码为空")
    return text


def read_result_text(wm, result_region: dict) -> str:
    """读取第三栏——结果反馈
    策略：Ctrl+A 剪贴板（优先，用户确认可用）→ OCR（兜底）
    """
    logger.info("读取结果...")
    cx, cy = _region_center(result_region)
    text = _clipboard_read_ctrl_a(wm, cx, cy)

    if text.strip():
        logger.info(f"结果(剪贴板): {text[:120]}")
        return text

    # 降级 OCR
    logger.info("剪贴板为空，降级到 OCR...")
    image = _screenshot_region(result_region)
    text = _ocr_from_image(image)
    logger.info(f"结果(OCR): {text[:120] if text else '空'}")
    return text or ""


def parse_result(result_text: str) -> tuple:
    """解析结果文本，判断答题是否正确
    Returns:
        (is_correct: bool, error_message: str)
        - 正确: (True, "")
        - 错误: (False, error_detail)
        - 不确定: (None, "")
    """
    if not result_text.strip():
        return None, ""

    text = result_text.strip()

    correct_keywords = ["恭喜", "答题正确", "答案正确", "通过"]
    for kw in correct_keywords:
        if kw in text:
            return True, ""

    error_keywords = ["答题错误", "答案错误", "执行结果", "Traceback", "错误", "Error"]
    for kw in error_keywords:
        if kw in text:
            return False, text

    return None, text
