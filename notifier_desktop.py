#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - 桌面通知版本
在電腦螢幕顯示彈出通知（適合電腦在公司的人）
"""

import json
import os
from datetime import datetime

# 跨平台桌面通知
try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False
    print("注意：未安裝 plyer，將使用替代方案")

CONFIG_FILE = "beverage_schedule.json"

# ===== 函數定義 =====

def send_desktop_notification(title, message, duration=10):
    """
    發送桌面通知
    """
    try:
        if HAS_PLYER:
            # 使用 plyer（跨平台）
            notification.notify(
                title=title,
                message=message,
                app_name='早餐提醒',
                timeout=duration  # 顯示秒數
            )
            print("桌面通知發送成功 (plyer)")
        else:
            # 依作業系統使用不同方法
            import platform
            system = platform.system()

            if system == "Darwin":  # macOS
                os.system(f'''
                    osascript -e 'display notification "{message}" with title "{title}"'
                ''')
                print("桌面通知發送成功 (macOS)")
            elif system == "Linux":
                os.system(f'notify-send "{title}" "{message}"')
                print("桌面通知發送成功 (Linux)")
            elif system == "Windows":
                # Windows 需要額外的套件，這裡提供簡單的替代方案
                os.system(f'msg "%username%" "{title}: {message}"')
                print("桌面通知發送成功 (Windows)")

        return True
    except Exception as e:
        print(f"桌面通知發送失敗: {e}")
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

    # 組合通知
    date_str = today.strftime('%m/%d')

    if has_beverage is None:
        title = f"⚠️ {date_str} {weekday_name} 早餐提醒"
        message = "無法判斷今日是否有飲料，建議帶杯子"
    elif has_beverage:
        title = f"☕ {date_str} {weekday_name} 早餐提醒"
        message = "今天有飲料！記得帶杯子喔～"
    else:
        title = f"✓ {date_str} {weekday_name} 早餐提醒"
        message = "今天沒有飲料，不用帶杯子"

    # 發送桌面通知
    send_desktop_notification(title, message)
    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
