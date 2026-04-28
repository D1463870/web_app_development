import sqlite3

def get_db_connection():
    """
    建立並回傳與 SQLite 資料庫的連線。
    預設使用 instance/database.db，並設定 row_factory 為 sqlite3.Row。
    """
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn
