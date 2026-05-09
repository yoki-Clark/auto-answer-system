"""题库缓存 —— 本地 JSON 文件存储，按题号索引，题干相似度校验"""
import json
import os
import sys
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.logger import setup_logger

logger = setup_logger("question_bank")


def _bank_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        config.QUESTION_BANK_FILE,
    )


def load_bank() -> dict:
    """加载题库文件，不存在则返回空字典"""
    path = _bank_path()
    if not os.path.exists(path):
        logger.info("题库文件不存在，视为空题库")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"题库已加载: {len(data)} 题")
        return data
    except Exception as e:
        logger.warning(f"题库加载失败: {e}，视为空题库")
        return {}


def save_to_bank(q_number: str, question: str, answer: str):
    """保存（或覆盖）一道题到题库"""
    if not q_number or not question or not answer:
        logger.warning("题号/题目/答案为空，跳过保存")
        return

    bank = load_bank()

    if q_number in bank and bank[q_number]["answer"] == answer:
        logger.info(f"题库 [{q_number}] 答案相同，跳过")
        return

    bank[q_number] = {
        "question": question.strip(),
        "answer": answer.strip(),
    }

    path = _bank_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)
    logger.info(f"已存入题库 [{q_number}]: {question[:40]}...")


def lookup(q_number: str, question_text: str) -> str | None:
    """查题库：按题号索引 → 题干相似度校验 → 返回缓存答案或 None

    Returns:
        缓存的答案字符串，或 None 表示未命中
    """
    if not q_number or not question_text:
        return None

    bank = load_bank()
    if not bank:
        return None

    entry = bank.get(q_number)
    if not entry:
        logger.info(f"题库 [{q_number}] 未找到")
        return None

    cached_question = entry.get("question", "")
    cached_answer = entry.get("answer", "")

    sim = SequenceMatcher(None, question_text.strip(), cached_question.strip()).ratio()
    logger.info(f"题库 [{q_number}] 相似度: {sim:.3f} (阈值: {config.SIMILARITY_THRESHOLD})")

    if sim >= config.SIMILARITY_THRESHOLD:
        logger.info(f"✓ 命中题库缓存 [{q_number}]，跳过 AI 调用")
        return cached_answer

    logger.info(f"相似度不足，视为不同题目")
    return None
