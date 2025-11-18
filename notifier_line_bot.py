#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - LINE Messaging API 版本
使用 LINE Bot 取代即將停止服務的 LINE Notify
"""

import requests
import json
from datetime import datetime
import os

# ===== 設定區 =====
LINE_BOT_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN_HERE"
LINE_USER_ID = "YOUR_USER_ID_HERE"  # 你的 LINE User ID

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_line_message(message, user_id, access_token):
    """
    使用 LINE Messaging API 發送訊息
    """
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print("LINE 訊息發送成功")
        return True
    except Exception as e:
        print(f"LINE 訊息發送失敗: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"錯誤詳情: {e.response.text}")
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

    # 組合訊息
    message = f"📅 {today.strftime('%m/%d')} {weekday_name} 早餐提醒\n\n"

    if has_beverage is None:
        message += "⚠️ 無法判斷今日是否有飲料\n建議帶杯子以防萬一"
    elif has_beverage:
        message += "☕ 今天有飲料！\n✓ 記得帶杯子喔～"
    else:
        message += "✗ 今天沒有飲料\n不用帶杯子"

    # 發送訊息
    send_line_message(message, LINE_USER_ID, LINE_BOT_CHANNEL_ACCESS_TOKEN)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
