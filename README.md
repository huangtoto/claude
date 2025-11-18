# 早餐飲料提醒系統

## ⚠️ 重要更新 (2024/11/18)

**LINE Notify 將於 2025/3/31 停止服務！**

本專案已更新為使用以下替代通知方案：
- ✅ **Telegram Bot**（推薦：免費、永久、最簡單）
- ✅ **Discord Webhook**（適合已使用 Discord 的使用者）
- ✅ **LINE Messaging API**（官方推薦，但需建立 LINE Bot）

詳細設定請參考 `NOTIFICATION_SETUP.md`

---

## 問題描述
- 公司每天供應早餐，但飲料供應不固定
- 餐廳離座位遠，希望出發前就知道要不要帶杯子
- 早上電腦未開機，查看菜單不便
- 希望每天早上自動收到通知提醒

## 通知方案比較

### 方案一：Telegram Bot（最推薦⭐）

**優點：**
- ✅ 完全免費、無訊息數量限制
- ✅ 設定超簡單（5分鐘完成）
- ✅ 跨平台：手機、電腦都能用
- ✅ 不需要申請審核

**缺點：**
- ⚠️ 需要安裝 Telegram App

**適合：想要最簡單、最穩定方案的使用者**

### 方案二：Discord Webhook

**優點：**
- ✅ 完全免費
- ✅ 設定簡單（3分鐘完成）
- ✅ 適合已經使用 Discord 的人

**缺點：**
- ⚠️ 需要有 Discord 帳號

**適合：已經在使用 Discord 的使用者**

### 方案三：LINE Messaging API

**優點：**
- ✅ LINE 官方推薦替代方案
- ✅ 繼續使用 LINE（不用額外裝 App）
- ✅ 每月有免費額度

**缺點：**
- ⚠️ 設定較複雜（需建立 LINE Bot）
- ⚠️ 超過免費額度需付費
- ⚠️ 需要 LINE Business 帳號

**適合：堅持使用 LINE 的使用者**

### 方案四：簡化方案（零技術門檻）

**直接解決問題的思路：**
1. **永遠帶杯子** - 買個輕便折疊杯（150元）
2. **保持兩個杯子** - 座位一個、背包一個
3. **同事群組** - 早到的人通知一聲

## 推薦架構

```
內網設備 (樹莓派/舊電腦/公司電腦)
  ├─ 定時任務 (crontab: 每天 7:30)
  ├─ 下載菜單圖片（可選）
  ├─ OCR 識別 / 規則判斷
  └─ 發送通知 (Telegram/Discord/LINE)
```

## 快速開始

### 1️⃣ 選擇通知方式並設定

**最簡單：Telegram（5分鐘）**
```bash
# 詳細步驟請看 NOTIFICATION_SETUP.md
python3 notifier_telegram.py
```

**其他方式：**
- Discord Webhook → `notifier_discord.py`
- LINE Messaging API → `notifier_line_bot.py`

### 2️⃣ 選擇判斷方式

- **簡單規則**：`simple_notifier.py`（週一三五有飲料）
- **配置檔**：`beverage_schedule.json`（手動設定時間表）
- **OCR 自動**：`breakfast_notifier.py`（自動識別菜單）

### 3️⃣ 設定定時執行

```bash
crontab -e
# 每天早上 7:30 執行
30 7 * * 1-5 python3 /path/to/notifier_telegram.py
```

完整說明請看 `QUICKSTART.md`

## 進階功能建議

1. **智能提醒**
   - 前一天晚上提醒（可以提前準備）
   - 若連續多天有/無飲料，可調整通知頻率

2. **錯誤處理**
   - 網路失敗時發送預設提醒
   - 圖片無法下載時通知

3. **統計功能**
   - 記錄飲料供應頻率
   - 預測模式（例如週一通常有飲料）
