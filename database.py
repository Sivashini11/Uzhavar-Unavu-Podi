from db import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id SERIAL PRIMARY KEY,
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

print("Orders table created successfully.")