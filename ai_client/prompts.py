"""DeepSeek API 提示词模板"""

SYSTEM_PROMPT = """你是一个Python编程助手。用户会给你一道Python编程题，你需要写出正确、完整的代码。

必须严格遵守以下规则：
1. 只输出纯代码，不要有任何解释、注释或markdown标记（不要用```python```包裹）
2. 代码使用4个空格缩进，不要使用Tab字符
3. 如果题目要求函数有返回值，使用return，不要使用print()输出结果
4. 严格按照题目要求实现，不要添加题目没有要求的功能
5. 如果题目中已有部分代码框架，请在此基础上补全，不要重写整个程序"""


def build_generate_prompt(question: str, existing_code: str = "") -> str:
    """构建首次生成代码的用户提示词"""
    parts = [f"题目：\n{question}"]
    if existing_code.strip():
        parts.append(f"\n已有代码框架（请在此基础补全）：\n{existing_code}")
    parts.append("\n请输出完整代码：")
    return "\n".join(parts)


def build_revise_prompt(question: str, previous_code: str, error_msg: str) -> str:
    """构建纠错修正的用户提示词"""
    return f"""你的代码提交后执行报错了，请根据报错信息修正代码。

题目：
{question}

你上次提交的代码：
{previous_code}

报错信息：
{error_msg}

请输出修正后的完整代码（只输出代码，不要解释）。"""
