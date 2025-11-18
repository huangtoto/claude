# 每日餐點通知設定指南

## 你的需求

- ✅ **週一到週五**每天早上 7:00 自動推送
- ✅ **讀取圖片**，OCR 識別內容
- ✅ 顯示「**星期幾、早餐、午餐、晚餐**各是什麼」
- ✅ **長久可行**的方案（不要 LINE Notify）

---

## 🏆 推薦方案

### 方案一：Email + OCR（最推薦⭐）

**為什麼最推薦：**
- ✅ **永久標準協議**（SMTP 已存在 40+ 年）
- ✅ 不依賴任何單一公司
- ✅ 手機自動推播
- ✅ 完全免費
- ✅ 不需要裝額外 App

### 方案二：Telegram + OCR

**適合：**
- 願意裝 Telegram App
- 想要即時通訊風格的通知

---

## 📧 方案一設定：Email + OCR

### 步驟 1：安裝 tesseract-ocr

**Ubuntu/Debian:**
```bash
sudo apt install tesseract-ocr tesseract-ocr-chi-tra
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
1. 下載：https://github.com/UB-Mannheim/tesseract/wiki
2. 安裝時選擇「繁體中文」語言包
3. 設定環境變數

### 步驟 2：安裝 Python 套件

```bash
pip3 install requests Pillow pytesseract
```

### 步驟 3：取得 Gmail App 密碼

1. 前往 https://myaccount.google.com/security
2. 開啟「兩步驟驗證」
3. 前往 https://myaccount.google.com/apppasswords
4. 選擇「郵件」→「其他」→ 輸入「餐點通知」
5. 點選「產生」
6. **複製 16 位數密碼**

### 步驟 4：設定程式

編輯 `daily_menu_email.py`：

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # 剛才的 App 密碼
RECEIVER_EMAIL = "your_email@gmail.com"  # 可以是同一個
```

### 步驟 5：測試執行

```bash
python3 daily_menu_email.py
```

成功的話，你會收到一封漂亮的 HTML 郵件，包含：
- 今天是星期幾
- 早餐內容
- 午餐內容
- 晚餐內容
- 完整菜單圖片

### 步驟 6：設定定時執行

```bash
crontab -e

# 每天早上 7:00 執行（週一到週五）
0 7 * * 1-5 python3 /path/to/daily_menu_email.py
```

---

## 📱 方案二設定：Telegram + OCR

### 步驟 1：安裝 tesseract-ocr

（同方案一步驟 1）

### 步驟 2：建立 Telegram Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/start`
3. 發送 `/newbot`
4. 輸入 Bot 名稱：`餐點通知小幫手`
5. 輸入使用者名稱：`menu_reminder_bot`（或其他以 bot 結尾的名稱）
6. **複製 Bot Token**

### 步驟 3：取得 Chat ID

1. 搜尋並開啟你剛建立的 Bot
2. 發送 `/start` 給它
3. 開啟瀏覽器，前往：
   ```
   https://api.telegram.org/bot你的TOKEN/getUpdates
   ```
4. 找到 `"chat":{"id":數字}`，那個數字就是你的 Chat ID

### 步驟 4：設定程式

編輯 `daily_menu_telegram.py`：

```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdef..."  # 你的 Bot Token
TELEGRAM_CHAT_ID = "123456789"  # 你的 Chat ID
```

### 步驟 5：測試執行

```bash
python3 daily_menu_telegram.py
```

成功的話，你會收到 Telegram 通知，包含：
- 今天是星期幾
- 早餐、午餐、晚餐內容
- 完整菜單圖片

### 步驟 6：設定定時執行

```bash
crontab -e

# 每天早上 7:00 執行（週一到週五）
0 7 * * 1-5 python3 /path/to/daily_menu_telegram.py
```

---

## 📊 方案比較

| 項目 | Email | Telegram |
|------|-------|----------|
| **長期穩定性** | ⭐⭐⭐⭐⭐ 永久 | ⭐⭐⭐⭐ 很穩定 |
| **設定難度** | ⭐⭐ | ⭐⭐ |
| **需要 App** | ✗ | ✓ |
| **手機推播** | ✓ | ✓ |
| **美觀程度** | ⭐⭐⭐⭐⭐ HTML | ⭐⭐⭐⭐ Markdown |
| **免費** | ✓ | ✓ |
| **推薦度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 📝 收到的通知範例

