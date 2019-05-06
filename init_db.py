import sqlite3

database_file = 'upload_result.db'
create_query = "CREATE TABLE IF NOT EXISTS upload_result(date TEXT, result TEXT, path TEXT)"
with sqlite3.connect(database_file) as conn:
    c = conn.cursor()
    c.execute(create_query)