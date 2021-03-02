# Not technically TraitsUI -- I'm first testing out PyQtChart before trying to use it in TraitsUI
# trying to do multiple lines at once
#
# ALSO NOTE -- If you're running PyQt5 on OSX Big Sur, you need to set an environment variable in the run configuration:
# https://forums.macrumors.com/threads/pyqt5-and-big-sur.2260773/
#
# -Kasey Russell, Feb 2021
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF
import numpy as np


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Line Series")
        self.setGeometry(100, 100, 680, 500)
        self.create_linechart()
        self.show()

    def create_linechart(self):
        series = QLineSeries()
        series.setName("Sensor 1")
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        # This is the "stream operator" that seems to be an alternative to .append()
        # and may be really interesting for data streaming applications such as ours...
        # https://doc.qt.io/qt-5/qdatastream.html
        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)

        series2 = QLineSeries()
        series2.setName("Sensor 2")
        for i in range(len(series)):
            series2.append(i*2, np.sqrt(i) + np.random.rand())

        chart = QChart()
        chart.addSeries(series)
        chart.addSeries(series2)
        chart.createDefaultAxes()
        chart.setTitle("Line Chart Example")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        chart.axes(orientation=Qt.Horizontal)[0].setTitleText("X")
        chart.axes(orientation=Qt.Vertical)[0].setTitleText("Y")

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

