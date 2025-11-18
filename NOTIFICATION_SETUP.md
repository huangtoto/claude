# 通知設定指南

LINE Notify 將於 2025/3/31 停止服務，本指南提供三種替代通知方案的詳細設定教學。

---

## 方案一：Telegram Bot（最推薦⭐）

### 為什麼推薦 Telegram？
- ✅ 完全免費，無訊息數量限制
- ✅ 設定超簡單（5分鐘完成）
- ✅ 穩定可靠，不會停止服務
- ✅ 跨平台支援（iOS、Android、Windows、Mac、Linux）

### 設定步驟

#### 步驟 1：安裝 Telegram
- iOS/Android：在 App Store/Google Play 搜尋「Telegram」
- 電腦版：https://desktop.telegram.org/
- 網頁版：https://web.telegram.org/

#### 步驟 2：建立 Bot
1. 在 Telegram 搜尋 `@BotFather`（官方機器人）
2. 發送 `/start` 開始對話
3. 發送 `/newbot` 建立新 Bot
4. 輸入 Bot 的顯示名稱（例如：早餐提醒小幫手）
5. 輸入 Bot 的使用者名稱（必須以 `_bot` 或 `Bot` 結尾，例如：breakfast_reminder_bot）
6. **複製 Bot Token**（格式類似：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）

#### 步驟 3：取得你的 Chat ID
1. 搜尋並開啟你剛建立的 Bot（用你設定的使用者名稱搜尋）
2. 發送 `/start` 給 Bot
3. 開啟瀏覽器，前往：
   ```
   https://api.telegram.org/bot你的BOT_TOKEN/getUpdates
   ```
   將 `你的BOT_TOKEN` 替換成步驟 2 複製的 Token
4. 在回傳的 JSON 中找到 `"chat":{"id":數字}`，這個數字就是你的 Chat ID
   ```json
   {
     "message": {
       "chat": {
         "id": 123456789,  ← 這個就是你的 Chat ID
         "first_name": "你的名字"
       }
     }
   }
   ```

#### 步驟 4：設定程式
編輯 `notifier_telegram.py`：
```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # 步驟 2 的 Token
TELEGRAM_CHAT_ID = "123456789"  # 步驟 3 的 Chat ID
```

#### 步驟 5：測試
```bash
python3 notifier_telegram.py
```

如果成功，你會在 Telegram 收到提醒訊息！

---

## 方案二：Discord Webhook

### 為什麼選擇 Discord？
- ✅ 適合已經在使用 Discord 的人
- ✅ 設定非常簡單（3分鐘）
- ✅ 完全免費

### 設定步驟

#### 步驟 1：建立 Discord 伺服器（如果還沒有）
1. 開啟 Discord
2. 點選左側「+」建立伺服器
3. 選擇「親自建立」→「僅供我和我的朋友使用」
4. 輸入伺服器名稱（例如：個人提醒）

#### 步驟 2：建立 Webhook
1. 在伺服器中建立一個文字頻道（例如：「早餐提醒」）
2. 點選頻道旁的齒輪圖示（編輯頻道）
3. 左側選單選擇「整合」→「Webhook」
4. 點選「新 Webhook」
5. 設定 Webhook 名稱（例如：早餐小幫手）
6. **複製 Webhook URL**（格式類似：`https://discord.com/api/webhooks/...`）

