"""
坐标校准脚本 —— 双点定位各区域，单点定位按钮
使用方法：
  1. 确保答题窗口（编程题自测）已打开并可见
  2. 运行: python calibrate.py
  3. 按提示操作：

     OCR 区域（题目区、结果区）→ 用两点框定矩形范围：
        第一步：鼠标移到区域【左上角】，按 Enter
        第二步：鼠标移到区域【右下角】，按 Enter

     点击区域（答案区、按钮）→ 只需一点：
        鼠标移到目标中心，按 Enter

  4. 校准完成生成 calibration.json
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyautogui
import json

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

CALIBRATION_FILE = "calibration.json"

# 两点区域（左上角 + 右下角，用于 OCR 截图）
REGIONS_2POINT = [
    ("question", "题目区域", "第一栏题干文字区域"),
    ("result", "结果反馈区域", "第三栏提交后显示结果的区域"),
]

# 单点区域（中心点，用于点击或粘贴）
POINTS = [
    ("question_number", "题号框", "显示当前题号的小输入框——可 Ctrl+A 全选复制"),
    ("answer", "答案区域", "第二栏写代码的文本框——点击中心位置即可"),
    ("submit_btn", "提交答案按钮", ""),
    ("next_btn", "下一题按钮", ""),
    ("window_titlebar", "答题窗口标题栏", "窗口顶部标题栏任意位置"),
]


def do_2point(name: str, description: str):
    """两点定位一个矩形区域"""
    print(f"\n{'─'*50}")
    print(f"【{description}】")
    print(f"  第1步：将鼠标移到该区域的 ↑左上角↑，按 Enter...")
    input("  >>> ")
    x1, y1 = pyautogui.position()
    print(f"  ✓ 左上角: ({x1}, {y1})")

    print(f"  第2步：将鼠标移到该区域的 ↓右下角↓，按 Enter...")
    input("  >>> ")
    x2, y2 = pyautogui.position()
    print(f"  ✓ 右下角: ({x2}, {y2})")

    return {
        "x1": x1, "y1": y1,
        "x2": x2, "y2": y2,
    }


def do_point(name: str, description: str, extra: str = ""):
    """单点定位"""
    desc = f"{description}"
    if extra:
        desc += f"（{extra}）"
    print(f"\n{'─'*50}")
    print(f"【{desc}】")
    input(f"  将鼠标移到目标位置，按 Enter...\n  >>> ")
    x, y = pyautogui.position()
    print(f"  ✓ ({x}, {y})")
    return {"x": x, "y": y}


def main():
    print("=" * 60)
    print("  答题窗口坐标校准工具 (v2 — 双点定位)")
    print("=" * 60)
    print("\n注意：")
    print("  - 请确保答题窗口可见且没有被其他窗口遮挡")
    print("  - 每次操作先将鼠标移到指定位置，然后回到终端按 Enter")
    print("  - 区域定位使用两点（左上+右下）框定矩形范围")

    coords = {}

    # 两点区域
    print("\n\n>>> 阶段1: 框定 OCR 识别区域（两点定位）<<<")
    for key, desc, extra in REGIONS_2POINT:
        coords[key] = do_2point(key, desc)

    # 单点
    print("\n\n>>> 阶段2: 定位点击目标（单点定位）<<<")
    for key, desc, extra in POINTS:
        coords[key] = do_point(key, desc, extra)

    # 保存
    with open(CALIBRATION_FILE, "w", encoding="utf-8") as f:
        json.dump(coords, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("  ✓ 校准完成！坐标已保存到 calibration.json")
    print(f"{'='*60}")

    # 打印摘要
    print("\n校准数据摘要:")
    for key in ["question", "result"]:
        r = coords[key]
        w, h = r["x2"] - r["x1"], r["y2"] - r["y1"]
        print(f"  {key}: ({r['x1']},{r['y1']}) -> ({r['x2']},{r['y2']})  区域{w}x{h}")
    for key in ["question_number", "answer", "submit_btn", "next_btn"]:
        p = coords[key]
        print(f"  {key}: ({p['x']}, {p['y']})")


if __name__ == "__main__":
    main()
