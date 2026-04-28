from . import get_db_connection

class Budget:
    @staticmethod
    def create(data):
        """新增一筆預算記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO budgets (user_id, amount, month_year) VALUES (?, ?, ?)",
                (data['user_id'], data['amount'], data['month_year'])
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
            
    @staticmethod
    def set_budget(data):
        """設定預算：若該月預算已存在則更新，否則新增"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            existing = cursor.execute(
                "SELECT id FROM budgets WHERE user_id = ? AND month_year = ?",
                (data['user_id'], data['month_year'])
            ).fetchone()
            
            if existing:
                cursor.execute(
                    "UPDATE budgets SET amount = ? WHERE id = ?",
                    (data['amount'], existing['id'])
                )
                new_id = existing['id']
            else:
                cursor.execute(
                    "INSERT INTO budgets (user_id, amount, month_year) VALUES (?, ?, ?)",
                    (data['user_id'], data['amount'], data['month_year'])
                )
                new_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error setting budget: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有預算記錄"""
        try:
            conn = get_db_connection()
            budgets = conn.execute("SELECT * FROM budgets").fetchall()
            conn.close()
            return budgets
        except Exception as e:
            print(f"Error fetching budgets: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        """取得單筆預算記錄"""
        try:
            conn = get_db_connection()
            budget = conn.execute("SELECT * FROM budgets WHERE id = ?", (id,)).fetchone()
            conn.close()
            return budget
        except Exception as e:
            print(f"Error fetching budget: {e}")
            return None
            
    @staticmethod
    def get_by_month(user_id, month_year):
        """取得特定月份的預算"""
        try:
            conn = get_db_connection()
            budget = conn.execute(
                "SELECT * FROM budgets WHERE user_id = ? AND month_year = ?", 
                (user_id, month_year)
            ).fetchone()
            conn.close()
            return budget
        except Exception as e:
            print(f"Error fetching monthly budget: {e}")
            return None

    @staticmethod
    def update(id, data):
        """更新預算記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE budgets SET amount = ?, month_year = ? WHERE id = ?",
                (data['amount'], data['month_year'], id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating budget: {e}")
            return False

    @staticmethod
    def delete(id):
        """刪除預算記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM budgets WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting budget: {e}")
            return False
