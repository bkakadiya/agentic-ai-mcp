import psycopg2
import random
from datetime import datetime, timedelta

DB_NAME = "mydatabase"
DB_USER = "***"  # Replace with your PostgreSQL username
DB_PASSWORD = "****"  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Drop table if it exists
    cur.execute("DROP TABLE IF EXISTS financial_transactions;")
    conn.commit()

    # Create the financial_transactions table
    cur.execute("""
        CREATE TABLE financial_transactions (
            id SERIAL PRIMARY KEY,
            transaction_date TIMESTAMP NOT NULL,
            account_id INTEGER NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT
        )
    """)
    conn.commit()

    print("Table financial_transactions created successfully.")

    # Insert 500 rows of sample data
    num_rows = 500
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)

    transaction_types = ["deposit", "withdrawal", "transfer_in", "transfer_out", "payment"]

    print("Inserting sample data...")
    for _ in range(num_rows):
        random_date = start_date + (end_date - start_date) * random.random()
        account_id = random.randint(1001, 1050)
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(10, 1000), 2)
        description = f"{transaction_type.capitalize()} on account {account_id}"
        if random.random() < 0.2:
            description += f" - Reference ID: {random.randint(10000, 99999)}"

        cur.execute("""
            INSERT INTO financial_transactions (transaction_date, account_id, transaction_type, amount, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (random_date, account_id, transaction_type, amount, description))

    conn.commit()
    print(f"{num_rows} sample financial transactions inserted successfully.")

    cur.close()
    conn.close()

    # Print the first 5 rows of the table to verify the data
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM financial_transactions LIMIT 5;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error connecting to or interacting with PostgreSQL: {e}")