from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

def create_pie_chart(data):
    series = QPieSeries()
    for category, amount in data:
        series.append(category, amount)
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Expense Distribution by Category")
    chart.legend().setAlignment(Qt.AlignBottom)
    return chart

def create_bar_chart(data):
    series = QBarSeries()
    for category, amount in data:
        set_bar = QBarSet(category)
        set_bar.append(amount)
        series.append(set_bar)
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Expense by Category")
    axisX = QValueAxis()
    axisX.setTitleText("Categories")
    axisY = QValueAxis()
    axisY.setTitleText("Amount")
    chart.setAxisX(axisX, series)
    chart.setAxisY(axisY, series)
    return chart

def create_line_chart(income_data, expense_data):
    income_series = QLineSeries()
    for i, amount in enumerate(income_data):
        income_series.append(i, amount)

    expense_series = QLineSeries()
    for i, amount in enumerate(expense_data):
        expense_series.append(i, amount)

    chart = QChart()
    chart.addSeries(income_series)
    chart.addSeries(expense_series)
    chart.setTitle("Income and Expense Trends Over Time")
    chart.createDefaultAxes()
    return chart
