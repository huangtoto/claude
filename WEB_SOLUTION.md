# 網頁方案 - 查看完整菜單

## 你的新需求

1. ✅ 不想用 Email（需要主動打開）
2. ✅ 沒有寄信服務
3. ✅ 希望是網址方案（開瀏覽器就能看）
4. ✅ 希望能外連（最好），內網也可以
5. ✅ **週五和週一收到完整菜單**（想知道餐點內容）

---

## 🌐 方案一：內網網頁伺服器（最簡單）

### 特色
- ✅ 設定超簡單（3分鐘）
- ✅ 不需要上傳到外部
- ✅ 手機連公司 Wi-Fi 就能看
- ⚠️ 在外面看不到（需要在公司網路）

### 快速設定

#### 步驟 1：安裝 Flask
```bash
pip3 install flask
```

#### 步驟 2：啟動伺服器
```bash
python3 web_server.py
```

會顯示：
```
早餐菜單網頁伺服器
==================================================

✓ 伺服器已啟動！

請在瀏覽器開啟以下網址：
  內網電腦: http://localhost:5000
  同網段裝置: http://你的電腦IP:5000

查詢電腦 IP 位址：
  Windows: ipconfig
  Linux/Mac: ifconfig
```

#### 步驟 3：查詢電腦 IP

**Windows:**
```bash
ipconfig
# 找到「IPv4 位址」，例如：192.168.1.100
```

**Mac/Linux:**
```bash
ifconfig
# 或
ip addr
# 找到類似 192.168.1.100 的 IP
```

#### 步驟 4：手機開啟網頁

在手機瀏覽器輸入：`http://192.168.1.100:5000`

**加到主畫面：**
- iOS Safari：點選「分享」→「加入主畫面」
- Android Chrome：點選「選單」→「加到主畫面」

### 設定開機自動啟動

**Windows（使用工作排程器）:**
1. 開啟「工作排程器」
2. 建立基本工作 → 名稱：菜單伺服器
3. 觸發程序：「電腦啟動時」
4. 動作：啟動程式
   - 程式：`python.exe` 的完整路徑
   - 引數：`C:\path\to\web_server.py`

**Linux/Mac（使用 systemd 或 launchd）:**

創建 `menu_server.service`:
```bash
[Unit]
Description=Breakfast Menu Server

[Service]
ExecStart=/usr/bin/python3 /path/to/web_server.py
Restart=always
User=你的使用者名稱

[Install]
WantedBy=multi-user.target
```

啟用：
```bash
sudo systemctl enable menu_server
sudo systemctl start menu_server
```

---

## 🌍 方案二：外連網頁（可在任何地方開啟）

### 特色
- ✅ 在家也能看
- ✅ 出差也能看
- ✅ 不需要連公司 Wi-Fi
- ⚠️ 需要設定雲端服務（約 10 分鐘）

### 使用 Imgur 圖床（推薦）

#### 為什麼選 Imgur？
- 完全免費
- 不需要登入就能上傳
- 圖片永久保存
- 產生公開網址

#### 步驟 1：申請 Imgur API

1. 前往 https://api.imgur.com/oauth2/addclient
2. 登入 Imgur 帳號（或註冊一個）
3. 填寫表單：
   - Application name: `Breakfast Menu`
   - Authorization type: 選擇「**Anonymous usage without user authorization**」
   - Email: 你的 Email
   - Description: `Upload breakfast menu`
4. 送出後會得到 **Client ID**（長得像：`abc123def456`）

#### 步驟 2：設定程式

編輯 `upload_to_cloud.py`：
```python
IMGUR_CLIENT_ID = "abc123def456"  # 貼上你的 Client ID
```

#### 步驟 3：測試上傳

```bash
python3 upload_to_cloud.py
```

成功的話會顯示：
```
✓ 上傳成功！
  公開網址: https://i.imgur.com/xxxxx.jpg
```

這個網址可以在**任何地方**開啟！

#### 步驟 4：設定定時上傳（週五和週一）

```bash
crontab -e

# 每週五和週一早上 7:00 上傳
0 7 * * 1,5 python3 /path/to/upload_to_cloud.py
```

---

## 📱 方案三：週五/週一自動通知 + 外連網址

### 特色
- ✅ 週五和週一自動收到通知
- ✅ 通知包含公開網址
- ✅ 可以看到完整菜單圖片
- ✅ 隨時都能開啟網址查看

### 設定步驟

#### 1. 選擇通知方式

編輯 `schedule_notification.py`：

```python
# 選擇你要用的通知方式
USE_TELEGRAM = True   # 推薦
USE_DISCORD = False
USE_EMAIL = False
```

#### 2. 填入設定

**如果用 Telegram：**
```python
TELEGRAM_BOT_TOKEN = "你的Bot Token"
TELEGRAM_CHAT_ID = "你的Chat ID"
```

（設定方式見 `NOTIFICATION_SETUP.md`）

#### 3. 填入 Imgur Client ID

```python
IMGUR_CLIENT_ID = "你的Client ID"
```

