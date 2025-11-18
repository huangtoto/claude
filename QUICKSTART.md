# 快速開始指南

## ⚠️ 重要：LINE Notify 將於 2025/3/31 停止服務

本指南已更新為使用 **Telegram Bot**（最簡單、免費、永久有效）

---

## 最快 5 分鐘設定完成！

### 步驟 1️⃣：設定 Telegram Bot (3分鐘)

#### 1-1. 安裝 Telegram（如果還沒有）
- 手機：App Store/Google Play 搜尋「Telegram」
- 電腦：https://desktop.telegram.org/

#### 1-2. 建立 Bot
1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/start`
3. 發送 `/newbot`
4. 輸入 Bot 名稱：`早餐提醒小幫手`
5. 輸入使用者名稱：`breakfast_reminder_bot`（或其他以 bot 結尾的名稱）
6. **複製 Bot Token**（長得像：`1234567890:ABCdef...`）

#### 1-3. 取得 Chat ID
1. 搜尋並開啟你剛建立的 Bot
2. 發送 `/start` 給它
3. 開啟瀏覽器，前往：
   ```
   https://api.telegram.org/bot你的TOKEN/getUpdates
   ```
   （把「你的TOKEN」換成剛才複製的）
4. 找到 `"chat":{"id":數字}`，那個數字就是你的 Chat ID

### 步驟 2️⃣：下載並設定程式 (1分鐘)

```bash
# 1. 下載程式（如果還沒有的話）
git clone <your-repo-url>
cd breakfast-beverage-alerts

# 2. 安裝套件
pip3 install -r requirements.txt

# 3. 編輯設定檔
nano notifier_telegram.py
# 修改這兩行：
# TELEGRAM_BOT_TOKEN = "你的Bot_Token"
# TELEGRAM_CHAT_ID = "你的Chat_ID"
```

### 步驟 3️⃣：測試執行 (30秒)

```bash
python3 notifier_telegram.py
```

✓ 如果你的 Telegram 收到訊息，就成功了！

### 步驟 4️⃣：設定每天自動執行 (30秒)

**Linux/Mac:**
```bash
crontab -e
# 加入這一行（每天早上 7:30 執行）
30 7 * * 1-5 cd /path/to/breakfast-beverage-alerts && /usr/bin/python3 notifier_telegram.py
```

**Windows:**
1. 開啟「工作排程器」
2. 建立基本工作 → 名稱：早餐提醒
3. 觸發：每天早上 7:30，週一到週五
4. 動作：執行 `python notifier_telegram.py`

---

---

## 🎯 其他通知方式

### 不想用 Telegram？

**Discord Webhook（3分鐘設定）**
- 適合已經在用 Discord 的人
- 詳細步驟：`NOTIFICATION_SETUP.md`

**LINE Messaging API（15分鐘設定）**
- 繼續使用 LINE（但設定較複雜）
- 詳細步驟：`NOTIFICATION_SETUP.md`

---

## 🎯 三種判斷方式

### 方式 A：簡單規則（最簡單）

修改程式中的規則：

```python
# 週一、三、五有飲料
has_beverage_days = [0, 2, 4]  # 0=週一, 2=週三, 4=週五
```

### 方式 B：配置檔（推薦）

編輯 `beverage_schedule.json`：

```json
{
  "weekly_pattern": {
    "monday": true,
    "tuesday": false,
    "wednesday": true,
    "thursday": false,
    "friday": true
  }
}
```

### 方式 C：OCR 自動識別（進階）

想要全自動？需要安裝 tesseract-ocr

詳細說明請看 `setup_guide.md`

---

## 📱 Telegram 收到的通知範例

**有飲料時：**
```
📅 11/18 週一 早餐提醒

☕ 今天有飲料！
✓ 記得帶杯子喔～
```

**沒有飲料時：**
```
📅 11/19 週二 早餐提醒

✗ 今天沒有飲料
不用帶杯子
```

---

## 💡 客製化建議

### 想要前一天晚上提醒？

改 crontab 時間：
```bash
0 21 * * 0-4 python3 notifier_telegram.py  # 週日到週四晚上 9:00
```

並修改程式訊息為「明天的早餐」

### 想要更早提醒（7:00）？

```bash
0 7 * * 1-5 python3 notifier_telegram.py
```

### 只想在有飲料時收到提醒？

修改程式，只在 `has_beverage == True` 時發送。

### 想要同時發送到多個平台？

修改程式同時呼叫多個發送函數：
```python
send_telegram_message(message, BOT_TOKEN, CHAT_ID)
send_discord_message(message, WEBHOOK_URL)
```

---

## ❓ 遇到問題？

**收不到 Telegram 通知？**
- 檢查 Bot Token 是否正確
- 檢查 Chat ID 是否正確
- 確認有對 Bot 發送過 `/start`
- 執行程式看有無錯誤訊息

**找不到 Chat ID？**
```
開啟：https://api.telegram.org/bot你的TOKEN/getUpdates
發送訊息給 Bot 後重新整理頁面
找到 "chat":{"id":數字}
```

**定時沒執行？**
```bash
# 檢查 crontab 是否正確
crontab -l

# 查看 cron 日誌
grep CRON /var/log/syslog
```

**菜單網址打不開？**
- 確認執行的電腦在公司內網
- 或考慮使用簡單規則/配置檔方式

---

## 🎁 額外福利：更簡單的方案

如果覺得程式太複雜，其實還有更簡單的解決方案：

### 方案 1：買個折疊杯
- 輕量矽膠折疊杯，放包包不佔空間
- 每天都帶，有備無患
- **成本：150-300元，一勞永逸**

### 方案 2：保持兩個杯子
- 座位放一個，包包放一個
- 完全不用煩惱

### 方案 3：LINE 群組協作
- 建立同事群組
- 早到的人發個訊息：「今天有飲料」
- 零成本，還能增進同事感情

---

**選擇最適合你的方式，享受美好的早餐時光！** ☕
