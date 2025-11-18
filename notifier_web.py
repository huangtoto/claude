#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐飲料提醒系統 - 網頁版本
產生一個簡單的 HTML 頁面，用瀏覽器開啟即可查看
"""

import json
import os
from datetime import datetime

CONFIG_FILE = "beverage_schedule.json"
OUTPUT_HTML = "breakfast_today.html"

# ===== 函數定義 =====

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


def generate_html(has_beverage, date_str, weekday_name, update_time):
    """
    產生 HTML 頁面
    """
    if has_beverage is None:
        icon = "⚠️"
        title = "無法判斷"
        message = "無法判斷今日是否有飲料<br>建議帶杯子以防萬一"
        color = "#FFA500"  # 橘色
    elif has_beverage:
        icon = "☕"
        title = "今天有飲料！"
        message = "記得帶杯子喔～"
        color = "#4CAF50"  # 綠色
    else:
        icon = "✓"
        title = "今天沒有飲料"
        message = "不用帶杯子"
        color = "#9E9E9E"  # 灰色

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>早餐飲料提醒 - {date_str} {weekday_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }}
        .icon {{
            font-size: 100px;
            margin-bottom: 20px;
        }}
        .date {{
            font-size: 24px;
            color: #666;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 36px;
            font-weight: bold;
            color: {color};
            margin-bottom: 20px;
        }}
        .message {{
            font-size: 24px;
            color: #333;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .update-time {{
            font-size: 14px;
            color: #999;
            margin-top: 30px;
        }}
        @media (max-width: 600px) {{
            .container {{
                padding: 30px;
            }}
            .icon {{
                font-size: 80px;
            }}
            .title {{
                font-size: 28px;
            }}
            .message {{
                font-size: 20px;
            }}
        }}
    </style>
    <meta http-equiv="refresh" content="300">
</head>
<body>
    <div class="container">
        <div class="icon">{icon}</div>
        <div class="date">{date_str} {weekday_name}</div>
        <div class="title">{title}</div>
        <div class="message">{message}</div>
        <div class="update-time">更新時間：{update_time}</div>
    </div>
</body>
</html>"""

    return html_content


def main():
    """主程式"""
    print(f"=== 早餐飲料檢查開始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]
    date_str = today.strftime('%m/%d')
    update_time = today.strftime('%Y-%m-%d %H:%M:%S')

    # 檢查是否為週末
    if today.weekday() >= 5:
        print("今天是週末，不產生頁面")
        return

    # 檢查飲料狀態
    has_beverage = check_beverage_by_schedule()

    # 產生 HTML
    html_content = generate_html(has_beverage, date_str, weekday_name, update_time)

    # 寫入檔案
    try:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML 頁面已產生：{OUTPUT_HTML}")
        print(f"  請用瀏覽器開啟 file://{os.path.abspath(OUTPUT_HTML)}")
    except Exception as e:
        print(f"✗ HTML 產生失敗：{e}")

    print("=== 檢查完成 ===")


if __name__ == "__main__":
    main()
