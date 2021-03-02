# Not technically TraitsUI -- I'm first testing out PyQtChart before trying to use it in TraitsUI
# What's the speed like with streaming data?
#
# ALSO NOTE -- If you're running PyQt5 on OSX Big Sur, you need to set an environment variable in the run configuration:
# https://forums.macrumors.com/threads/pyqt5-and-big-sur.2260773/
#
# -Kasey Russell, Feb 2021
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import time


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Line Series")
        self.setGeometry(100, 100, 680, 500)

        self.t0 = time.perf_counter()

        self.chart = QChart()

        self.series = QLineSeries()
        self.series.setName("Sensor 1")

        self.series2 = QLineSeries()
        self.series2.setName("Sensor 2")

        self.series3 = QLineSeries()
        self.series3.setName("Sensor 3")

        self.create_linechart()
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.stream_data)
        self.timer.start(0)

    def create_linechart(self):
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series2)
        self.chart.addSeries(self.series3)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Line Chart Example")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

        self.chart.axes(orientation=Qt.Horizontal)[0].setTitleText("X")
        self.chart.axes(orientation=Qt.Vertical)[0].setTitleText("Y")
        self.chart.axes(orientation=Qt.Vertical)[0].setRange(-2, 2)

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)

    def stream_data(self):
        time_elapsed = time.perf_counter() - self.t0
        self.series.append(time_elapsed, np.random.rand() + 0.5)
        self.series2.append(time_elapsed, np.random.rand() - 0.5)
        self.series3.append(time_elapsed, np.random.rand() - 1.5)
        self.chart.axes(orientation=Qt.Horizontal)[0].setRange(0, time_elapsed)
        if len(self.series) == 1000:
            print(f"Avg time per point: {time_elapsed/1000}")


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

