from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtChart import QChartView, QChart
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class AnalysisPage(QWidget):
    def __init__(self, income_chart, expense_chart, line_chart, on_back):
        super().__init__()
        self.setWindowTitle("Detailed Analysis")

        layout = QVBoxLayout()

        # Pie Charts for Income Distribution and Expense Distribution
        income_chart_view = QChartView(income_chart)
        income_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(income_chart_view)

        expense_chart_view = QChartView(expense_chart)
        expense_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(expense_chart_view)

        # Line Chart for Income and Expense Trends
        line_chart_view = QChartView(line_chart)
        line_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(line_chart_view)

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
        back_button.clicked.connect(on_back)
        layout.addWidget(back_button)

        self.setLayout(layout)