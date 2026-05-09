"""配置文件模板 —— 复制为 config.py 并填入真实值"""
import os

# ==================== 账号信息 ====================
ACCOUNT = "your_account"
PASSWORD = "your_password"

# ==================== DeepSeek API ====================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-api-key-here")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# ==================== 窗口信息 ====================
EXE_PATH = r"你的路径\Python小屋刷题软件客户端3.1.3.exe"
LOGIN_WINDOW_TITLE = "课堂管理系统3.1.3-董付国"
MAIN_WINDOW_TITLE_PREFIX = "编程题自测--"

# ==================== 答题参数 ====================
MAX_RETRIES_PER_QUESTION = 3
SUBMIT_TIMEOUT = 15
RESULT_POLL_INTERVAL = 0.5
WINDOW_WAIT_TIMEOUT = 30
QUESTION_SWITCH_DELAY = 1.5

# ==================== 题库缓存 ====================
QUESTION_BANK_FILE = "question_bank.json"
SIMILARITY_THRESHOLD = 0.85

# ==================== OCR 配置 ====================
TESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract.exe"
OCR_LANG = "chi_sim+eng"

# ==================== 日志 ====================
LOG_LEVEL = "INFO"
LOG_FILE = "automation.log"
