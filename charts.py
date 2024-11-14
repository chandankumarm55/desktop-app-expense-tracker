# charts.py
from PyQt5.QtChart import QChart, QPieSeries, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import Qt, QDateTime

def create_pie_chart(data, title="Distribution by Category"):
    series = QPieSeries()
    total = sum(amount for _, amount in data)

    for category, amount in data:
        slice_ = series.append(category, amount)
        slice_.setLabel(f"{category} ({amount / total * 100:.1f}%)")
        slice_.setLabelVisible()

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle(title)
    chart.legend().setAlignment(Qt.AlignBottom)
    chart.legend().setLabelColor(Qt.black)
    chart.setBackgroundBrush(Qt.white)

    chart.setTheme(QChart.ChartThemeBlueCerulean)
    chart.setAnimationOptions(QChart.AllAnimations)
    chart.setAnimationDuration(1000)

    return chart
    
def create_line_chart(dates, income_data, expense_data):
    income_series = QLineSeries()
    expense_series = QLineSeries()

    for date, income in zip(dates, income_data):
        timestamp = QDateTime.fromString(date, "yyyy-MM-dd").toMSecsSinceEpoch()
        income_series.append(timestamp, income)

    for date, expense in zip(dates, expense_data):
        timestamp = QDateTime.fromString(date, "yyyy-MM-dd").toMSecsSinceEpoch()
        expense_series.append(timestamp, expense)

    chart = QChart()
    chart.addSeries(income_series)
    chart.addSeries(expense_series)
    chart.setTitle("Income and Expense Trends Over Time")

    axisX = QDateTimeAxis()
    axisX.setFormat("MMM dd")
    axisX.setTitleText("Date")
    chart.addAxis(axisX, Qt.AlignBottom)
    income_series.attachAxis(axisX)
    expense_series.attachAxis(axisX)

    axisY = QValueAxis()
    axisY.setTitleText("Amount")
    chart.addAxis(axisY, Qt.AlignLeft)
    income_series.attachAxis(axisY)
    expense_series.attachAxis(axisY)
    return chart
