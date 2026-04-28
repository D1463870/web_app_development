from . import get_db_connection

class Record:
    @staticmethod
    def create(data):
        """
        新增一筆收支記錄。
        參數: data 包含 user_id, category_id, amount, date, note
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO records (user_id, category_id, amount, date, note) VALUES (?, ?, ?, ?, ?)",
                (data['user_id'], data['category_id'], data['amount'], data['date'], data.get('note', ''))
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating record: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有收支記錄"""
        try:
            conn = get_db_connection()
            records = conn.execute("SELECT * FROM records").fetchall()
            conn.close()
            return records
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []
            
    @staticmethod
    def get_by_month(user_id, month_year):
        """取得特定月份的收支記錄 (month_year 格式: YYYY-MM)"""
        try:
            conn = get_db_connection()
            records = conn.execute(
                '''SELECT r.*, c.name as category_name, c.type as category_type 
                   FROM records r 
                   JOIN categories c ON r.category_id = c.id 
                   WHERE r.user_id = ? AND r.date LIKE ? 
                   ORDER BY r.date DESC, r.id DESC''', 
                (user_id, f"{month_year}-%")
            ).fetchall()
            conn.close()
            return records
        except Exception as e:
            print(f"Error fetching monthly records: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        """取得單筆收支記錄"""
        try:
            conn = get_db_connection()
            record = conn.execute("SELECT * FROM records WHERE id = ?", (id,)).fetchone()
            conn.close()
            return record
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None

    @staticmethod
    def update(id, data):
        """更新收支記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE records SET category_id = ?, amount = ?, date = ?, note = ? WHERE id = ?",
                (data['category_id'], data['amount'], data['date'], data.get('note', ''), id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    @staticmethod
    def delete(id):
        """刪除收支記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM records WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
