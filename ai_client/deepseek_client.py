"""DeepSeek API 客户端封装"""
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
import config
from ai_client.prompts import (
    SYSTEM_PROMPT,
    build_generate_prompt,
    build_revise_prompt,
)
from utils.logger import setup_logger

logger = setup_logger("deepseek")

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if config.DEEPSEEK_API_KEY == "your-api-key-here":
            raise ValueError(
                "请设置 DEEPSEEK_API_KEY 环境变量，或在 config.py 中填写 API Key"
            )
        _client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL,
        )
    return _client


def extract_code(response_text: str) -> str:
    """从 AI 返回的文本中提取纯代码
    处理 AI 可能用 ```python``` 包裹代码的情况
    """
    text = response_text.strip()

    # 尝试提取 ```python ... ``` 中的代码
    pattern = r"```(?:python)?\s*\n?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()

    return text


def generate_code(question: str, existing_code: str = "") -> str:
    """根据题目生成代码"""
    client = _get_client()
    user_prompt = build_generate_prompt(question, existing_code)

    logger.info("调用 DeepSeek 生成代码...")
    response = client.chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    code = extract_code(response.choices[0].message.content)
    logger.info(f"AI 返回代码长度: {len(code)} 字符")
    return code


def revise_code(question: str, previous_code: str, error_msg: str) -> str:
    """根据错误信息修正代码"""
    client = _get_client()
    user_prompt = build_revise_prompt(question, previous_code, error_msg)

    logger.info("调用 DeepSeek 修正代码...")
    response = client.chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    code = extract_code(response.choices[0].message.content)
    logger.info(f"AI 返回修正代码长度: {len(code)} 字符")
    return code
