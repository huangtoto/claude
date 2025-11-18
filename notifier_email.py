#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - Email 版本
使用 Email 發送通知（最通用，每個人都有）
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os

# ===== 設定區 =====

# Email 設定
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP 伺服器
SMTP_PORT = 587  # TLS 埠號
SENDER_EMAIL = "your_email@gmail.com"  # 寄件者信箱
SENDER_PASSWORD = "your_app_password"  # Gmail App 專用密碼（不是登入密碼！）
RECEIVER_EMAIL = "your_email@gmail.com"  # 收件者信箱（可以是同一個）

# 其他常見 Email 服務設定：
# Outlook/Hotmail: smtp.office365.com, port 587
# Yahoo: smtp.mail.yahoo.com, port 587
# 163: smtp.163.com, port 465 (SSL)

CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_email(subject, body, sender_email, sender_password, receiver_email):
    """
    發送 Email 通知
    """
    try:
        # 建立 email 訊息
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 加入郵件內容
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 連接到 SMTP 伺服器並發送
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # 啟用 TLS 加密
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Email 發送成功")
        return True
    except Exception as e:
        print(f"Email 發送失敗: {e}")
        return False


def load_schedule():
    """讀取飲料時間表配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"讀取配置檔失敗: {e}")
    return None


def check_beverage_by_schedule():
    """根據配置檔檢查今天是否有飲料"""
    schedule = load_schedule()
    if not schedule:
        return None

    today = datetime.now()

    # 依星期判斷
    if "weekly_pattern" in schedule:
        weekday = today.weekday()
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return schedule["weekly_pattern"].get(weekdays[weekday], None)

    # 依日期判斷
    if "dates" in schedule:
        date_str = today.strftime("%Y-%m-%d")
        return schedule["dates"].get(date_str, None)

    return None


def main():
    """主程式"""
    print(f"=== 早餐飲料檢查開始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]

    # 檢查是否為週末
    if today.weekday() >= 5:
        print("今天是週末，不發送提醒")
        return

    # 檢查飲料狀態
    has_beverage = check_beverage_by_schedule()

    # 組合郵件主旨和內容
    date_str = today.strftime('%m/%d')

    if has_beverage is None:
        subject = f"⚠️ {date_str} {weekday_name} 早餐提醒"
        body = f"""早安！

今天是 {date_str} {weekday_name}

⚠️ 無法判斷今日是否有飲料
建議帶杯子以防萬一

祝您有美好的一天！
"""
    elif has_beverage:
        subject = f"☕ {date_str} {weekday_name} 早餐提醒 - 記得帶杯子！"
        body = f"""早安！

今天是 {date_str} {weekday_name}

☕ 今天有飲料！
✓ 記得帶杯子喔～

祝您有美好的一天！
"""
    else:
        subject = f"✓ {date_str} {weekday_name} 早餐提醒 - 不用帶杯子"
        body = f"""早安！

今天是 {date_str} {weekday_name}

✗ 今天沒有飲料
不用帶杯子

祝您有美好的一天！
"""

    # 發送 Email
    send_email(subject, body, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
