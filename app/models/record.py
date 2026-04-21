import sqlite3

class Record:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path

    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, user_id, category_id, amount, date, note=''):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO records (user_id, category_id, amount, date, note)
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, category_id, amount, date, note)
            )
            return cursor.lastrowid

    def get_by_month(self, user_id, year_month):
        with self.get_db() as conn:
            cursor = conn.execute(
                '''SELECT r.*, c.name as category_name, c.type as category_type
                   FROM records r
                   JOIN categories c ON r.category_id = c.id
                   WHERE r.user_id = ? AND r.date LIKE ?
                   ORDER BY r.date DESC, r.id DESC''',
                (user_id, f"{year_month}-%")
            )
            return cursor.fetchall()

    def update(self, record_id, category_id, amount, date, note):
        with self.get_db() as conn:
            conn.execute(
                '''UPDATE records
                   SET category_id = ?, amount = ?, date = ?, note = ?
                   WHERE id = ?''',
                (category_id, amount, date, note, record_id)
            )

    def delete(self, record_id):
        with self.get_db() as conn:
            conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
