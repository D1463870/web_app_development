from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.record import Record
from app.models.category import Category
from datetime import datetime

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    month_year = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    records = Record.get_by_month(user_id, month_year)
    categories = Category.get_all_by_user(user_id)
    
    return render_template('records/index.html', records=records, categories=categories, current_month=month_year)

@records_bp.route('/', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    category_id = request.form.get('category_id')
    amount = request.form.get('amount')
    date = request.form.get('date')
    note = request.form.get('note')
    
    if not category_id or not amount or not date:
        flash('分類、金額與日期為必填', 'danger')
        return redirect(url_for('records.index'))
        
    Record.create({
        'user_id': user_id,
        'category_id': category_id,
        'amount': float(amount),
        'date': date,
        'note': note
    })
    flash('新增紀錄成功', 'success')
    return redirect(url_for('records.index'))

@records_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    record = Record.get_by_id(id)
    
    if not record or record['user_id'] != user_id:
        flash('找不到該紀錄或無權限編輯', 'danger')
        return redirect(url_for('records.index'))
        
    categories = Category.get_all_by_user(user_id)
    return render_template('records/edit.html', record=record, categories=categories)

@records_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    record = Record.get_by_id(id)
    
    if not record or record['user_id'] != user_id:
        flash('無權限編輯此紀錄', 'danger')
        return redirect(url_for('records.index'))
        
    Record.update(id, {
        'category_id': request.form.get('category_id'),
        'amount': float(request.form.get('amount')),
        'date': request.form.get('date'),
        'note': request.form.get('note')
    })
    flash('更新成功', 'success')
    return redirect(url_for('records.index'))

@records_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    record = Record.get_by_id(id)
    
    if not record or record['user_id'] != user_id:
        flash('無權限刪除此紀錄', 'danger')
    else:
        Record.delete(id)
        flash('刪除成功', 'success')
        
    return redirect(url_for('records.index'))
