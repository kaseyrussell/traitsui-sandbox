# Not technically TraitsUI -- I'm first testing out PyQtChart before trying to use it in TraitsUI
# This is somewhat based on the LineChart example from here:
# https://www.youtube.com/watch?v=YPoRL4-vZTw
# And the official QtCharts example here:
# https://doc.qt.io/qt-5/qtcharts-linechart-example.html
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

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()  # not in youtube but in QtCharts example
        # chart.setAnimationOptions(QChart.SeriesAnimations)  # not in the official QtCharts example; kind of annoying
        chart.setTitle("Line Chart Example")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

