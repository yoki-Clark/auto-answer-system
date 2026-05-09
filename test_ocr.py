"""读取功能测试 —— 测试题目(拖选+剪贴板)、答案(剪贴板)、结果(剪贴板)"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automator.window_mgr import WindowManager
from automator.reader import (
    read_question_number, read_question, read_current_code,
    read_result_text, parse_result,
)

CALIBRATION_FILE = "calibration.json"


def main():
    if not os.path.exists(CALIBRATION_FILE):
        print("[错误] 未找到 calibration.json，请先运行 calibrate.py")
        return

    with open(CALIBRATION_FILE, "r", encoding="utf-8") as f:
        calib = json.load(f)

    wm = WindowManager()
    existing = wm.find_window_by_title("编程题自测--")
    if not existing:
        print("[错误] 未找到答题窗口")
        return
    wm.main_window = existing
    print(f"✓ 已连接: {existing.window_text()}\n")

    # 测试0: 题号 (Ctrl+A 剪贴板)
    print("=" * 60)
    print("测试0: 读取题号 (Ctrl+A 剪贴板)")
    print("=" * 60)
    num_pt = (calib["question_number"]["x"], calib["question_number"]["y"])
    q_number = read_question_number(wm, num_pt)
    print(f"\n题号: '{q_number}'\n")

    # 测试1: 题目 (拖选+剪贴板 → OCR兜底)
    print("=" * 60)
    print("测试1: 读取题目 (拖选+剪贴板 优先)")
    print("=" * 60)
    question = read_question(wm, calib["question"])
    print(f"\n题目内容:\n{question}\n")

    # 测试2: 答案
    print("=" * 60)
    print("测试2: 读取已有代码 (Ctrl+A 剪贴板)")
    print("=" * 60)
    answer_pt = (calib["answer"]["x"], calib["answer"]["y"])
    code = read_current_code(wm, answer_pt)
    print(f"\n已有代码:\n{code}\n")

    # 测试3: 结果 (Ctrl+A 剪贴板 → OCR兜底)
    print("=" * 60)
    print("测试3: 读取结果反馈 (Ctrl+A 剪贴板 优先)")
    print("=" * 60)
    result = read_result_text(wm, calib["result"])
    print(f"\n结果原文:\n{result}\n")

    # 解析测试
    if result.strip():
        ok, msg = parse_result(result)
        print(f"解析结果: is_correct={ok}")
        if msg:
            print(f"详细信息: {msg[:200]}")


if __name__ == "__main__":
    main()
