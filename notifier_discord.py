#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - Discord Webhook 版本
使用 Discord Webhook 發送通知（免費、簡單）
"""

import requests
import json
from datetime import datetime
import os

# ===== 設定區 =====
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_discord_message(message, webhook_url):
    """
    發送 Discord Webhook 訊息
    """
    data = {
        "content": message,
        "username": "早餐提醒小幫手"
    }

    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("Discord 訊息發送成功")
        return True
    except Exception as e:
        print(f"Discord 訊息發送失敗: {e}")
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
    message = f"📅 **{today.strftime('%m/%d')} {weekday_name} 早餐提醒**\n\n"

    if has_beverage is None:
        message += "⚠️ 無法判斷今日是否有飲料\n建議帶杯子以防萬一"
    elif has_beverage:
        message += "☕ **今天有飲料！**\n✓ 記得帶杯子喔～"
    else:
        message += "✗ 今天沒有飲料\n不用帶杯子"

    # 發送訊息
    send_discord_message(message, DISCORD_WEBHOOK_URL)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
