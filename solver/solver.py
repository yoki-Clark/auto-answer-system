"""答题主逻辑 —— 读题 → AI生成 → 写入 → 提交 → 校验 → 重试"""
import time
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from automator import reader, writer, clicker
from ai_client.deepseek_client import generate_code, revise_code
from utils.logger import setup_logger

logger = setup_logger("solver")


def _load_calibration():
    calib_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "calibration.json",
    )
    if os.path.exists(calib_path):
        with open(calib_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _get_point(calibration: dict, key: str) -> tuple:
    """从校准数据提取单点坐标 → (x, y)"""
    item = calibration[key]
    return (item["x"], item["y"])


def _get_region(calibration: dict, key: str) -> dict:
    """从校准数据提取双点区域 → {x1, y1, x2, y2}"""
    return calibration[key]


def wait_for_result(wm, result_region: dict, timeout=None):
    """轮询等待第三栏出现结果"""
    if timeout is None:
        timeout = config.SUBMIT_TIMEOUT
    start = time.time()
    last_text = ""

    while time.time() - start < timeout:
        text = reader.read_result_text(wm, result_region)
        if text and text != last_text and text.strip():
            is_correct, error_msg = reader.parse_result(text)
            if is_correct is not None:
                return is_correct, error_msg
        last_text = text or ""
        time.sleep(config.RESULT_POLL_INTERVAL)

    logger.warning("等待提交结果超时")
    return None, ""


def solve_one_question(wm, calibration, question_index: int) -> bool:
    """解答一道题，返回是否成功"""
    question_region = _get_region(calibration, "question")
    answer_point = _get_point(calibration, "answer")
    result_region = _get_region(calibration, "result")
    submit_point = _get_point(calibration, "submit_btn")
    next_point = _get_point(calibration, "next_btn")

    # 读取题目 (OCR)
    question = reader.read_question(wm, question_region)

    # 读取已有代码 (剪贴板)
    existing_code = reader.read_current_code(wm, answer_point)

    # AI 生成代码
    code = generate_code(question, existing_code)

    for attempt in range(1, config.MAX_RETRIES_PER_QUESTION + 1):
        logger.info(f"--- 第 {question_index} 题 / 第 {attempt} 次提交 ---")

        writer.write_code(wm, answer_point, code)
        clicker.click_submit(wm, submit_point)

        is_correct, error_msg = wait_for_result(wm, result_region)

        if is_correct:
            logger.info("✓ 答题正确！")
            time.sleep(config.QUESTION_SWITCH_DELAY)
            clicker.click_next(wm, next_point)
            time.sleep(config.QUESTION_SWITCH_DELAY)
            return True

        if is_correct is False:
            logger.warning(f"✗ 答题错误 (第{attempt}次)")
            if attempt < config.MAX_RETRIES_PER_QUESTION:
                logger.info("调用 AI 修正代码...")
                code = revise_code(question, code, error_msg)
        else:
            logger.warning("无法确定结果，等待后重试")
            time.sleep(2)

    logger.error(f"题目 {question_index} 达到最大重试次数 ({config.MAX_RETRIES_PER_QUESTION})，跳过")
    clicker.click_next(wm, next_point)
    time.sleep(config.QUESTION_SWITCH_DELAY)
    return False


def run(wm, max_questions=None):
    """主循环：逐题解答"""
    calibration = _load_calibration()
    if calibration is None:
        raise RuntimeError("未找到 calibration.json，请先运行 calibrate.py 校准坐标")

    logger.info(f"开始答题循环 (每题最多重试 {config.MAX_RETRIES_PER_QUESTION} 次)")

    count = 0
    success_count = 0

    try:
        while max_questions is None or count < max_questions:
            count += 1
            ok = solve_one_question(wm, calibration, count)
            if ok:
                success_count += 1
            logger.info(f"进度: 已完成 {count} 题, 正确 {success_count}, 正确率 {success_count/count*100:.1f}%")
    except KeyboardInterrupt:
        logger.info("用户中断")
    except Exception as e:
        logger.error(f"运行异常: {e}")
        raise

    logger.info(f"答题结束: 共 {count} 题, 正确 {success_count}")
