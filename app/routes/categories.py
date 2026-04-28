from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.category import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    
    if request.method == 'POST':
        name = request.form.get('name')
        c_type = request.form.get('type')
        
        if not name or not c_type:
            flash('名稱與類型為必填', 'danger')
        else:
            Category.create({
                'user_id': user_id,
                'name': name,
                'type': c_type,
                'is_default': 0
            })
            flash('分類新增成功', 'success')
            return redirect(url_for('categories.index'))
            
    categories = Category.get_all_by_user(user_id)
    return render_template('categories/index.html', categories=categories)

@categories_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    category = Category.get_by_id(id)
    
    if not category or (category['user_id'] != user_id and category['is_default'] != 1):
        flash('無權限刪除', 'danger')
    elif category['is_default'] == 1:
        flash('預設分類無法刪除', 'danger')
    else:
        Category.delete(id)
        flash('分類已刪除', 'success')
        
    return redirect(url_for('categories.index'))