### Email 版本

**主旨：** 📅 11/18 星期一 餐點通知

**內容：**（漂亮的 HTML 格式）

```
🍳 今日餐點
2024年11月18日 星期一

🌅 早餐
三明治、豆漿、水果

🍱 午餐
便當、湯品

🌙 晚餐
自助餐、飲料

[完整菜單圖片]

祝您用餐愉快！😊
```

### Telegram 版本

```
📅 2024年11月18日 星期一
━━━━━━━━━━━━━━━

🌅 早餐
三明治、豆漿、水果

🍱 午餐
便當、湯品

🌙 晚餐
自助餐、飲料

━━━━━━━━━━━━━━━
祝您用餐愉快！😊
```

並附上完整菜單圖片

---

## 🔧 OCR 識別準確度調整

如果 OCR 識別率不高，可以調整：

### 1. 圖片預處理

```python
# 在 ocr_image 函數中加入
from PIL import ImageEnhance

# 增加對比度
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2.0)

# 轉為灰階
image = image.convert('L')
```

### 2. 調整正則表達式

根據你的菜單實際格式，修改 `extract_today_menu` 函數中的正則表達式。

### 3. 手動微調

如果 OCR 總是識別不準，可以結合「配置檔」方式：

```json
{
  "2024-11-18": {
    "breakfast": "三明治、豆漿、水果",
    "lunch": "便當、湯品",
    "dinner": "自助餐、飲料"
  }
}
```

程式優先讀取配置檔，沒有的話才用 OCR。

---

## ⚙️ 進階設定

### 1. 前一天晚上提醒

```bash
crontab -e

# 每天晚上 9:00 提醒明天的餐點
0 21 * * 0-4 python3 /path/to/daily_menu_email.py --tomorrow
```

需要修改程式讀取「明天」對應的星期幾。

### 2. 錯誤處理

如果 OCR 失敗或圖片下載失敗，程式會自動發送錯誤通知。

### 3. 記錄歷史

```python
# 在 main() 函數末尾加入
import json

history = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "menu": menu_data
}

with open("menu_history.json", "a") as f:
    f.write(json.dumps(history, ensure_ascii=False) + "\n")
```

---

## ❓ 常見問題

### Q1: OCR 識別率很低怎麼辦？

A: 嘗試以下方法：
1. 確認已安裝繁體中文語言包：`tesseract-ocr-chi-tra`
2. 圖片預處理（增加對比度、去噪）
3. 如果菜單格式很固定，考慮用正則表達式直接定位
4. 最後手段：手動維護配置檔

### Q2: Gmail App 密碼找不到？

A: 必須先開啟「兩步驟驗證」才會出現「應用程式密碼」選項。

前往：https://myaccount.google.com/security

### Q3: 定時任務沒執行？

A: 檢查：
```bash
# 查看 crontab 設定
crontab -l

# 查看系統 log
grep CRON /var/log/syslog

# 測試 Python 路徑
which python3
```

確保 crontab 中的 Python 路徑正確。

### Q4: 週末也想收到通知？

A: 修改 crontab：
```bash
# 每天（包括週末）
0 7 * * * python3 /path/to/daily_menu_email.py
```

並移除程式中的週末檢查：
```python
# 註解掉這幾行
# if weekday_num >= 5:
#     print(f"今天是{today_weekday}（週末），不發送通知")
#     return
```

### Q5: 可以同時用 Email 和 Telegram 嗎？

A: 可以！
```bash
crontab -e

# 同時執行兩個程式
0 7 * * 1-5 python3 /path/to/daily_menu_email.py && python3 /path/to/daily_menu_telegram.py
```

或合併成一個程式，同時發送兩種通知。

---

## 🎯 最終建議

### 如果不想裝 App

**→ 使用 Email 版本**

- 永久標準協議
- 手機自動推播
- 漂亮的 HTML 格式
- 完全不用擔心服務停止

### 如果可以裝 App

**→ 使用 Telegram 版本**

- 即時通訊風格
- 更快收到
- 介面簡潔

### 兩個都用

**→ 雙重保障**

- Email：長期穩定
- Telegram：即時查看

---

選擇最適合你的方式，開始享受每天的餐點通知吧！🍳