#### 4. 測試執行

```bash
# 測試（會檢查今天是否為週五/週一）
python3 schedule_notification.py
```

#### 5. 設定定時執行

```bash
crontab -e

# 每天早上 7:00 執行（程式會自動判斷是否為週五/週一）
0 7 * * * python3 /path/to/schedule_notification.py

# 或只在週五和週一執行
0 7 * * 1,5 python3 /path/to/schedule_notification.py
```

### 收到的通知範例

**Telegram:**
```
📅 11/18 週一 早餐菜單

🍳 本週菜單已更新！
點選下方連結查看完整菜單：
https://i.imgur.com/xxxxx.jpg

💡 可以將連結加入書籤，方便隨時查看
```

並附上菜單圖片（直接在 Telegram 中顯示）

---

## 🔄 方案比較

| 項目 | 內網伺服器 | 外連網址 | 週五/週一通知 |
|------|-----------|---------|--------------|
| **設定難度** | ⭐ 超簡單 | ⭐⭐ 簡單 | ⭐⭐ 簡單 |
| **外部存取** | ✗ | ✓ | ✓ |
| **自動通知** | ✗ | ✗ | ✓ |
| **看完整菜單** | ✓ | ✓ | ✓ |
| **適合** | 在公司看 | 任何地方看 | 主動推送 |

---

## 💡 我的建議

### 情境 1：只在公司需要看

**選擇：內網伺服器**

```bash
# 1. 啟動伺服器（開機自動）
python3 web_server.py

# 2. 手機加入書籤
http://192.168.1.100:5000
```

**優點：**
- 超簡單（3分鐘搞定）
- 不需要外部服務
- 圖片自動更新

---

### 情境 2：希望在家也能看

**選擇：外連網址 + 週五/週一通知**

```bash
# 設定定時上傳並通知
crontab -e
0 7 * * 1,5 python3 /path/to/schedule_notification.py
```

**結果：**
- 週五和週一早上收到 Telegram 通知
- 通知包含公開網址和圖片
- 網址可以隨時開啟（在家、出差都可以）

**優點：**
- 主動推送，不會忘記
- 外連網址，隨時可看
- 看到完整菜單內容

---

## 🎯 推薦配置

### 配置 A：極簡方案（內網）

```bash
# 只需要一行
python3 web_server.py
```

然後手機加書籤：`http://你的電腦IP:5000`

---

### 配置 B：完整方案（外連 + 通知）

**1. 申請 Imgur API（5分鐘）**
- 前往 https://api.imgur.com/oauth2/addclient
- 取得 Client ID

**2. 設定 Telegram Bot（5分鐘）**
- 跟 @BotFather 建立 Bot
- 取得 Token 和 Chat ID

**3. 設定定時執行**
```bash
crontab -e
# 每週五和週一早上 7:00
0 7 * * 1,5 python3 /path/to/schedule_notification.py
```

**結果：**
- ✅ 週五早上收到本週菜單
- ✅ 週一早上收到本週菜單
- ✅ 包含完整圖片和公開網址
- ✅ 隨時都能開啟網址查看

---

## ❓ 常見問題

### Q1: 為什麼選週五和週一？
A: 週五可以看下週菜單，週一再看一次本週菜單，避免忘記。

### Q2: 內網伺服器電腦關機怎麼辦？
A: 如果電腦關機，網頁就打不開。建議：
- 方案 A：用樹莓派或舊電腦 24 小時運行
- 方案 B：改用外連方案（上傳到 Imgur）

### Q3: Imgur 圖片會過期嗎？
A: Imgur 圖片永久保存，不會過期。即使舊的圖片還是能開。

### Q4: 可以自動刪除舊圖片嗎？
A: Imgur 有 API 可以刪除，但建議保留（不佔空間，也不收費）。如果真的要刪，可以修改程式在上傳新圖時刪除舊圖。

### Q5: 可以同時用內網和外連嗎？
A: 可以！
- 在公司用內網伺服器（速度快）
- 在家用外連網址（隨時可看）

### Q6: 如果公司網路很慢，Imgur 上傳會失敗嗎？
A: 可能會。如果遇到這個問題：
- 增加 timeout 時間
- 或改用其他圖床服務（ImgBB、Postimages）
- 或只用內網方案

---

## 🚀 快速開始

### 最快方案（3分鐘）- 內網

```bash
# 1. 安裝 Flask
pip3 install flask

# 2. 啟動伺服器
python3 web_server.py

# 3. 手機開啟
http://你的電腦IP:5000
```

完成！

### 完整方案（15分鐘）- 外連 + 通知

```bash
# 1. 申請 Imgur API
https://api.imgur.com/oauth2/addclient

# 2. 設定 Telegram Bot
跟 @BotFather 對話

# 3. 填入設定
nano schedule_notification.py

# 4. 測試
python3 schedule_notification.py

# 5. 設定定時
crontab -e
0 7 * * 1,5 python3 /path/to/schedule_notification.py
```

完成！

---

選擇最適合你的方案，開始使用吧！🍳
