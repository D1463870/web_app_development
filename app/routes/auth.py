from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('信箱與密碼為必填欄位', 'danger')
            return redirect(url_for('auth.register'))
            
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('此信箱已被註冊', 'danger')
            return redirect(url_for('auth.register'))
            
        hashed_password = generate_password_hash(password)
        user_id = User.create({'email': email, 'password_hash': hashed_password})
        
        if user_id:
            session['user_id'] = user_id
            flash('註冊成功！', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('註冊失敗，請稍後再試', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('登入成功！', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('信箱或密碼錯誤', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已登出', 'info')
    return redirect(url_for('auth.login'))
