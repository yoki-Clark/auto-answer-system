"""自动化答题系统 —— 主入口"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automator.window_mgr import WindowManager
from solver import solver
from utils.logger import setup_logger

logger = setup_logger("main")


def main():
    print("=" * 60)
    print("  自动化答题系统 — Python小屋刷题助手")
    print("=" * 60)

    wm = WindowManager()

    # ====== 阶段1: 启动并登录 ======
    print("\n[阶段1] 启动并登录软件...")
    # 如果软件已在运行且已登录，可跳过此步骤
    try:
        # 先尝试直接找答题窗口（已登录的情况）
        existing = wm.find_window_by_title("编程题自测--")
        if existing:
            print("检测到已登录的答题窗口，跳过启动和登录步骤。")
            wm.main_window = existing
        else:
            wm.start_app()
            wm.login()
    except Exception as e:
        print(f"登录失败: {e}")
        print("请确保软件已启动并登录到答题界面后重试。")
        return

    # ====== 阶段2: 开始答题 ======
    print("\n[阶段2] 开始自动答题...")
    print("提示: 按 Ctrl+C 可随时停止\n")

    try:
        solver.run(wm, max_questions=None)
    except RuntimeError as e:
        print(f"\n错误: {e}")
        print("请先运行: python calibrate.py 完成坐标校准")


if __name__ == "__main__":
    main()
