# 不需要額外 App 的通知方案

如果你不想使用 Telegram、Discord、LINE，這裡提供**不需要額外安裝 App** 的替代方案！

---

## 方案一：Email 通知（最推薦⭐）

### 為什麼推薦 Email？
- ✅ 每個人都有 Email，不需要裝 App
- ✅ 手機、電腦都能收
- ✅ 完全免費
- ✅ 設定簡單（5分鐘）

### 設定步驟

#### 步驟 1：取得 Gmail App 密碼

如果使用 Gmail，需要建立「應用程式密碼」（不是你的登入密碼）：

1. 前往 https://myaccount.google.com/security
2. 確認已開啟「兩步驟驗證」（如果沒有，需要先開啟）
3. 搜尋「應用程式密碼」或前往 https://myaccount.google.com/apppasswords
4. 選擇應用程式：「郵件」
5. 選擇裝置：「其他」，輸入「早餐提醒」
6. 點選「產生」
7. **複製 16 位數的密碼**（格式：xxxx xxxx xxxx xxxx）

**其他 Email 服務：**
- **Outlook/Hotmail**：可直接使用登入密碼，或到安全性設定產生應用程式密碼
- **Yahoo**：需要到帳戶安全性產生應用程式密碼
- **其他**：請參考該服務的 SMTP 設定說明

#### 步驟 2：設定程式

編輯 `notifier_email.py`：

```python
# Gmail 範例
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"      # 你的 Gmail
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"    # 剛才複製的應用程式密碼
RECEIVER_EMAIL = "your_email@gmail.com"    # 可以是同一個信箱

# Outlook 範例
# SMTP_SERVER = "smtp.office365.com"
# SMTP_PORT = 587
# SENDER_EMAIL = "your_email@outlook.com"
# SENDER_PASSWORD = "你的密碼或應用程式密碼"
# RECEIVER_EMAIL = "your_email@outlook.com"
```

#### 步驟 3：測試

```bash
python3 notifier_email.py
```

成功的話，你會收到一封提醒信！

#### 步驟 4：設定定時執行

```bash
crontab -e
# 每天早上 7:00 執行
0 7 * * 1-5 python3 /path/to/notifier_email.py
```

### 優點
- 📧 不需要裝任何 App
- 📱 手機會推播通知
- 💾 自動保存歷史記錄
- 🔍 可以搜尋過去的提醒

---

## 方案二：桌面通知

### 適合情況
- ✅ 電腦會在公司開機
- ✅ 想要在電腦螢幕看到彈出通知
- ✅ 不想用手機

### 設定步驟

#### 步驟 1：安裝套件（可選）

```bash
# 推薦安裝 plyer（跨平台支援）
pip3 install plyer

# 如果不安裝，程式會自動使用系統內建通知
```

#### 步驟 2：測試執行

```bash
python3 notifier_desktop.py
```

你的電腦右下角（Windows）或右上角（Mac）會彈出通知！

#### 步驟 3：設定定時執行

```bash
crontab -e
# 每天早上 7:30 執行
30 7 * * 1-5 python3 /path/to/notifier_desktop.py
```

### 注意事項
- 電腦必須開機才能顯示通知
- 如果電腦睡眠或關機，就看不到通知

---

## 方案三：網頁版（最簡單！）

### 特色
- ✅ 不需要任何帳號
- ✅ 開瀏覽器就能看
- ✅ 可以設為首頁或書籤
- ✅ 手機、電腦都能開

### 設定步驟

#### 步驟 1：產生網頁

```bash
python3 notifier_web.py
```

會產生 `breakfast_today.html` 檔案

#### 步驟 2：開啟網頁

用瀏覽器打開 `breakfast_today.html`，就能看到今天的提醒！

**設為瀏覽器首頁：**
- Chrome：設定 → 啟動時 → 開啟特定網頁
- 輸入：`file:///完整路徑/breakfast_today.html`

