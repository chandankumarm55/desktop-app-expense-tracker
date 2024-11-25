import sqlite3

class BudgetDatabase:
    def __init__(self, db_name="budget.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            type TEXT,
            date TEXT,
            description TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, category, amount, trans_type, date, description):
        query = """
        INSERT INTO transactions (category, amount, type, date, description)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (category, amount, trans_type, date, description))
        self.conn.commit()

    def get_all_transactions(self):
        query = "SELECT * FROM transactions"
        return self.conn.execute(query).fetchall()

    def get_summary_data(self):
        query = """
        SELECT type, SUM(amount) FROM transactions GROUP BY type
        """
        return self.conn.execute(query).fetchall()

    def get_category_data(self, type="Expense"):
        query = """
        SELECT category, SUM(amount) FROM transactions WHERE type = ? GROUP BY category
        """
        return self.conn.execute(query, (type,)).fetchall()


    def close(self):
        self.conn.close()
        
    def delete_transaction(self, transaction_id):
        query = "DELETE FROM transactions WHERE id = ?"
        
        self.conn.execute(query, (transaction_id,))
        self.conn.commit()

