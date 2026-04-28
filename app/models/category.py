from . import get_db_connection

class Category:
    @staticmethod
    def create(data):
        """
        新增一筆分類記錄。
        參數:
            data (dict): 包含 user_id, name, type, is_default
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (user_id, name, type, is_default) VALUES (?, ?, ?, ?)",
                (data.get('user_id'), data['name'], data['type'], data.get('is_default', 0))
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有分類記錄"""
        try:
            conn = get_db_connection()
            categories = conn.execute("SELECT * FROM categories").fetchall()
            conn.close()
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
            
    @staticmethod
    def get_all_by_user(user_id):
        """取得特定使用者的所有分類 (包含系統預設)"""
        try:
            conn = get_db_connection()
            categories = conn.execute(
                "SELECT * FROM categories WHERE user_id = ? OR user_id IS NULL OR is_default = 1 ORDER BY type, id", 
                (user_id,)
            ).fetchall()
            conn.close()
            return categories
        except Exception as e:
            print(f"Error fetching categories for user: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        """取得單筆分類記錄"""
        try:
            conn = get_db_connection()
            category = conn.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()
            conn.close()
            return category
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None

    @staticmethod
    def update(id, data):
        """更新分類記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE categories SET name = ?, type = ? WHERE id = ?",
                (data['name'], data['type'], id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    @staticmethod
    def delete(id):
        """刪除分類記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM categories WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
