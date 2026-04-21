from flask import Blueprint, render_template, request, redirect, url_for, flash, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def index():
    """
    顯示系統首頁 / 儀表板：
    - 取得當月收支總計與預算使用比例
    - 組合圖表所需資料，渲染 dashboard/index.html
    """
    pass

@dashboard_bp.route('/budget', methods=['GET', 'POST'])
def budget():
    """
    預算設定：
    - GET: 顯示預算設定表單
    - POST: 更新當月預算金額
    """
    pass

@dashboard_bp.route('/export/csv', methods=['GET'])
def export_csv():
    """
    資料匯出：
    - 將符合條件的明細紀錄轉換為 CSV 格式供使用者下載
    """
    pass
