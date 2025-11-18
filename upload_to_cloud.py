#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上傳菜單到雲端（外連方案）
支援：Imgur（推薦）、Google Drive
"""

import requests
from datetime import datetime
import os
import json

# ===== 設定區 =====

MENU_URL = "http://srvap1.lungteng.com.tw/EIP/UPLOAD/MealsMenu/%E8%8F%9C%E5%96%AE.jpg"
OUTPUT_FILE = "menu_url.txt"  # 儲存公開網址

# Imgur 設定（推薦：免費、簡單、不需登入）
IMGUR_CLIENT_ID = "YOUR_IMGUR_CLIENT_ID"  # 從 https://api.imgur.com/oauth2/addclient 取得

# ===== 函數定義 =====

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
    """
    上傳到 Imgur（推薦）
    免費、簡單、不需要登入、圖片永久保存
    """
    try:
        print("上傳到 Imgur...")

        headers = {
            'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'
        }

        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            files={'image': image_data}
        )
        response.raise_for_status()

        data = response.json()
        image_url = data['data']['link']

        print(f"✓ 上傳成功！")
        print(f"  公開網址: {image_url}")

        return image_url
    except Exception as e:
        print(f"✗ 上傳失敗: {e}")
        return None


def upload_to_imgbb(image_data):
    """
    上傳到 ImgBB（替代方案）
    免費、簡單
    申請 API Key: https://api.imgbb.com/
    """
    IMGBB_API_KEY = "YOUR_IMGBB_API_KEY"

    try:
        print("上傳到 ImgBB...")

        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        response = requests.post(
            'https://api.imgbb.com/1/upload',
            data={
                'key': IMGBB_API_KEY,
                'image': image_base64
            }
        )
        response.raise_for_status()

        data = response.json()
        image_url = data['data']['url']

        print(f"✓ 上傳成功！")
        print(f"  公開網址: {image_url}")

        return image_url
    except Exception as e:
        print(f"✗ 上傳失敗: {e}")
        return None


def save_url(url):
    """儲存公開網址"""
    try:
        with open(OUTPUT_FILE, 'w') as f:
            f.write(url)
        print(f"✓ 網址已儲存到 {OUTPUT_FILE}")
    except Exception as e:
        print(f"✗ 儲存失敗: {e}")


def generate_html(image_url):
    """產生美觀的網頁"""
    today = datetime.now()
    weekday_name = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][today.weekday()]

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日早餐菜單 - {today.strftime('%m/%d')} {weekday_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header .date {{
            font-size: 18px;
            opacity: 0.9;
        }}
        .menu-image {{
            width: 100%;
            display: block;
            cursor: pointer;
        }}
        .footer {{
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        .tips {{
            background: #f8f9fa;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .tips h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍳 今日早餐菜單</h1>
            <div class="date">{today.strftime('%Y年%m月%d日')} {weekday_name}</div>
        </div>

        <img src="{image_url}" alt="早餐菜單" class="menu-image" onclick="window.open('{image_url}', '_blank')">

        <div class="tips">
            <h3>💡 小提示</h3>
            <p>點擊圖片可以放大查看</p>
            <p>將此頁面加入書籤，方便隨時查看</p>
        </div>

        <div class="footer">
            更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <small>此網址可在任何地方開啟</small>
        </div>
    </div>
</body>
</html>"""

    with open('menu_public.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ 網頁已產生: menu_public.html")


def main():
    """主程式"""
    print("=" * 50)
    print("菜單上傳雲端工具")
    print("=" * 50)

    # 1. 下載菜單
    image_data = download_menu()
    if not image_data:
        print("\n✗ 無法下載菜單，程式結束")
        return

    print()

    # 2. 上傳到雲端
    image_url = upload_to_imgur(image_data)

    # 如果 Imgur 失敗，可以試試 ImgBB
    # image_url = upload_to_imgbb(image_data)

    if not image_url:
        print("\n✗ 上傳失敗，程式結束")
        return

    print()

    # 3. 儲存網址
    save_url(image_url)

    # 4. 產生網頁
    generate_html(image_url)

    print()
    print("=" * 50)
    print("✓ 完成！")
    print("=" * 50)
    print(f"\n公開網址: {image_url}")
    print("\n這個網址可以在任何地方開啟（包括手機、家裡）")
    print("建議將網址加入手機書籤")
    print()


if __name__ == "__main__":
    main()
