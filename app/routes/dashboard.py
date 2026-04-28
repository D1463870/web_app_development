from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from app.models.record import Record
from app.models.budget import Budget
from datetime import datetime
import csv
import io

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    now = datetime.now()
    month_year = now.strftime('%Y-%m')
    
    records = Record.get_by_month(user_id, month_year)
    budget = Budget.get_by_month(user_id, month_year)
    
    total_expense = sum(r['amount'] for r in records if r['category_type'] == 'expense')
    total_income = sum(r['amount'] for r in records if r['category_type'] == 'income')
    
    budget_amount = budget['amount'] if budget else 0
    budget_usage = (total_expense / budget_amount * 100) if budget_amount > 0 else 0
    
    return render_template('dashboard/index.html', 
                           records=records, 
                           total_expense=total_expense,
                           total_income=total_income,
                           budget_amount=budget_amount,
                           budget_usage=budget_usage,
                           month_year=month_year)

@dashboard_bp.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    now = datetime.now()
    month_year = now.strftime('%Y-%m')
    
    if request.method == 'POST':
        amount = request.form.get('amount')
        if not amount:
            flash('請輸入預算金額', 'danger')
            return redirect(url_for('dashboard.budget'))
            
        Budget.set_budget({
            'user_id': user_id,
            'amount': float(amount),
            'month_year': month_year
        })
        flash('預算設定成功', 'success')
        return redirect(url_for('dashboard.index'))
        
    current_budget = Budget.get_by_month(user_id, month_year)
    return render_template('dashboard/budget.html', budget=current_budget)

@dashboard_bp.route('/export/csv', methods=['GET'])
def export_csv():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    records = Record.get_all()
    user_records = [r for r in records if r['user_id'] == user_id]
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category ID', 'Amount', 'Note'])
    for r in user_records:
        writer.writerow([r['date'], r['category_id'], r['amount'], r['note']])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=records.csv"}
    )
