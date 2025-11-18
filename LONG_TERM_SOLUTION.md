# 長期穩定解決方案

## 為什麼需要考慮長期方案？

LINE Notify 將於 2025/3/31 停止服務，我們需要一個**不會再停止服務**的長期方案。

---

## 🏆 最推薦：Email 通知

### 為什麼 Email 是最佳長期方案？

#### 1. 永不停止服務
- **Email 是網際網路基礎協議（SMTP）**，已存在 40+ 年
- 不依賴任何單一公司
- 即使 Gmail 倒閉，你換到 Outlook 或任何 Email 服務，程式碼不需要改

#### 2. 零服務商風險
| 服務 | 風險 |
|------|------|
| LINE Notify | ❌ 2025/3/31 停止服務 |
| Telegram | ⚠️ 需要 App，某些國家可能封鎖 |
| Discord | ⚠️ 需要 App，服務可能改變 |
| **Email (SMTP)** | ✅ **標準協議，永遠可用** |

#### 3. 完全免費、無限制
- Gmail：每天可發送 500 封（你只需要 1 封）
- Outlook：類似額度
- 不會有「超過額度要付費」的問題

#### 4. 符合所有需求
- ✅ 手機自動推播（不需要主動打開）
- ✅ 不用裝額外 App
- ✅ 任何地方都能收（出差、換手機、換公司都沒問題）
- ✅ 自動保存歷史記錄（可以回頭查詢）

---

## 📋 推薦的長期架構

```
公司內網電腦/樹莓派（定時執行）
  │
  ├─ 步驟 1：判斷今天是否有飲料
  │   ├─ 方案 A：簡單規則（週一三五有飲料）
  │   ├─ 方案 B：配置檔（手動維護）
  │   └─ 方案 C：OCR 識別（在內網執行）
  │
  └─ 步驟 2：發送 Email 通知
      └─ 使用 SMTP 標準協議
```

### 關鍵優勢：不需要處理內網圖片

**問題：** 你的菜單圖片在內網 (`http://srvap1.lungteng.com.tw/...`)

**為什麼不是問題：**
1. **判斷邏輯在內網執行**
   - 程式在內網電腦執行，可以直接存取內網圖片
   - OCR 識別在本地進行，不需要把圖片傳出去

2. **Email 只傳文字**
   - 不傳送圖片，只傳送判斷結果（有/無飲料）
   - 符合你的需求：「去餐廳前就知道要不要帶杯子」

3. **避免複雜的解決方案**
   - 不需要架設公開圖床
   - 不需要 VPN 或反向代理
   - 不需要申請固定 IP

---

## 🎯 實作建議

### 階段一：現在到 2025/3（過渡期）

**雙軌並行：LINE Notify + Email**

```bash
#!/bin/bash
# dual_notify.sh

# 判斷飲料狀態（共用邏輯）
python3 check_beverage.py > /tmp/result.txt

# 同時發送兩種通知
python3 simple_notifier.py      # LINE Notify（2025/3 前）
python3 notifier_email.py       # Email（永久可用）
```

**好處：**
- 現在就能測試 Email 方案是否好用
- 過渡期有雙重保障
- 習慣 Email 通知的感覺

**定時設定：**
```bash
crontab -e
# 每天早上 7:00 執行
0 7 * * 1-5 /path/to/dual_notify.sh
```

### 階段二：2025/3 之後

**只使用 Email**

```bash
crontab -e
# 每天早上 7:00 執行
0 7 * * 1-5 python3 /path/to/notifier_email.py
```

**好處：**
- 已經測試過半年，確定好用
- 零風險、零成本
- 永久可用、不會再遇到服務停止

---

## ⚙️ 判斷飲料的三種方式

### 方案 A：簡單規則（最簡單）

**適合：** 飲料供應有固定規律

```python
# 在 notifier_email.py 中
def check_beverage_by_day():
    today = datetime.now()
    weekday = today.weekday()

    # 週一、三、五有飲料
    has_beverage_days = [0, 2, 4]
    return weekday in has_beverage_days
```

**優點：**
- 寫死在程式裡，不會出錯
- 零維護成本

**缺點：**
- 如果規律改變，需要改程式碼

---

### 方案 B：配置檔（推薦⭐）

**適合：** 想要彈性調整

編輯 `beverage_schedule.json`：
```json
{
  "weekly_pattern": {
    "monday": true,
    "tuesday": false,
    "wednesday": true,
    "thursday": false,
    "friday": true,
    "saturday": false,
    "sunday": false
  },
  "special_dates": {
    "2025-12-25": false,
    "2025-01-01": false
  }
}
```

**優點：**
- 可以隨時調整，不用改程式
- 可以設定特殊日期（例如聖誕節沒飲料）

**缺點：**
- 需要手動維護配置檔

---

### 方案 C：OCR 自動識別（最高級）

**適合：** 想要全自動

```python
import pytesseract
from PIL import Image

def check_beverage_by_ocr():
    # 1. 下載內網圖片（程式在內網執行，可以直接下載）
    image = download_menu_image("http://srvap1.lungteng.com.tw/...")

    # 2. OCR 識別（在本地執行）
    text = pytesseract.image_to_string(image, lang='chi_tra')

    # 3. 檢查關鍵字
    beverage_keywords = ["飲料", "豆漿", "奶茶", "紅茶"]
    for keyword in beverage_keywords:
        if keyword in text:
            return True
    return False
```

