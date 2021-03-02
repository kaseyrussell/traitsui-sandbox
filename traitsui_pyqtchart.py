"""
Classes to enable embedding a PyQtChart chart into a TraitsUI GUI

This is a PyQtChart/PyQt5 adaptation of Pierre Haessig's script to put a matplotlib figure in a Qt-based TraitsUI window:
https://gist.github.com/pierre-haessig/9838326
which was itself a Qt adaptation of Gael Varoquaux's tutorial to integrate Matplotlib
http://docs.enthought.com/traitsui/tutorials/traits_ui_scientific_app.html#extending-traitsui-adding-a-matplotlib-figure-to-our-application
based on Qt-based code shared by Didrik Pinte, May 2012
http://markmail.org/message/z3hnoqruk56g2bje


Tested with
PyQt5.QtCore.QT_VERSION_STR: 5.12.9
traits.__version__: '6.2.0'
traitsui.__version__: '7.1.1'

-Kasey Russell, Feb 2021
"""
from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QPainter
from traitsui.qt4.editor import Editor
from traitsui.basic_editor_factory import BasicEditorFactory


class _PyQtChartEditor(Editor):
    scrollable = True

    def init(self, parent):
        self.control = self._create_chart_view(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_chart_view(self, parent):
        """ Create the chart """
        chart_view = QChartView(self.value)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view


class PyQtChartEditor(BasicEditorFactory):
    klass = _PyQtChartEditor


if __name__ == '__main__':
    # demo the editor
    from PyQt5.QtChart import QChart, QLineSeries
    from PyQt5.QtCore import Qt, QPointF
    from traits.api import HasTraits, Int, Float, observe, Any, Instance
    from traitsui.api import View, Item
    from numpy import sin, cos, linspace, pi


    class Test(HasTraits):

        chart = Instance(QChart, ())
        series = Instance(QLineSeries, ())
        n = Int(11)
        a = Float(0.5)

        view = View(Item('chart', editor=PyQtChartEditor(),
                         show_label=False),
                    Item('n'),
                    Item('a'),
                    width=500,
                    height=500,
                    resizable=True)

        def __init__(self):
            super(Test, self).__init__()
            self.chart.addSeries(self.series)
            self.chart.setAnimationOptions(QChart.SeriesAnimations)  # kind of fun! Or comment out to make it snappy
            self.chart.createDefaultAxes()
            self.chart.legend().setVisible(False)
            self.chart.axes(orientation=Qt.Horizontal)[0].setRange(-2, 2)
            self.chart.axes(orientation=Qt.Vertical)[0].setRange(-2, 2)
            self._t = linspace(0, 2 * pi, 1000)
            self._initialized = False
            self.plot()

        @observe('n,a')
        def plot(self, event=None):
            t = self._t
            a = self.a
            n = self.n
            x = sin(t) * (1 + a * cos(n * t))
            y = cos(t) * (1 + a * cos(n * t))
            if not self._initialized:
                self._initialized = True
                for xi, yi in zip(x, y):
                    self.series.append(xi, yi)
            else:
                new_data = [QPointF(xi, yi) for xi, yi in zip(x, y)]
                self.series.replace(new_data)


    obj = Test()
    obj.configure_traits()
