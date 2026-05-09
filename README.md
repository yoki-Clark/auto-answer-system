# 自动化答题系统 — Python小屋刷题助手

基于 DeepSeek API + 桌面 GUI 自动化的 Python 编程题自动答题工具。

## 原理

1. **读取题号+题目** — 剪贴板读取题号，鼠标拖选获取题干
2. **查题库缓存** — 按题号+题干相似度(≥85%)匹配，命中则直接用缓存答案
3. **AI 生成代码** — 未命中缓存时调用 DeepSeek API 生成/修正代码
4. **填写答案** — 剪贴板粘贴到答案区 + 模拟点击提交
5. **判断结果** — 读取反馈，答对自动存题库并进入下一题，答错用报错信息修正重试

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
    ├── logger.py
    └── question_bank.py  # 题库缓存
```

## 技术要点

- **目标软件是 Tkinter 构建的 EXE**，pywinauto 只能找到窗口但无法穿透内部控件树。所有交互依赖屏幕坐标（calibrate.py 校准）和键盘快捷键。
- **读取策略**（经实测确定）：题目区用鼠标拖选（Ctrl+A 会闪退），答案区、结果区、题号框用 Ctrl+A 全选。**Ctrl+A 与 Ctrl+C 之间必须 ≥0.06s 延迟**，否则剪贴板读空。OCR 仅作兜底。
- **题库缓存**：答对自动存 `question_bank.json`，同题号+题干相似度 ≥85% 直接复用，跳过 AI 调用。
- **结果判定**：只检查"恭喜/答题正确"等关键词，其余一切返回（含"提交失败"）全按错误处理，完整报错信息发给 AI 修正。
- **纠错机制**：每题最多 3 次重试。
- **退出方式**：鼠标移至屏幕四角自动触发安全退出（pyautogui 防故障机制）。Ctrl+C 也可。
- **Git 代理**：系统配置了 `http.proxy=http://127.0.0.1:7890`，推送时若代理未运行需 `git -c http.proxy= -c https.proxy= push`。

## 免责声明

本项目仅供学习和研究使用，请遵守相关软件的使用协议。
