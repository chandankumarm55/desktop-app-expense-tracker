import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QRadioButton, QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QWidget, QStackedWidget, QHeaderView
)
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtChart import QLegend
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime

from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from database import BudgetDatabase
from charts import create_pie_chart, create_line_chart
from analysis_page import AnalysisPage

class BudgetTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = BudgetDatabase()
        self.setWindowTitle("Budget Tracker")
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create main page
        self.main_page = QWidget()
        self.init_main_ui()
        self.central_widget.addWidget(self.main_page)

        # Create transactions page
        self.transactions_page = QWidget()
        self.init_transactions_page()
        self.central_widget.addWidget(self.transactions_page)

        # Set the theme
        self.set_black_white_theme()

        # Set window size
        self.resize(1200, 800)

    def init_main_ui(self):
        """Initialize the main UI layout."""
        main_layout = QHBoxLayout(self.main_page)

        # Left Side: Transaction Entry Form
        left_layout = QVBoxLayout()
        self.init_transaction_form(left_layout)

        # Right Side: Overview and Charts
        right_layout = QVBoxLayout()
        self.init_overview_charts(right_layout)

        # Add layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Update charts and overview
        self.update_overview()

    def init_transaction_form(self, layout):
        """Initialize the transaction entry form."""
        title_label = QLabel("Add Transaction")
        title_label.setStyleSheet("QLabel { color: black; font-size: 16px; font-weight: bold; }")

        # Input fields
        input_style = """
            QLineEdit, QTextEdit, QDateEdit {
                background-color: white;
                color: black;
                border: 1px solid black;
                padding: 5px;
            }
            QRadioButton {
                color: black;
            }
        """
        self.category_input = QLineEdit(placeholderText="Category")
        self.category_input.setStyleSheet(input_style)

        self.amount_input = QLineEdit(placeholderText="Amount")
        self.amount_input.setStyleSheet(input_style)

        self.income_radio = QRadioButton("Income")
        self.expense_radio = QRadioButton("Expense")

        self.date_input = QDateEdit()
        self.date_input.setStyleSheet(input_style)

        self.description_input = QTextEdit(placeholderText="Description")
        self.description_input.setStyleSheet(input_style)

        # Buttons
        button_style = """
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """
        self.add_transaction_btn = QPushButton("Add Transaction")
        self.add_transaction_btn.setStyleSheet(button_style)
        self.add_transaction_btn.clicked.connect(self.add_transaction)

        self.view_all_transactions_btn = QPushButton("View All Transactions")
        self.view_all_transactions_btn.setStyleSheet(button_style)
        self.view_all_transactions_btn.clicked.connect(self.show_transactions_page)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.category_input)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.income_radio)
        layout.addWidget(self.expense_radio)
        layout.addWidget(self.date_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.add_transaction_btn)
        layout.addWidget(self.view_all_transactions_btn)

    def init_overview_charts(self, layout):
        title_label = QLabel("Overview")
        title_label.setStyleSheet("QLabel { color: black; font-size: 16px; font-weight: bold; }")
        
        self.total_income_label = QLabel("Total Income: ₹0.00")
        self.total_expense_label = QLabel("Total Expense: ₹0.00")
        self.total_savings_label = QLabel("Savings: ₹0.00")
        
        self.expense_chart_view = QChartView()
        self.expense_chart_view.setRenderHint(QPainter.Antialiasing)
        self.expense_chart_view.setStyleSheet("background-color: white;")
        
        self.income_chart_view = QChartView()
        self.income_chart_view.setRenderHint(QPainter.Antialiasing)
        self.income_chart_view.setStyleSheet("background-color: white;")
        
        layout.addWidget(title_label)
        layout.addWidget(self.total_income_label)
        layout.addWidget(self.total_expense_label)
        layout.addWidget(self.total_savings_label)
        layout.addWidget(QLabel("Expense Distribution by Category"))
        layout.addWidget(self.expense_chart_view)
        layout.addWidget(QLabel("Income Distribution by Category"))
        layout.addWidget(self.income_chart_view)

        

        # Analysis button
        button_style = """
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """
        self.view_analysis_btn = QPushButton("View More Analysis")
        self.view_analysis_btn.setStyleSheet(button_style)
        self.view_analysis_btn.clicked.connect(self.view_analysis)

       

    def init_transactions_page(self):
        """Initialize the transactions page."""
        layout = QVBoxLayout(self.transactions_page)

        # Back button
        back_button = QPushButton("Back to Main")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        back_button.clicked.connect(self.show_main_page)
        layout.addWidget(back_button)

        # Transactions table
        self.transaction_table = QTableWidget()
        self.transaction_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: black;
            }
            QHeaderView::section {
                background-color: black;
                color: white;
                padding: 5px;
            }
        """)
        layout.addWidget(self.transaction_table)

    def show_main_page(self):
        self.central_widget.setCurrentWidget(self.main_page)

    def show_transactions_page(self):
        self.update_transactions_table()
        self.central_widget.setCurrentWidget(self.transactions_page)
        

    def update_transactions_table(self):
        transactions = self.db.get_all_transactions()
        self.transaction_table.setColumnCount(6)  # Add an extra column for the delete button
        self.transaction_table.setHorizontalHeaderLabels(["Category", "Amount", "Type", "Date", "Description", "Delete"])
        self.transaction_table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            for col, data in enumerate(transaction[1:]):  # Skip the ID column
                item = QTableWidgetItem(str(data))
                if row % 2 == 0:
                    item.setBackground(QColor(240, 240, 240))  # Light gray for even rows
                else:
                    item.setBackground(QColor(255, 255, 255))  # White for odd row
                item.setTextAlignment(Qt.AlignCenter)
                self.transaction_table.setItem(row, col, item)

            # Add a delete button in the last column for each row
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: darkred;
                }
            """)
            delete_button.clicked.connect(lambda checked, row=row: self.delete_transaction(transactions[row]))  # Use ID for deletion
            self.transaction_table.setCellWidget(row, 5, delete_button)  # Place the button in the 6th column
        
        self.transaction_table.resizeColumnsToContents()
        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.transaction_table.setSortingEnabled(True)

    def delete_transaction(self, transaction_id):
        """Delete a transaction from the database."""
        print(transaction_id)
        self.db.delete_transaction(transaction_id[0])
        self.update_transactions_table()  # Refresh the table after deletion       
        # Styling the transaction table

        self.transaction_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dcdcdc;
                font-family: Arial;
                font-size: 14px;
                background-color: #fdfdfd;
                color: #333333;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                padding: 5px;
                text-align: center;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #cce7ff;
                color: #000000;
            }
        """)
        self.transaction_table.verticalHeader().setDefaultSectionSize(30)

        # Add filter layout and export button only once
        if not hasattr(self, 'filter_layout_added') or not self.filter_layout_added:
            self.filter_layout_added = True
            export_button = QPushButton("Export to CSV")
            export_button.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)
            export_button.clicked.connect(self.export_transactions_to_csv)

            # Filter inputs
            category_filter = QLineEdit()
            category_filter.setPlaceholderText("Filter by Category")
            category_filter.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #dcdcdc;
                    padding: 5px;
                }
            """)
            category_filter.textChanged.connect(lambda text: self.filter_transactions("Category", text))

            type_filter = QLineEdit()
            type_filter.setPlaceholderText("Filter by Type (Income/Expense)")
            type_filter.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #dcdcdc;
                    padding: 5px;
                }
            """)
            type_filter.textChanged.connect(lambda text: self.filter_transactions("Type", text))

            # Layout for filters and export button
            filter_layout = QHBoxLayout()
            filter_layout.addWidget(category_filter)
            filter_layout.addWidget(type_filter)
            filter_layout.addWidget(export_button)

            # Insert the filter layout only if it's not already added
            self.transactions_page.layout().insertLayout(1, filter_layout)

    # Method to filter transactions based on user input
    def filter_transactions(self, column_name, filter_text):
        column_map = {
            "Category": 0,
            "Type": 2
        }
        column_index = column_map.get(column_name, -1)
        if column_index == -1:
            return
        for row in range(self.transaction_table.rowCount()):
            item = self.transaction_table.item(row, column_index)
            if item and filter_text.lower() in item.text().lower():
                self.transaction_table.showRow(row)
            else:
                self.transaction_table.hideRow(row)

    # Method to export transactions to a CSV file
    def export_transactions_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Transactions", "", "CSV Files (*.csv)")
        if not file_path:
            return
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers
            headers = [self.transaction_table.horizontalHeaderItem(col).text() for col in range(self.transaction_table.columnCount())]
            writer.writerow(headers)

            # Write data rows
            for row in range(self.transaction_table.rowCount()):
                row_data = [self.transaction_table.item(row, col).text() for col in range(self.transaction_table.columnCount())]
                writer.writerow(row_data)



    def add_transaction(self):
        try:
            category = self.category_input.text()
            amount = float(self.amount_input.text())
            trans_type = "Income" if self.income_radio.isChecked() else "Expense"
            date = self.date_input.text()
            description = self.description_input.toPlainText()

            self.db.add_transaction(category, amount, trans_type, date, description)

            # Clear input fields
            self.category_input.clear()
            self.amount_input.clear()
            self.description_input.clear()
            self.income_radio.setChecked(False)
            self.expense_radio.setChecked(False)

            self.update_overview()
        except ValueError:
            pass  # Handle invalid input

    def update_overview(self):
        transactions = self.db.get_summary_data()
        categories_expense = [(category, amount) for category, amount in self.db.get_category_data("Expense")]
        categories_income = [(category, amount) for category, amount in self.db.get_category_data("Income")]
        income_amount = sum(amount for trans_type, amount in transactions if trans_type == "Income")
        expense_amount = sum(amount for trans_type, amount in transactions if trans_type == "Expense")
        savings = income_amount - expense_amount
        
        self.total_income_label.setText(f"Total Income: ₹{income_amount:.2f}")
        self.total_expense_label.setText(f"Total Expense: ₹{expense_amount:.2f}")
        self.total_savings_label.setText(f"Savings: ₹{savings:.2f}")
        
        expense_chart = create_pie_chart(categories_expense, "Expense Distribution")
        income_chart = create_pie_chart(categories_income, "Income Distribution")
        self.expense_chart_view.setChart(expense_chart)
        self.income_chart_view.setChart(income_chart)

   

    def view_analysis(self):
        transactions = self.db.get_summary_data()
        income_data = [amount for trans_type, amount in transactions if trans_type == "Income"]
        expense_data = [amount for trans_type, amount in transactions if trans_type == "Expense"]
        dates = [QDateTime.fromString(date, "yyyy-MM-dd") for _, _, _, _, date, _ in self.db.get_all_transactions()]
        
        line_chart = create_line_chart(dates, income_data, expense_data)
        def on_back():
            self.central_widget.setCurrentWidget(self.main_page)
       
       
    def set_black_white_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                color: black;
            }
        """)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec_())
