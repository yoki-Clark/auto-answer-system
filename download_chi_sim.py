"""下载 Tesseract 中文简体语言包
如果下载失败，请手动下载放到 C:\Program Files\Tesseract-OCR\tessdata\ 目录下
下载地址: https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
"""
import urllib.request
import os
import shutil

DEST = r"C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata"
URLS = [
    "https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata",
    "https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/chi_sim.traineddata",
]


def download(url, dest):
    print(f"尝试: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            with open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
        print(f"✓ 下载成功: {os.path.getsize(dest)} bytes")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False


def main():
    print("下载 Tesseract 中文简体语言包...")
    print(f"目标路径: {DEST}\n")

    if os.path.exists(DEST):
        print(f"文件已存在 ({os.path.getsize(DEST)} bytes)，无需下载。")
        return

    for url in URLS:
        if download(url, DEST):
            print("\n下载完成！请将 config.py 中的 OCR_LANG 改为 'chi_sim+eng'")
            return

    print("\n自动下载失败。请手动下载：")
    print("  1. 浏览器打开: https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata")
    print(f"  2. 保存到: {DEST}")
    print("  3. 将 config.py 中的 OCR_LANG 改为 'chi_sim+eng'")


if __name__ == "__main__":
    main()
