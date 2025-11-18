#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週五和週一提醒腳本
上傳菜單並發送通知（Telegram/Discord/Email）
"""

import requests
from datetime import datetime
import os

# ===== 設定區 =====

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
IMGUR_CLIENT_ID = "YOUR_IMGUR_CLIENT_ID"

# 選擇通知方式（解除註解你要用的）
USE_TELEGRAM = True
USE_DISCORD = False
USE_EMAIL = False

# Telegram 設定
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Discord 設定
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL"

# Email 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"

# ===== 函數定義 =====

def should_send_today():
    """檢查今天是否應該發送（週五或週一）"""
    today = datetime.now()
    weekday = today.weekday()  # 0=週一, 4=週五

    return weekday in [0, 4]  # 週一 或 週五


def download_menu():
    """下載菜單圖片"""
    try:
        print("下載菜單圖片...")
        response = requests.get(MENU_URL, timeout=10)
        response.raise_for_status()
        print("✓ 下載成功")
        return response.content
    except Exception as e:
        print(f"✗ 下載失敗: {e}")
        return None


def upload_to_imgur(image_data):
    """上傳到 Imgur"""
    try:
        print("上傳到 Imgur...")
        headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            files={'image': image_data}
        )
        response.raise_for_status()
        data = response.json()
        image_url = data['data']['link']
        print(f"✓ 上傳成功: {image_url}")
        return image_url
    except Exception as e:
        print(f"✗ 上傳失敗: {e}")
        return None


def send_telegram(image_url):
    """發送 Telegram 通知"""
    if not USE_TELEGRAM:
        return

    try:
        today = datetime.now()
        weekday_name = ["週一", "週二", "週三", "週四", "週五"][today.weekday()]

        message = f"""📅 {today.strftime('%m/%d')} {weekday_name} 早餐菜單

🍳 本週菜單已更新！
點選下方連結查看完整菜單：
{image_url}

💡 可以將連結加入書籤，方便隨時查看
"""

        # 發送訊息
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

        # 發送圖片
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": image_url,
            "caption": f"{weekday_name}早餐菜單"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

        print("✓ Telegram 通知發送成功")
    except Exception as e:
        print(f"✗ Telegram 通知失敗: {e}")


def send_discord(image_url):
    """發送 Discord 通知"""
    if not USE_DISCORD:
        return

    try:
        today = datetime.now()
        weekday_name = ["週一", "週二", "週三", "週四", "週五"][today.weekday()]

        data = {
            "content": f"**📅 {today.strftime('%m/%d')} {weekday_name} 早餐菜單**\n\n🍳 本週菜單已更新！\n{image_url}",
            "username": "早餐菜單小幫手",
            "embeds": [{
                "image": {"url": image_url},
                "color": 6750054
            }]
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("✓ Discord 通知發送成功")
    except Exception as e:
        print(f"✗ Discord 通知失敗: {e}")


def send_email(image_url):
    """發送 Email 通知"""
    if not USE_EMAIL:
        return

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        today = datetime.now()
        weekday_name = ["週一", "週二", "週三", "週四", "週五"][today.weekday()]

        subject = f"📅 {today.strftime('%m/%d')} {weekday_name} 早餐菜單"

        body = f"""早安！

今天是 {today.strftime('%Y年%m月%d日')} {weekday_name}

🍳 本週早餐菜單已更新！

查看完整菜單：
{image_url}

💡 建議將連結加入書籤，方便隨時查看

祝您有美好的一天！
"""

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✓ Email 通知發送成功")
    except Exception as e:
        print(f"✗ Email 通知失敗: {e}")


def main():
    """主程式"""
    print("=" * 50)
    print("週五/週一菜單提醒")
    print("=" * 50)

    # 檢查是否為週五或週一
    if not should_send_today():
        today = datetime.now()
        weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]
        print(f"\n今天是{weekday_name}，不需要發送通知")
        print("僅在週一和週五發送")
        return

    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五"][today.weekday()]
    print(f"\n今天是{weekday_name}，開始處理...")
    print()

    # 1. 下載菜單
    image_data = download_menu()
    if not image_data:
        print("\n✗ 無法下載菜單")
        return

    print()

    # 2. 上傳到雲端
    image_url = upload_to_imgur(image_data)
    if not image_url:
        print("\n✗ 上傳失敗")
        return

    print()

    # 3. 發送通知
    send_telegram(image_url)
    send_discord(image_url)
    send_email(image_url)

    print()
    print("=" * 50)
    print("✓ 完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
