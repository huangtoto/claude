#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - Telegram Bot 版本
使用 Telegram 作為通知管道（免費、永久有效）
"""

import requests
import json
from datetime import datetime
import os

# ===== 設定區 =====
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # 從 @BotFather 取得
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # 你的 Chat ID

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_telegram_message(message, bot_token, chat_id):
    """
    發送 Telegram 訊息
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"  # 支援 HTML 格式
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Telegram 訊息發送成功")
        return True
    except Exception as e:
        print(f"Telegram 訊息發送失敗: {e}")
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

    # 組合訊息（使用 HTML 格式）
    message = f"<b>📅 {today.strftime('%m/%d')} {weekday_name} 早餐提醒</b>\n\n"

    if has_beverage is None:
        message += "⚠️ 無法判斷今日是否有飲料\n建議帶杯子以防萬一"
    elif has_beverage:
        message += "☕ <b>今天有飲料！</b>\n✓ 記得帶杯子喔～"
    else:
        message += "✗ 今天沒有飲料\n不用帶杯子"

    # 發送訊息
    send_telegram_message(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
