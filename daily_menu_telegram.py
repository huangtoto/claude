#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日餐點通知系統 - Telegram 版（長期穩定方案）
每天早上 7:00 讀取菜單圖片，識別當天三餐內容，發送 Telegram
"""

import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import pytesseract
import re

# ===== 設定區 =====

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"

# ===== 函數定義 =====

def download_menu_image():
    """下載菜單圖片"""
    try:
        print("下載菜單圖片...")
        response = requests.get(MENU_URL, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        print("✓ 圖片下載成功")
        return image, response.content
    except Exception as e:
        print(f"✗ 圖片下載失敗: {e}")
        return None, None


def ocr_image(image):
    """使用 OCR 識別圖片文字"""
    try:
        print("OCR 識別中...")
        text = pytesseract.image_to_string(image, lang='chi_tra')
        print("✓ OCR 識別完成")
        return text
    except Exception as e:
        print(f"✗ OCR 識別失敗: {e}")
        return None


def get_today_weekday():
    """取得今天是星期幾"""
    today = datetime.now()
    weekday_map = {
        0: '星期一', 1: '星期二', 2: '星期三',
        3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'
    }
    return weekday_map[today.weekday()], today.weekday()


def extract_today_menu(text):
    """從完整菜單中提取今天的餐點"""
    today_weekday, weekday_num = get_today_weekday()

    # 移除多餘空白
    text = re.sub(r'\s+', ' ', text)

    result = {
        'weekday': today_weekday,
        'breakfast': None,
        'lunch': None,
        'dinner': None
    }

    # 找到包含今天星期幾的部分
    lines = text.split('\n')
    relevant_text = ""

    for i, line in enumerate(lines):
        if today_weekday in line or today_weekday.replace('星期', '週') in line:
            # 收集這一行及後面幾行
            for j in range(i, min(i + 10, len(lines))):
                relevant_text += lines[j] + " "
            break

    if not relevant_text:
        relevant_text = text

    # 提取早餐
    breakfast_match = re.search(r'早餐?[：:、]?\s*([^\n午晚]{2,50})', relevant_text)
    if breakfast_match:
        result['breakfast'] = breakfast_match.group(1).strip()

    # 提取午餐
    lunch_match = re.search(r'午餐?[：:、]?\s*([^\n早晚]{2,50})', relevant_text)
    if lunch_match:
        result['lunch'] = lunch_match.group(1).strip()

    # 提取晚餐
    dinner_match = re.search(r'晚餐?[：:、]?\s*([^\n早午]{2,50})', relevant_text)
    if dinner_match:
        result['dinner'] = dinner_match.group(1).strip()

    return result


def format_telegram_message(menu_data):
    """格式化 Telegram 訊息"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekday = menu_data.get('weekday', '未知')

    breakfast = menu_data.get('breakfast', '無法識別')
    lunch = menu_data.get('lunch', '無法識別')
    dinner = menu_data.get('dinner', '無法識別')

    message = f"📅 *{date_str} {weekday}*\n"
    message += "━━━━━━━━━━━━━━━\n\n"
    message += f"🌅 *早餐*\n{breakfast}\n\n"
    message += f"🍱 *午餐*\n{lunch}\n\n"
    message += f"🌙 *晚餐*\n{dinner}\n\n"
    message += "━━━━━━━━━━━━━━━\n"
    message += "祝您用餐愉快！😊"

    return message


def send_telegram(menu_data, image_data):
    """發送 Telegram 通知（含圖片）"""
    try:
        # 1. 發送文字訊息
        message = format_telegram_message(menu_data)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

        # 2. 發送圖片
        if image_data:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            files = {'photo': BytesIO(image_data)}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": "完整菜單"
            }
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()

        print("✓ Telegram 通知發送成功")
        return True
    except Exception as e:
        print(f"✗ Telegram 通知發送失敗: {e}")
        return False


def main():
    """主程式"""
    print("=" * 50)
    print("每日餐點通知系統 - Telegram 版")
    print("=" * 50)
    print()

    # 檢查是否為週末
    today_weekday, weekday_num = get_today_weekday()
    if weekday_num >= 5:
        print(f"今天是{today_weekday}（週末），不發送通知")
        return

    print(f"今天是 {today_weekday}，開始處理...\n")

    # 1. 下載菜單圖片
    image, image_data = download_menu_image()
    if not image:
        print("✗ 無法繼續")
        return

    print()

    # 2. OCR 識別
    text = ocr_image(image)
    if not text:
        print("✗ 無法繼續")
        return

    print(f"\nOCR 識別結果：\n{text}\n")

    # 3. 解析今天的餐點
    menu_data = extract_today_menu(text)

    print("解析結果：")
    print(f"  早餐：{menu_data.get('breakfast', '無法識別')}")
    print(f"  午餐：{menu_data.get('lunch', '無法識別')}")
    print(f"  晚餐：{menu_data.get('dinner', '無法識別')}")
    print()

    # 4. 發送 Telegram
    send_telegram(menu_data, image_data)

    print()
    print("=" * 50)
    print("✓ 完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