**或加入書籤：**
- 開啟檔案後，按 Ctrl+D (Windows) 或 Cmd+D (Mac) 加入書籤

#### 步驟 3：設定定時更新

```bash
crontab -e
# 每天早上 6:30 更新網頁
30 6 * * 1-5 python3 /path/to/notifier_web.py
```

### 進階：架設簡單網頁伺服器

如果想在手機也能看：

```bash
# 在專案目錄執行
python3 -m http.server 8080
```

然後在手機瀏覽器開啟：`http://你的電腦IP:8080/breakfast_today.html`

---

## 方案四：Slack Webhook

### 適合情況
- ✅ 公司有使用 Slack
- ✅ 想要在 Slack 收到提醒

### 設定步驟

#### 步驟 1：建立 Slack Webhook

1. 前往 https://api.slack.com/apps
2. 點選「Create New App」→「From scratch」
3. 輸入 App 名稱：「早餐提醒」
4. 選擇要安裝的 Workspace
5. 左側選單選擇「Incoming Webhooks」
6. 開啟「Activate Incoming Webhooks」
7. 點選「Add New Webhook to Workspace」
8. 選擇要發送通知的頻道
9. **複製 Webhook URL**

#### 步驟 2：設定程式

編輯 `notifier_slack.py`：

```python
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

#### 步驟 3：測試

```bash
python3 notifier_slack.py
```

Slack 頻道會收到訊息！

---

## 方案比較

| 方案 | 需要 App | 設定難度 | 手機通知 | 推薦度 |
|-----|---------|---------|---------|--------|
| **Email** | ✗ | ⭐⭐ | ✓ | ⭐⭐⭐⭐⭐ |
| **桌面通知** | ✗ | ⭐ | ✗ | ⭐⭐⭐ |
| **網頁版** | ✗ | ⭐ | ✓ (需手動開啟) | ⭐⭐⭐⭐ |
| **Slack** | ✓ (公司已有) | ⭐⭐ | ✓ | ⭐⭐⭐⭐ |

---

## 我的建議

### 情況 1：不想裝任何 App
→ 選擇 **Email**（最推薦）
- 手機會自動推播
- 不需要額外動作

### 情況 2：電腦會在公司開機
→ 選擇 **桌面通知**
- 螢幕直接彈出提醒
- 零設定（不裝 plyer 也能用）

### 情況 3：想要最簡單的
→ 選擇 **網頁版**
- 早上打開瀏覽器就看到
- 可以設為首頁

### 情況 4：公司有用 Slack
→ 選擇 **Slack Webhook**
- 整合進現有工作流程

---

## 常見問題

### Q1: Email 收不到？
- 檢查應用程式密碼是否正確（有空格要去掉）
- 檢查垃圾郵件資料夾
- 確認 SMTP 伺服器和埠號正確

### Q2: Gmail 應用程式密碼找不到？
- 需要先開啟兩步驟驗證
- 前往：https://myaccount.google.com/apppasswords

### Q3: 桌面通知沒出現？
- 檢查電腦是否開機
- Windows：確認「通知」權限已開啟
- Mac：系統偏好設定 → 通知

### Q4: 網頁版檔案在哪？
- 執行程式的目錄下
- 檔名：`breakfast_today.html`
- 可以搜尋檔案名稱找到

### Q5: 想在手機看網頁版？
方法 1：把檔案上傳到 Google Drive/Dropbox，開啟分享連結
方法 2：架設簡單網頁伺服器（見上方說明）
方法 3：用 Email 方案更簡單

---

## 混合使用

你可以同時使用多種方式！例如：

```bash
# 同時發送 Email 和桌面通知
python3 notifier_email.py && python3 notifier_desktop.py
```

或修改程式，在一個腳本中呼叫多個發送函數。

---

**選擇最適合你的方式，享受便利的早餐提醒！** 📧💻
