from flask import Blueprint, render_template, request, redirect, url_for, flash, session

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['GET', 'POST'])
def index():
    """
    處理分類清單與新增分類：
    - GET: 取得所有預設與自訂分類，渲染 categories/index.html
    - POST: 新增一筆自訂分類
    """
    pass

@categories_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除自訂分類：
    - 若為預設分類則不可刪除
    - 重導向回分類清單
    """
    pass
