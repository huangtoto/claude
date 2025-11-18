#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統
每天早上自動檢查菜單並發送 LINE 通知
"""

import requests
import os
from datetime import datetime
from io import BytesIO
from PIL import Image
import pytesseract

# ===== 設定區 =====
LINE_NOTIFY_TOKEN = "YOUR_LINE_NOTIFY_TOKEN_HERE"  # 請替換成你的 LINE Notify Token
MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"

# 飲料關鍵字（可依實際菜單調整）
BEVERAGE_KEYWORDS = [
    "飲料", "豆漿", "奶茶", "紅茶", "綠茶", "咖啡",
    "果汁", "牛奶", "米漿", "飲品", "茶", "汁"
]

# ===== 函數定義 =====

def download_menu_image(url):
    """
    下載菜單圖片
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"下載圖片失敗: {e}")
        return None


def check_beverage_in_image(image):
    """
    使用 OCR 檢查圖片中是否有飲料關鍵字
    需要安裝 tesseract-ocr
    """
    try:
        # 使用繁體中文 OCR
        text = pytesseract.image_to_string(image, lang='chi_tra')
        print(f"OCR 識別結果:\n{text}\n")

        # 檢查是否包含飲料關鍵字
        for keyword in BEVERAGE_KEYWORDS:
            if keyword in text:
                return True, keyword
        return False, None
    except Exception as e:
        print(f"OCR 處理失敗: {e}")
        return None, None


def check_beverage_simple(image):
    """
    簡易版：不使用 OCR，僅檢查圖片檔案大小或其他特徵
    你可以根據實際情況調整判斷邏輯
    """
    # 這裡提供一個簡單的範例：假設有飲料的圖片較大
    # 實際使用時需要根據真實情況調整
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    size = len(img_byte_arr.getvalue())

    print(f"圖片大小: {size} bytes")
    # 這只是示範，實際需要觀察規律後調整
    return size > 100000  # 假設超過 100KB 就有飲料


def send_line_notify(message, token):
    """
    發送 LINE Notify 訊息
    """
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "message": message
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print("LINE 通知發送成功")
        return True
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")
        return False


def main():
    """
    主程式
    """
    print(f"=== 早餐飲料檢查開始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    # 1. 下載菜單圖片
    image = download_menu_image(MENU_URL)
    if image is None:
        send_line_notify(
            "\n⚠️ 早餐提醒\n無法取得今日菜單，請自行確認是否需要帶杯子。",
            LINE_NOTIFY_TOKEN
        )
        return

    # 2. 檢查是否有飲料
    # 方法 A：使用 OCR（需要安裝 tesseract）
    has_beverage, keyword = check_beverage_in_image(image)

    # 方法 B：簡易判斷（不需要 OCR）
    # has_beverage = check_beverage_simple(image)
    # keyword = None

    # 3. 發送通知
    if has_beverage is None:
        message = "\n⚠️ 早餐提醒\n無法判斷今日是否有飲料，建議帶杯子以防萬一。"
    elif has_beverage:
        if keyword:
            message = f"\n☕ 早餐提醒\n今天有飲料！（發現關鍵字: {keyword}）\n記得帶杯子喔～"
        else:
            message = "\n☕ 早餐提醒\n今天有飲料！記得帶杯子喔～"
    else:
        message = "\n✓ 早餐提醒\n今天沒有飲料，不用帶杯子。"

    send_line_notify(message, LINE_NOTIFY_TOKEN)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
