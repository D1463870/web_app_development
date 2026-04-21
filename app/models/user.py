import sqlite3

class User:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path

    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, email, password_hash):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            return cursor.lastrowid

    def get_by_id(self, user_id):
        with self.get_db() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()

    def get_by_email(self, email):
        with self.get_db() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
            return cursor.fetchone()
