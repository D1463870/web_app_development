import sqlite3

class Budget:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path

    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def set_budget(self, user_id, month_year, amount):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO budgets (user_id, amount, month_year)
                   VALUES (?, ?, ?)
                   ON CONFLICT(user_id, month_year)
                   DO UPDATE SET amount=excluded.amount''',
                (user_id, amount, month_year)
            )
            return cursor.lastrowid

    def get_by_month(self, user_id, month_year):
        with self.get_db() as conn:
            cursor = conn.execute(
                'SELECT * FROM budgets WHERE user_id = ? AND month_year = ?',
                (user_id, month_year)
            )
            return cursor.fetchone()