#### 步驟 3：設定程式
編輯 `notifier_discord.py`：
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/你的webhook網址"
```

#### 步驟 4：測試
```bash
python3 notifier_discord.py
```

成功的話，Discord 頻道會收到訊息！

---

## 方案三：LINE Messaging API

### 為什麼選擇 LINE Messaging API？
- ✅ LINE 官方推薦的 LINE Notify 替代方案
- ✅ 繼續使用 LINE，不用另外裝 App
- ✅ 每月免費額度：200 則訊息（足夠使用）

### 注意事項
- ⚠️ 設定較複雜（約需 15-20 分鐘）
- ⚠️ 需要建立 LINE Official Account
- ⚠️ 超過 200 則/月需付費

### 設定步驟

#### 步驟 1：建立 LINE Developers 帳號
1. 前往 https://developers.line.biz/
2. 使用 LINE 帳號登入
3. 點選「Create a new provider」建立提供者
4. 輸入 Provider 名稱（例如：個人專案）

#### 步驟 2：建立 Messaging API Channel
1. 點選「Create a Messaging API channel」
2. 填寫資料：
   - Channel name：早餐提醒 Bot
   - Channel description：個人使用的早餐提醒系統
   - Category：選擇適合的分類
   - Subcategory：選擇適合的子分類
3. 同意條款並建立

#### 步驟 3：設定 Channel
1. 進入剛建立的 Channel
2. 在「Messaging API」頁籤：
   - 找到「Channel access token」區域
   - 點選「Issue」發行 Token
   - **複製 Channel Access Token**
3. 關閉以下設定（避免自動回覆干擾）：
   - Auto-reply messages：Disabled
   - Greeting messages：Disabled

#### 步驟 4：加 Bot 為好友
1. 在「Messaging API」頁籤找到 QR Code
2. 用 LINE 掃描 QR Code 加 Bot 為好友
3. 或複製「LINE ID」在 LINE 中搜尋並加好友

#### 步驟 5：取得你的 User ID
**方法 A：使用網頁工具**
1. 傳送任意訊息給你的 Bot
2. 前往 Console → Messaging API → Webhook settings
3. 啟用 Webhook 並設定 URL（隨便填，只是要觸發）
4. 查看 webhook 收到的資料取得 User ID

**方法 B：使用測試腳本**
建立 `get_user_id.py`：
```python
import requests
import json

CHANNEL_ACCESS_TOKEN = "你的_CHANNEL_ACCESS_TOKEN"

url = "https://api.line.me/v2/bot/message/push"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
}

# 先隨便發一個測試訊息給自己
# 如果成功收到訊息，就表示 Token 正確

# 或使用 getProfile API（需要先知道 User ID）
```

**方法 C：最簡單的方式**
1. 在 Console → Messaging API
2. 找到「Your user ID」（如果有顯示的話）

如果以上方法都不行，可以使用 LINE Notify 移轉工具或詢問 LINE 官方文件。

#### 步驟 6：設定程式
編輯 `notifier_line_bot.py`：
```python
LINE_BOT_CHANNEL_ACCESS_TOKEN = "你的Channel_Access_Token"
LINE_USER_ID = "你的User_ID"  # 格式通常是 U開頭的字串
```

#### 步驟 7：測試
```bash
python3 notifier_line_bot.py
```

成功的話，你會在 LINE 收到 Bot 的訊息！

### LINE 費用說明
- 免費額度：每月 200 則訊息
- 如果每天發 1 則，一個月約 20-30 則，完全免費
- 超過的話：https://www.lycorp.co.jp/en/service/line-businesscenter/plan/

---

## 方案比較總結

| 項目 | Telegram | Discord | LINE Messaging API |
|------|----------|---------|-------------------|
| 設定難度 | ⭐⭐ 簡單 | ⭐ 最簡單 | ⭐⭐⭐⭐ 複雜 |
| 設定時間 | 5 分鐘 | 3 分鐘 | 15-20 分鐘 |
| 需要安裝 App | ✓ Telegram | ✓ Discord | ✗ 已有 LINE |
| 免費額度 | 無限制 | 無限制 | 200則/月 |
| 訊息推送速度 | 極快 | 快 | 快 |
| 穩定性 | 極高 | 高 | 高 |
| 推薦度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 建議

**新手/一般使用者** → 選擇 **Telegram**
- 最簡單、最穩定、完全免費

**已經在用 Discord** → 選擇 **Discord**
- 3 分鐘設定完成

**堅持用 LINE** → 選擇 **LINE Messaging API**
- 需要花點時間設定，但之後可以一直用

---

## 常見問題

### Q1: Telegram 安全嗎？
A: Telegram 是知名的通訊軟體，全球有數億用戶使用，安全性高。

### Q2: 我不想裝新的 App，有其他辦法嗎？
A: 可以使用 Discord（如果你已經有）或 LINE Messaging API。或者考慮「零技術方案」：買個折疊杯每天帶著。

### Q3: 哪個方案最省事？
A: Telegram。設定簡單、完全免費、不會停止服務。

### Q4: LINE Messaging API 超過 200 則會怎樣？
A: 會開始收費，但如果只用於個人提醒（每天1則），一個月最多 30 則，不會超過。

### Q5: 可以同時用多個通知方式嗎？
A: 可以！你可以修改程式同時發送到 Telegram 和 Discord，雙重保障。

---

需要更多協助？歡迎回報問題！
