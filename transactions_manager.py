# transactions_manager.py
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

def update_transactions_table(db, transaction_table):
    # Retrieve all transactions from the database
    transactions = db.get_all_transactions()

    # Set up table columns
    transaction_table.setColumnCount(5)
    transaction_table.setHorizontalHeaderLabels(["Category", "Amount", "Type", "Date", "Description"])
    transaction_table.setRowCount(len(transactions))

    # Populate the table with transactions
    for row, transaction in enumerate(transactions):
        for col, data in enumerate(transaction[1:]):  # Skip the ID column
            item = QTableWidgetItem(str(data))
            if row % 2 == 0:
                item.setBackground(QColor(240, 240, 240))  # Light gray for even rows
            else:
                item.setBackground(QColor(255, 255, 255))  # White for odd rows
            item.setTextAlignment(Qt.AlignCenter)
            transaction_table.setItem(row, col, item)

    transaction_table.resizeColumnsToContents()
    header = transaction_table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)
    transaction_table.setSortingEnabled(True)
