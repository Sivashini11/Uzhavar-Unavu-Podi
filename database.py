import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id TEXT,

    customer_name TEXT,

    phone TEXT,

    address TEXT,

    product TEXT,

    weight TEXT,

    quantity INTEGER,

    amount INTEGER,

    status TEXT

)
""")

conn.commit()

conn.close()

print("Database Created Successfully")