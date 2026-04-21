# 路由與頁面設計文件 (API Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **系統首頁** | GET | `/` | `templates/dashboard/index.html` | 登入後首頁，顯示當月總覽與快速新增 |
| **註冊頁面** | GET, POST | `/register` | `templates/auth/register.html` | 顯示註冊表單與處理註冊邏輯 |
| **登入頁面** | GET, POST | `/login` | `templates/auth/login.html` | 顯示登入表單與處理登入邏輯 |
| **登出** | GET | `/logout` | — | 執行登出並重導向至登入頁 |
| **收支列表** | GET | `/records` | `templates/records/index.html` | 列出收支明細，支援參數篩選 |
| **新增記帳** | POST | `/records` | — | 接收並儲存收支，重導向回列表或首頁 |
| **編輯記帳頁面** | GET | `/records/<id>/edit` | `templates/records/edit.html` | 顯示收支編輯表單 |
| **更新記帳** | POST | `/records/<id>/update` | — | 接收並更新收支紀錄，重導向 |
| **刪除記帳** | POST | `/records/<id>/delete` | — | 刪除單筆紀錄，重導向 |
| **分類列表** | GET, POST | `/categories` | `templates/categories/index.html` | 列出並允許新增自訂分類 |
| **刪除分類** | POST | `/categories/<id>/delete`| — | 刪除自訂分類，重導向 |
| **預算設定** | GET, POST | `/budget` | `templates/dashboard/budget.html` | 設定當月預算金額 |
| **匯出資料** | GET | `/export/csv` | — | 將明細轉為 CSV 下載 |

## 2. 每個路由的詳細說明

### Auth 認證群組 (`auth.py`)
- **GET /register**：渲染註冊畫面。
- **POST /register**：輸入 `email`, `password_hash`。邏輯：檢查 Email 重複、密碼加密、呼叫 `User.create()`、存入 Session、重導向至首頁。
- **GET /login**：渲染登入畫面。
- **POST /login**：輸入 `email`, `password_hash`。邏輯：校對密碼、存入 Session、重導向至首頁。若失敗則閃存 (flash) 錯誤訊息。
- **GET /logout**：邏輯：清除 Session，重導向至 `/login`。

### Records 收支紀錄群組 (`records.py`)
- **GET /records**：輸入 URL 參數 `month` 或無（預設當月）。邏輯：呼叫 `Record.get_by_month()`。輸出：渲染明細列表。
- **POST /records**：輸入表單 `category_id`, `amount`, `date`, `note`。邏輯：驗證資料後 `Record.create()`，重導向回列表。
- **GET /records/<id>/edit**：邏輯：取得單筆紀錄，若無則 404；若非本人的資料則拒絕。渲染附帶原值的編輯表單。
- **POST /records/<id>/update**：邏輯：驗證資料、`Record.update()`，重導向回列表。
- **POST /records/<id>/delete**：邏輯：`Record.delete()`，閃存「刪除成功」，重導向回列表。

### Categories 分類對照群組 (`categories.py`)
- **GET, POST /categories**：
  - GET：呼叫 `Category.get_all_by_user()` 渲染清單。
  - POST：接收 `name`, `type`，呼叫 `Category.create()` 新增自訂分類，並重導向回本頁。
- **POST /categories/<id>/delete**：邏輯：檢查是否被紀錄佔用或是否為系統預設，允許後刪除。

### Dashboard 首頁與全域群組 (`dashboard.py`)
- **GET /**：邏輯：綜合取得當月收支與當月預算，組合圓餅圖所需資料傳至前端渲染 `index.html`。
- **GET, POST /budget**：
  - GET：渲染預算設定頁。
  - POST：接收 `amount`, `month_year`，呼叫 `Budget.set_budget()`，重導向首頁。
- **GET /export/csv**：邏輯：取得過往紀錄，產生 CSV 檔案 `Response` (mimetype=`text/csv`)。

## 3. Jinja2 模板清單

所有檔案皆繼承自 `templates/base.html`：

- `templates/base.html` (核心佈局、Nav 導覽列)
- `templates/auth/login.html` (登入)
- `templates/auth/register.html` (註冊)
- `templates/dashboard/index.html` (首頁儀表板 / 圖表)
- `templates/dashboard/budget.html` (設定預算)
- `templates/records/index.html` (明細清單 + 篩選列)
- `templates/records/edit.html` (單筆編輯畫面)
- `templates/categories/index.html` (分類與新增頁面)
