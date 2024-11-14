import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QRadioButton, QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QWidget, QStackedWidget
)
from PyQt5.QtChart import QLegend

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
        
        self.total_income_label = QLabel("Total Income: $0.00")
        self.total_expense_label = QLabel("Total Expense: $0.00")
        self.total_savings_label = QLabel("Savings: $0.00")
        
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
        self.transaction_table.setColumnCount(5)
        self.transaction_table.setHorizontalHeaderLabels(["Category", "Amount", "Type", "Date", "Description"])
        self.transaction_table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):
            for col, data in enumerate(transaction[1:]):  # Skip ID column
                self.transaction_table.setItem(row, col, QTableWidgetItem(str(data)))

        self.transaction_table.resizeColumnsToContents()

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
        
        self.total_income_label.setText(f"Total Income: ${income_amount:.2f}")
        self.total_expense_label.setText(f"Total Expense: ${expense_amount:.2f}")
        self.total_savings_label.setText(f"Savings: ${savings:.2f}")
        
        expense_chart = create_pie_chart(categories_expense, "Expense Distribution")
        income_chart = create_pie_chart(categories_income, "Income Distribution")
        self.expense_chart_view.setChart(expense_chart)
        self.income_chart_view.setChart(income_chart)

   

    def view_analysis(self):
        transactions = self.db.get_summary_data()
        income_data = [amount for trans_type, amount in transactions if trans_type == "Income"]
        expense_data = [amount for trans_type, amount in transactions if trans_type == "Expense"]
        dates = [QDateTime.fromString(date, "yyyy-MM-dd") for _, _, _, _, date, _ in self.db.get_all_transactions()]
        # pie_chart_expense = create_pie_chart(self.db.get_category_data(type="Expense"))
        # pie_chart_income = create_pie_chart(self.db.get_category_data(type="Income"))
        line_chart = create_line_chart(dates, income_data, expense_data)
        def on_back():
            self.central_widget.setCurrentWidget(self.main_page)
        # analysis_dialog = AnalysisPage(pie_chart_income, pie_chart_expense, line_chart, on_back)
        # analysis_dialog.setStyleSheet("background-color: white;")
        # self.central_widget.addWidget(analysis_dialog)
        # self.central_widget.setCurrentWidget(analysis_dialog)


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
