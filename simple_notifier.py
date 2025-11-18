#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡易版早餐飲料提醒系統
不使用 OCR，使用手動配置或簡單規則判斷
"""

import requests
import json
from datetime import datetime, timedelta
import os

# ===== 設定區 =====
LINE_NOTIFY_TOKEN = "YOUR_LINE_NOTIFY_TOKEN_HERE"
MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_line_notify(message, token):
    """發送 LINE Notify 訊息"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print("LINE 通知發送成功")
        return True
    except Exception as e:
        print(f"LINE 通知發送失敗: {e}")
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

    # 方法 1: 依星期判斷
    if "weekly_pattern" in schedule:
        weekday = today.weekday()  # 0=週一, 6=週日
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return schedule["weekly_pattern"].get(weekdays[weekday], None)

    # 方法 2: 依日期判斷
    if "dates" in schedule:
        date_str = today.strftime("%Y-%m-%d")
        return schedule["dates"].get(date_str, None)

    return None


def check_beverage_by_day():
    """簡單規則：根據星期幾判斷（範例）"""
    today = datetime.now()
    weekday = today.weekday()  # 0=週一, 6=週日

    # 範例規則：週一、三、五有飲料（請根據實際情況調整）
    has_beverage_days = [0, 2, 4]  # 週一、三、五

    return weekday in has_beverage_days


def check_menu_accessible():
    """檢查菜單是否可存取"""
    try:
        response = requests.head(MENU_URL, timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """主程式"""
    print(f"=== 早餐飲料檢查開始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]

    # 檢查是否為週末（假設週末不上班）
    if today.weekday() >= 5:  # 週六、週日
        print("今天是週末，不發送提醒")
        return

    # 方法 A: 使用配置檔
    has_beverage = check_beverage_by_schedule()

    # 方法 B: 使用簡單規則（如果沒有配置檔）
    if has_beverage is None:
        has_beverage = check_beverage_by_day()

    # 組合訊息
    message = f"\n📅 {today.strftime('%m/%d')} {weekday_name} 早餐提醒\n\n"

    if has_beverage is None:
        message += "⚠️ 無法判斷今日是否有飲料\n建議帶杯子以防萬一"
    elif has_beverage:
        message += "☕ 今天有飲料！\n✓ 記得帶杯子喔～"
    else:
        message += "✗ 今天沒有飲料\n不用帶杯子"

    # 發送通知
    send_line_notify(message, LINE_NOTIFY_TOKEN)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
