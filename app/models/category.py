import sqlite3

class Category:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path

    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, user_id, name, type, is_default=0):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO categories (user_id, name, type, is_default) VALUES (?, ?, ?, ?)',
                (user_id, name, type, is_default)
            )
            return cursor.lastrowid

    def get_all_by_user(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute(
                'SELECT * FROM categories WHERE user_id = ? OR is_default = 1 ORDER BY type, id',
                (user_id,)
            )
            return cursor.fetchall()
