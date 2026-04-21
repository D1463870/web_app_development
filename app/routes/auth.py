from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊：
    - GET: 顯示註冊表單
    - POST: 接收表單資料，建立新 User，並重導向
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入：
    - GET: 顯示登入表單
    - POST: 驗證帳密，將 user_id 寫入 session
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理登出：清除 session 並重導向至登入頁
    """
    pass
