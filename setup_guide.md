# 安裝與設定指南

## 一、環境準備

### 1. 選擇執行設備
因為菜單圖片僅限內網存取，你需要一台在公司內網的設備：
- 選項 A：公司電腦（需保持開機）
- 選項 B：樹莓派（推薦，便宜、省電、24小時運行）
- 選項 C：舊筆電/小主機

### 2. 安裝 Python
```bash
# 檢查是否已安裝 Python 3
python3 --version

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Windows
# 從 https://www.python.org/ 下載安裝
```

### 3. 安裝 Tesseract OCR（可選）

**如果要使用 OCR 自動識別，需要安裝：**

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-chi-tra

# macOS
brew install tesseract tesseract-lang

# Windows
# 從 https://github.com/UB-Mannheim/tesseract/wiki 下載安裝
# 安裝後需設定環境變數
```

**如果不想使用 OCR：**
- 可以使用簡易判斷方式（見程式碼中的 `check_beverage_simple`）
- 或改用人工確認方式

## 二、申請 LINE Notify Token

1. 前往 https://notify-bot.line.me/
2. 登入你的 LINE 帳號
3. 點選右上角的「個人頁面」
4. 點選「發行權杖」
5. 輸入權杖名稱（例如：早餐提醒）
6. 選擇接收通知的聊天室（建議選「透過 1 對 1 聊天接收 LINE Notify 的通知」）
7. 點選「發行」
8. **重要：複製並保存權杖**（只會顯示一次）

## 三、設定專案

### 1. 下載專案
```bash
cd ~
git clone <your-repo-url>
cd breakfast-beverage-alerts
```

### 2. 安裝 Python 套件
```bash
pip3 install -r requirements.txt
```

### 3. 設定 LINE Token
編輯 `breakfast_notifier.py`，將 `YOUR_LINE_NOTIFY_TOKEN_HERE` 替換成你的權杖：
```python
LINE_NOTIFY_TOKEN = "你的權杖"
```

### 4. 測試執行
```bash
python3 breakfast_notifier.py
```

如果成功，你應該會收到 LINE 通知！

## 四、設定定時執行

### Linux/Mac (使用 crontab)

```bash
# 編輯 crontab
crontab -e

# 加入以下內容（每天早上 7:30 執行）
30 7 * * * /usr/bin/python3 /home/your-username/breakfast-beverage-alerts/breakfast_notifier.py >> /home/your-username/breakfast-beverage-alerts/log.txt 2>&1

# 或者早上 7:00 執行
0 7 * * * /usr/bin/python3 /home/your-username/breakfast-beverage-alerts/breakfast_notifier.py >> /home/your-username/breakfast-beverage-alerts/log.txt 2>&1
```

**Crontab 時間格式說明：**
```
分 時 日 月 週
30 7 * * *  = 每天 7:30
0  7 * * *  = 每天 7:00
0  7 * * 1-5 = 週一到週五 7:00
```

### Windows (使用工作排程器)

1. 開啟「工作排程器」（Task Scheduler）
2. 點選「建立基本工作」
3. 名稱：早餐飲料提醒
4. 觸發程序：每天
5. 時間：早上 7:30
6. 動作：啟動程式
   - 程式或指令碼：`python.exe` 的完整路徑
   - 引數：`breakfast_notifier.py` 的完整路徑
   - 開始於：專案資料夾路徑
7. 完成設定

## 五、進階設定

### 1. 調整飲料關鍵字
根據你們公司的菜單內容，修改 `breakfast_notifier.py` 中的 `BEVERAGE_KEYWORDS`：
```python
BEVERAGE_KEYWORDS = [
    "飲料", "豆漿", "奶茶", "紅茶", "綠茶", "咖啡",
    "果汁", "牛奶", "米漿", "飲品", "茶", "汁"
]
```

### 2. 前一天晚上提醒
如果希望前一天晚上就收到提醒，可以改 crontab 時間：
```bash
# 每天晚上 9:00 提醒明天的早餐
0 21 * * * /usr/bin/python3 /path/to/breakfast_notifier.py
```

並修改通知訊息為「明天的早餐...」

### 3. 加入錯誤重試
在 `main()` 函數中加入重試邏輯，避免網路暫時失敗。

### 4. 記錄歷史資料
可以將每天的檢查結果寫入檔案或資料庫，分析飲料供應規律。

## 六、常見問題

### Q1: 收不到通知？
- 檢查 LINE Notify Token 是否正確
- 確認網路連線正常
- 查看程式執行 log

### Q2: OCR 識別率低？
- 確認繁體中文語言包已安裝
- 調整圖片預處理（增加對比度、去噪）
- 或改用簡易判斷方式

### Q3: 定時任務沒執行？
- 檢查 crontab 語法是否正確
- 確認 Python 路徑正確
- 查看系統 log：`grep CRON /var/log/syslog`

### Q4: 內網連線問題？
- 確認執行設備在公司內網
- 測試能否開啟菜單 URL
- 考慮使用 VPN 連回公司

## 七、替代方案

如果覺得技術實作太複雜，也可以考慮：

### 方案 A：手動版
1. 建立一個 Google 試算表或 Line Bot
2. 行政人員或志願者每天早上更新
3. 系統自動發送通知

### 方案 B：簡化思維
1. **永遠帶杯子** - 輕便矽膠折疊杯，放包包不佔空間
2. **保持兩個杯子** - 座位放一個，包包放一個
3. **設定習慣** - 每天都帶，不用想

這些方法不需要寫程式，也能解決問題！