**優點：**
- 全自動，不需要人工維護
- 圖片在內網處理，不需要傳出去

**缺點：**
- 需要安裝 tesseract-ocr
- OCR 辨識率可能不是 100%
- 複雜度較高

---

## 📧 Email 設定（Gmail 範例）

### 步驟 1：取得 Gmail App 密碼

1. 前往 https://myaccount.google.com/security
2. 確認已開啟「兩步驟驗證」
3. 搜尋「應用程式密碼」或前往 https://myaccount.google.com/apppasswords
4. 選擇「郵件」→「其他」→ 輸入「早餐提醒」
5. 點選「產生」
6. **複製 16 位數密碼**（格式：xxxx xxxx xxxx xxxx）

### 步驟 2：設定程式

編輯 `notifier_email.py`：

```python
# Gmail 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # App 密碼
RECEIVER_EMAIL = "your_email@gmail.com"  # 可以是同一個
```

### 步驟 3：測試

```bash
python3 notifier_email.py
```

成功的話，你會收到一封早餐提醒信！

---

## 🔄 從 LINE Notify 遷移到 Email

### 遷移計畫

**第 1 週：安裝測試**
```bash
# 設定 Email 通知
pip3 install -r requirements.txt
nano notifier_email.py  # 填入 Gmail 設定
python3 notifier_email.py  # 測試
```

**第 2-4 週：雙軌並行**
```bash
# 同時運行 LINE Notify 和 Email
crontab -e
# 0 7 * * 1-5 python3 /path/to/simple_notifier.py && python3 /path/to/notifier_email.py
```
- 觀察 Email 通知是否穩定
- 習慣新的通知方式

**2025/3 之後：完全切換**
```bash
# 只保留 Email
crontab -e
# 0 7 * * 1-5 python3 /path/to/notifier_email.py
```

---

## ❓ 常見問題

### Q1: 如果我的公司換 Email 系統怎麼辦？
A: 只需要改 SMTP 設定，程式邏輯完全不用動。SMTP 是標準協議，所有 Email 服務都支援。

### Q2: Gmail 會不會突然停止 SMTP 服務？
A: 機率極低。SMTP 是 Email 的基礎協議，如果 Gmail 停止，你可以馬上換到 Outlook、Yahoo 或任何 Email 服務，改 5 行設定就好。

### Q3: Email 會不會進垃圾郵件匣？
A: 因為是自己發給自己，不會。即使發給別人，可以在手機設定「標記為非垃圾郵件」。

### Q4: 如果我換手機號碼怎麼辦？
A: Email 不綁手機號碼，完全不影響。這也是 Email 比 LINE/Telegram 更長久的原因。

### Q5: 我可以同時發給多個人嗎？
A: 可以！修改 `RECEIVER_EMAIL` 為列表：
```python
RECEIVER_EMAIL = ["person1@gmail.com", "person2@gmail.com"]
```

---

## 🎁 進階功能

### 1. 前一天晚上提醒

```bash
# 每天晚上 9:00 提醒明天的早餐
0 21 * * * python3 /path/to/notifier_email.py --tomorrow
```

### 2. 只在有飲料時提醒

```python
if has_beverage:
    send_email(...)  # 只在有飲料時發送
```

### 3. 統計飲料供應頻率

```python
# 記錄每天的結果
import json
from datetime import datetime

history = []
history.append({
    "date": datetime.now().strftime("%Y-%m-%d"),
    "has_beverage": has_beverage
})

with open("history.json", "w") as f:
    json.dump(history, f)
```

幾個月後可以分析：週一通常有飲料嗎？

---

## 📊 方案比較總結

| 項目 | LINE Notify | LINE Bot | Telegram | Email |
|------|-------------|----------|----------|-------|
| **服務穩定性** | ❌ 2025/3 停止 | ⚠️ 可能改變 | ⚠️ 可能改變 | ✅ 永久標準 |
| **設定難度** | ⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **需要 App** | ✗ | ✗ | ✓ | ✗ |
| **手機推播** | ✓ | ✓ | ✓ | ✓ |
| **免費額度** | 無限 | 200則/月 | 無限 | 500則/日 |
| **處理內網圖片** | ✓ 直接上傳 | ❌ 需要公開網址 | ⚠️ 需要公開網址 | ✓ 只傳文字結果 |
| **長期推薦度** | ❌ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 最終建議

**短期（現在到 2025/3）：**
- 繼續用 LINE Notify（簡單、好用）
- 同時設定 Email（測試、習慣）

**長期（2025/3 之後）：**
- **只用 Email**
- 理由：永久可用、零風險、零成本

**判斷方式：**
- 簡單規則（週一三五有飲料）
- 或配置檔（手動維護）

**不需要：**
- ❌ 不需要傳送內網圖片到外部
- ❌ 不需要架設公開圖床
- ❌ 不需要擔心服務停止

---

選擇 Email，一勞永逸！📧
