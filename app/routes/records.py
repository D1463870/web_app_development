from flask import Blueprint, render_template, request, redirect, url_for, flash, session

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/', methods=['GET'])
def index():
    """
    取得收支紀錄清單：
    - 支援依據月份或條件篩選
    - 渲染 records/index.html
    """
    pass

@records_bp.route('/', methods=['POST'])
def create():
    """
    接收新增收支的表單：
    - 驗證必填並呼叫 Record.create()
    - 成功後重導向回列表或首頁
    """
    pass

@records_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    顯示單筆紀錄的編輯表單：
    - 取得該筆資料，若不屬於該用戶則報錯
    - 渲染 records/edit.html
    """
    pass

@records_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    處理單筆紀錄更新：
    - 接收表單更新欄位
    - 重導向回列表
    """
    pass

@records_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除單筆紀錄：
    - 呼叫 Record.delete()
    - 重導向回列表
    """
    pass
