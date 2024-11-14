import sys
from PyQtChart import QChartView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QDateEdit, QTextEdit
from database import BudgetDatabase
from charts import create_pie_chart, create_bar_chart, create_line_chart
from analysis_page import AnalysisPage

class BudgetTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.db = BudgetDatabase()
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QHBoxLayout()

        # Left side - Transaction Entry
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.income_radio = QRadioButton("Income")
        self.expense_radio = QRadioButton("Expense")
        self.date_input = QDateEdit()
        self.description_input = QTextEdit()
        self.add_transaction_btn = QPushButton("Add Transaction")
        self.add_transaction_btn.clicked.connect(self.add_transaction)
        self.view_analysis_btn = QPushButton("View More Analysis")
        self.view_analysis_btn.clicked.connect(self.view_analysis)

        # Right side - Charts
        self.overview_label = QLabel()
        self.pie_chart_view = QChartView()
        self.bar_chart_view = QChartView()

        layout.addWidget(self.overview_label)
        layout.addWidget(self.pie_chart_view)
        layout.addWidget(self.bar_chart_view)
        self.setLayout(layout)
        self.update_overview()

    def add_transaction(self):
        category = self.category_input.text()
        amount = float(self.amount_input.text())
        trans_type = "Income" if self.income_radio.isChecked() else "Expense"
        date = self.date_input.text()
        description = self.description_input.toPlainText()
        self.db.add_transaction(category, amount, trans_type, date, description)
        self.update_overview()

    def update_overview(self):
        transactions = self.db.get_summary_data()
        categories = self.db.get_category_data()

        income_data = [amount for trans_type, amount in transactions if trans_type == "Income"]
        expense_data = [amount for trans_type, amount in transactions if trans_type == "Expense"]

        line_chart = create_line_chart(income_data, expense_data)
        pie_chart = create_pie_chart(categories)
        bar_chart = create_bar_chart(categories)

        self.pie_chart_view.setChart(pie_chart)
        self.bar_chart_view.setChart(bar_chart)

    def view_analysis(self):
        income_data = [amount for trans_type, amount in self.db.get_summary_data() if trans_type == "Income"]
        expense_data = [amount for trans_type, amount in self.db.get_summary_data() if trans_type == "Expense"]
        line_chart = create_line_chart(income_data, expense_data)
        self.analysis_page = AnalysisPage(line_chart)
        self.analysis_page.exec_()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec_())
