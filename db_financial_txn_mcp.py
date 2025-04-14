import psycopg2
import os
from mcp.server.fastmcp import FastMCP

mcp_db = FastMCP("db_financial_transactions")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")  # Replace with your PostgreSQL username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Replace with your PostgreSQL password
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_db():
    """Connects to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@mcp_db.tool()
async def query_transactions(account_id: int = None, transaction_type: str = None, min_amount: float = None, max_amount: float = None) -> str:
    """Query financial transactions based on criteria.

    Args:
        account_id: Filter by account ID.
        transaction_type: Filter by transaction type (deposit, withdrawal, etc.).
        min_amount: Filter transactions with amount greater than or equal to this value.
        max_amount: Filter transactions with amount less than or equal to this value.
    """
    conn = connect_db()
    if not conn:
        return "Could not connect to the database."
    cur = conn.cursor()
    query = "SELECT transaction_date, account_id, transaction_type, amount, description FROM financial_transactions WHERE 1=1"
    params = []

    if account_id is not None:
        query += " AND account_id = %s"
        params.append(account_id)
    if transaction_type is not None:
        query += " AND transaction_type = %s"
        params.append(transaction_type)
    if min_amount is not None:
        query += " AND amount >= %s"
        params.append(min_amount)
    if max_amount is not None:
        query += " AND amount <= %s"
        params.append(max_amount)

    try:
        cur.execute(query, params)
        results = cur.fetchall()
        if results:
            output = "Financial Transactions:\n"
            for row in results:
                output += f"Date: {row[0]}, Account: {row[1]}, Type: {row[2]}, Amount: {row[3]}, Description: {row[4]}\n"
            return output
        else:
            return "No transactions found matching the criteria."
    except psycopg2.Error as e:
        return f"Error querying the database: {e}"
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("Starting PostgreSQL data MCP server...")
    mcp_db.run(transport='stdio')
    print("PostgreSQL data MCP server is running...")