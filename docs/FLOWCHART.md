# 個人記帳簿系統流程圖 (Flowchart)

> **說明**：由於目前目錄中尚未建立 `ARCHITECTURE.md`，以下流程圖與對照表將基於 `PRD.md` 定義的需求，以及 Flask + SQLite 的基本架構假設進行繪製。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從開啟系統到各個核心操作動作的路徑。

```mermaid
flowchart TD
    A([使用者開啟網頁]) --> B{是否已有帳號且登入？}
    B -- 否 --> C[登入 / 註冊頁面]
    C -->|驗證成功| D((系統首頁 - 當月收支總覽))
    B -- 是 --> D
    
    D --> E{要執行什麼操作？}
    
    E -- 新增記帳 --> F[填寫收支表單]
    F -->|送出表單| G[儲存紀錄]
    G --> D
    
    E -- 查看明細/編輯/刪除 --> H[進入收支明細清單頁]
    H --> I{要對單筆操作？}
    I -- 編輯 --> J[編輯表單]
    J -->|更新| H
    I -- 刪除 --> K[確認刪除]
    K -->|刪除完成| H
    H -->|返回| D
    
    E -- 查看圖表分析 --> L[進入視覺圖表頁面]
    L --> M[切換月份/類別篩選]
    M --> L
    L -->|返回| D
    
    E -- 分類自訂 --> N[進入分類管理]
    N -->|新增/修改/刪除分類| N
    N -->|返回| D
    
    E -- 預算設定 --> O[進入預算設定與提醒區]
    O -->|儲存最新預算| D
    
    E -- 資料匯出 --> P[匯出 CSV]
    P --> D
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述核心操作「使用者點擊新增一筆收支紀錄」從前端到資料庫的資料流與技術處理步驟。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (網頁)
    participant Flask as Flask Route
    participant DB as SQLite 資料庫
    
    User->>Browser: 在表單輸入金額、日期、分類並點擊新增
    Browser->>Flask: POST /records (攜帶 Form Data)
    activate Flask
    Flask->>Flask: 驗證使用者登入狀態 (Session)
    Flask->>Flask: 驗證輸入資料格式 (必填、金額為數字等)
    Flask->>DB: INSERT INTO records (user_id, amount, ...)
    activate DB
    DB-->>Flask: 新增成功，回傳操作結果
    deactivate DB
    Flask-->>Browser: HTTP 302 Redirect 回列表或首頁
    deactivate Flask
    Browser-->>User: 重新渲染畫面，顯示新增成功的最新紀錄
```

## 3. 功能清單對照表

以下為基於 PRD 整理的主要功能與預期開發的 Route 端點、HTTP Method 對照：

| 功能項目 | API / URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **會員註冊** | `/register` | GET, POST | GET: 顯示註冊頁面 <br> POST: 處理帳號建立 |
| **會員登入** | `/login` | GET, POST | GET: 顯示登入頁面 <br> POST: 驗證密碼寫入 Session |
| **會員登出** | `/logout` | GET | 清除 Session 並導向登入頁 |
| **系統首頁** | `/` | GET | 顯示當月總結區塊與快速新增表單 |
| **新增紀錄** | `/records` | POST | 接收新增收支的表單資料 |
| **收支明細清單** | `/records` | GET | 列出使用者所有的收支紀錄（支援 Query 參數做月份過濾）|
| **編輯單筆紀錄** | `/records/<id>/edit` | GET, POST | GET: 取得單筆資料並顯示編輯表單 <br> POST: 儲存變更 |
| **刪除單筆紀錄** | `/records/<id>/delete`| POST | 刪除單一紀錄（為防 CSRF 通常避免使用 GET 刪除） |
| **圖表分析** | `/dashboard` | GET | 呈現統計圓餅圖/長條圖 |
| **分類管理** | `/categories` | GET, POST | 列出與新增自訂分類 |
| **預算設定** | `/budget` | GET, POST | 顯示與更新每月預算設定 |
| **匯出資料** | `/export/csv` | GET | 產生該用戶紀錄的 CSV 供下載 |
