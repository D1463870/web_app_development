from . import get_db_connection

class User:
    @staticmethod
    def create(data):
        """
        新增一筆使用者記錄。
        參數:
            data (dict): 包含 email, password_hash
        回傳:
            int: 新增的資料 ID，若發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (data['email'], data['password_hash'])
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者記錄"""
        try:
            conn = get_db_connection()
            users = conn.execute("SELECT * FROM users").fetchall()
            conn.close()
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        """取得單筆使用者記錄"""
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None
            
    @staticmethod
    def get_by_email(email):
        """依據信箱取得使用者記錄 (登入時使用)"""
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    @staticmethod
    def update(id, data):
        """更新使用者記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE users SET email = ?, password_hash = ? WHERE id = ?",
                (data['email'], data['password_hash'], id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(id):
        """刪除使用者記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
