# 自动化答题系统 — Python小屋刷题助手

基于 DeepSeek API + 桌面 GUI 自动化的 Python 编程题自动答题工具。

## 原理

1. **读取题目** — 鼠标拖选 + 剪贴板获取题干
2. **AI 生成代码** — 调用 DeepSeek API 生成/修正代码
3. **填写答案** — 剪贴板粘贴到答案区 + 模拟点击提交
4. **判断结果** — 读取反馈，答对进入下一题，答错用报错信息修正重试

## 环境要求

- Windows 10/11
- Python 3.10+
- Tesseract-OCR（含中文语言包）
- DeepSeek API Key

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置
cp config.example.py config.py
# 编辑 config.py，填入 DeepSeek API Key 和账号密码

# 3. 校准坐标（确保答题窗口已打开）
python calibrate.py

# 4. 测试读取
python test_ocr.py

# 5. 运行
python main.py
```

## 项目结构

```
├── main.py              # 主入口
├── config.example.py    # 配置模板
├── calibrate.py         # 坐标校准工具
├── test_ocr.py          # 读取测试
├── automator/           # GUI 自动化模块
│   ├── window_mgr.py    # 窗口管理 & 登录
│   ├── reader.py        # 读取题目/代码/结果
│   ├── writer.py        # 写入代码
│   └── clicker.py       # 点击按钮
├── ai_client/           # AI 接口
│   ├── deepseek_client.py
│   └── prompts.py
├── solver/              # 答题逻辑
│   └── solver.py
└── utils/               # 工具
    └── logger.py
```

## 免责声明

本项目仅供学习和研究使用，请遵守相关软件的使用协议。
