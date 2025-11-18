#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日餐點通知系統 - Email 版（長期穩定方案）
每天早上 7:00 讀取菜單圖片，識別當天三餐內容，發送 Email
"""

import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import pytesseract
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ===== 設定區 =====

# Email 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Gmail App 專用密碼
RECEIVER_EMAIL = "your_email@gmail.com"

# 菜單圖片 URL
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


def format_html_email(menu_data, image_data):
    """格式化 HTML Email"""
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekday = menu_data.get('weekday', '未知')

    breakfast = menu_data.get('breakfast', '無法識別')
    lunch = menu_data.get('lunch', '無法識別')
    dinner = menu_data.get('dinner', '無法識別')

    html = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header .date {{
            margin-top: 10px;
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .meal {{
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .meal-title {{
            font-size: 20px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .meal-content {{
            font-size: 16px;
            color: #333;
            line-height: 1.6;
        }}
        .menu-image {{
            width: 100%;
            margin: 20px 0;
            border-radius: 8px;
        }}
        .footer {{
            padding: 20px;
            text-align: center;
            color: #999;
            font-size: 14px;
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍳 今日餐點</h1>
            <div class="date">{date_str} {weekday}</div>
        </div>

        <div class="content">
            <div class="meal">
                <div class="meal-title">🌅 早餐</div>
                <div class="meal-content">{breakfast}</div>
            </div>

            <div class="meal">
                <div class="meal-title">🍱 午餐</div>
                <div class="meal-content">{lunch}</div>
            </div>

            <div class="meal">
                <div class="meal-title">🌙 晚餐</div>
                <div class="meal-content">{dinner}</div>
            </div>

            <img src="cid:menu_image" alt="完整菜單" class="menu-image">
        </div>

        <div class="footer">
            祝您用餐愉快！😊<br>
            <small>更新時間：{datetime.now().strftime('%H:%M:%S')}</small>
        </div>
    </div>
</body>
</html>
"""
    return html


def send_email(menu_data, image_data):
    """發送 Email（含 HTML 和圖片）"""
    today = datetime.now()
    weekday = menu_data.get('weekday', '未知')

    try:
        # 建立郵件
        msg = MIMEMultipart('related')
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"📅 {today.strftime('%m/%d')} {weekday} 餐點通知"

        # HTML 內容
        html_content = format_html_email(menu_data, image_data)
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)

        # 附加圖片
        if image_data:
            image_part = MIMEImage(image_data)
            image_part.add_header('Content-ID', '<menu_image>')
            msg.attach(image_part)

        # 發送
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✓ Email 發送成功")
        return True
    except Exception as e:
        print(f"✗ Email 發送失敗: {e}")
        return False


def main():
    """主程式"""
    print("=" * 50)
    print("每日餐點通知系統 - Email 版")
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

    # 4. 發送 Email
    send_email(menu_data, image_data)

    print()
    print("=" * 50)
    print("✓ 完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
