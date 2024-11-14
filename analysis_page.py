from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtChart import QChartView

class AnalysisPage(QDialog):
    def __init__(self, line_chart):
        super().__init__()
        self.setWindowTitle("Detailed Analysis")
        layout = QVBoxLayout()
        chart_view = QChartView(line_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)
        self.setLayout(layout)
