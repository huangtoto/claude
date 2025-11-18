# 快速開始指南

## 最快 5 分鐘設定完成！

### 步驟 1️⃣：取得 LINE Notify Token (2分鐘)

1. 用手機或電腦開啟 https://notify-bot.line.me/
2. 登入 LINE 帳號
3. 點選「個人頁面」→「發行權杖」
4. 權杖名稱輸入：`早餐提醒`
5. 選擇「透過 1 對 1 聊天接收通知」
6. 按「發行」並**複製權杖**（很重要！只會顯示一次）

### 步驟 2️⃣：下載並設定程式 (2分鐘)

```bash
# 1. 下載程式（如果還沒有的話）
git clone <your-repo-url>
cd breakfast-beverage-alerts

# 2. 安裝套件
pip3 install -r requirements.txt

# 3. 編輯設定檔，貼上你的 LINE Token
nano simple_notifier.py
# 找到 LINE_NOTIFY_TOKEN = "YOUR_LINE_NOTIFY_TOKEN_HERE"
# 改成你的權杖，例如：
# LINE_NOTIFY_TOKEN = "AbCdEf123456..."
```

### 步驟 3️⃣：測試執行 (30秒)

```bash
python3 simple_notifier.py
```

✓ 如果你的 LINE 收到訊息，就成功了！

### 步驟 4️⃣：設定每天自動執行 (30秒)

**Linux/Mac:**
```bash
crontab -e
# 加入這一行（每天早上 7:30 執行）
30 7 * * 1-5 cd /home/你的使用者名稱/breakfast-beverage-alerts && /usr/bin/python3 simple_notifier.py
```

**Windows:**
1. 開啟「工作排程器」
2. 建立基本工作 → 名稱：早餐提醒
3. 觸發：每天早上 7:30，週一到週五
4. 動作：執行 `python simple_notifier.py`

---

## 🎯 三種使用方式

### 方式 A：簡單規則（最簡單）

直接修改 `simple_notifier.py` 的規則：

```python
# 週一、三、五有飲料
has_beverage_days = [0, 2, 4]  # 0=週一, 2=週三, 4=週五
```

### 方式 B：配置檔（推薦）

編輯 `beverage_schedule.json`：

```json
{
  "weekly_pattern": {
    "monday": true,      # 週一有飲料
    "tuesday": false,    # 週二沒有
    "wednesday": true,   # 週三有
    "thursday": false,
    "friday": true
  }
}
```

### 方式 C：OCR 自動識別（進階）

想要全自動？使用 `breakfast_notifier.py`（需要安裝 tesseract-ocr）

詳細說明請看 `setup_guide.md`

---

## 📱 收到的通知範例

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
0 21 * * 0-4 python3 simple_notifier.py  # 週日到週四晚上 9:00
```

並修改程式訊息為「明天的早餐」

### 想要更早提醒（7:00）？

```bash
0 7 * * 1-5 python3 simple_notifier.py
```

### 只想在有飲料時收到提醒？

修改 `simple_notifier.py`，只在 `has_beverage == True` 時發送。

---

## ❓ 遇到問題？

**收不到通知？**
- 檢查 LINE Token 是否正確
- 執行程式看有無錯誤訊息

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
