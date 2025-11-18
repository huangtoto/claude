#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早餐菜單網頁伺服器
在內網提供網頁服務，可用手機/電腦瀏覽器開啟查看菜單
"""

from flask import Flask, render_template_string, send_file
import requests
from datetime import datetime
import os
from io import BytesIO

app = Flask(__name__)

# 菜單圖片 URL（內網）
MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"

# 快取設定
CACHE_FILE = "menu_cache.jpg"
CACHE_DURATION = 3600  # 1小時（秒）

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日早餐菜單</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .header .date {
            font-size: 18px;
            opacity: 0.9;
        }
        .menu-image {
            width: 100%;
            display: block;
        }
        .footer {
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        .refresh-btn {
            display: inline-block;
            margin: 20px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-size: 16px;
            transition: all 0.3s;
        }
        .refresh-btn:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .tips {
            background: #f8f9fa;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .tips h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .tips ul {
            list-style: none;
            padding-left: 20px;
        }
        .tips li {
            margin: 5px 0;
            color: #555;
        }
        .tips li:before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 5px;
        }
        @media (max-width: 600px) {
            .header h1 {
                font-size: 24px;
            }
            .header .date {
                font-size: 16px;
            }
        }
    </style>
    <meta http-equiv="refresh" content="300">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍳 今日早餐菜單</h1>
            <div class="date">{{ date }} {{ weekday }}</div>
        </div>

        {% if menu_available %}
        <img src="/menu-image" alt="早餐菜單" class="menu-image">

        <div class="tips">
            <h3>小提示</h3>
            <ul>
                <li>本頁面每 5 分鐘自動更新</li>
                <li>也可以手動重新整理瀏覽器</li>
                <li>將此頁面加入書籤，方便下次查看</li>
                <li>可以在手機上將此頁面「加到主畫面」</li>
            </ul>
        </div>
        {% else %}
        <div style="padding: 50px; text-align: center; color: #999;">
            <h2>😢 無法載入菜單</h2>
            <p>請確認網路連線正常</p>
            <a href="/" class="refresh-btn">重新載入</a>
        </div>
        {% endif %}

        <div class="footer">
            更新時間：{{ update_time }}<br>
            <a href="/" class="refresh-btn" style="margin-top: 10px;">🔄 重新整理</a>
        </div>
    </div>
</body>
</html>
"""

def download_menu():
    """下載菜單圖片"""
    try:
        # 檢查快取
        if os.path.exists(CACHE_FILE):
            cache_age = datetime.now().timestamp() - os.path.getmtime(CACHE_FILE)
            if cache_age < CACHE_DURATION:
                print(f"使用快取圖片（{int(cache_age)}秒前）")
                return True

        # 下載新圖片
        print("下載菜單圖片...")
        response = requests.get(MENU_URL, timeout=10)
        response.raise_for_status()

        # 儲存快取
        with open(CACHE_FILE, 'wb') as f:
            f.write(response.content)

        print("菜單圖片下載成功")
        return True
    except Exception as e:
        print(f"下載菜單失敗: {e}")
        return os.path.exists(CACHE_FILE)  # 如果有舊快取還是可以用


@app.route('/')
def index():
    """首頁"""
    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]

    menu_available = download_menu()

    return render_template_string(
        HTML_TEMPLATE,
        date=today.strftime('%Y年%m月%d日'),
        weekday=weekday_name,
        update_time=datetime.now().strftime('%H:%M:%S'),
        menu_available=menu_available
    )


@app.route('/menu-image')
def menu_image():
    """提供菜單圖片"""
    if os.path.exists(CACHE_FILE):
        return send_file(CACHE_FILE, mimetype='image/jpeg')
    else:
        return "圖片不存在", 404


if __name__ == '__main__':
    print("=" * 50)
    print("早餐菜單網頁伺服器")
    print("=" * 50)
    print("\n啟動中...")

    # 預先下載一次
    download_menu()

    print("\n✓ 伺服器已啟動！")
    print("\n請在瀏覽器開啟以下網址：")
    print("  內網電腦: http://localhost:5000")
    print("  同網段裝置: http://你的電腦IP:5000")
    print("\n查詢電腦 IP 位址：")
    print("  Windows: ipconfig")
    print("  Linux/Mac: ifconfig 或 ip addr")
    print("\n按 Ctrl+C 停止伺服器")
    print("=" * 50)

    # 啟動伺服器
    # 0.0.0.0 表示接受所有網路介面的連線（包括手機）
    app.run(host='0.0.0.0', port=5000, debug=False)
