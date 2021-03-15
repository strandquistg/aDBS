from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Tester layout")

        layout_base = QVBoxLayout()
        layout_h = QHBoxLayout()#QGridLayout()
        camera1 = QLabel("webcam1")
        camera2 = QLabel("webcam2")
        start_b = QPushButton("Start Video")
        stop_b = QPushButton("Stop Video")

        #layout_h.addWidget(Color('purple'))
        layout_h.addWidget(camera1)
        layout_h.addWidget(camera2)

        layout_base.addWidget( start_b )
        layout_base.addWidget( stop_b )
        layout_base.addLayout(layout_h)
        layout_h.setSpacing(30)

        widget = QWidget()
        widget.setLayout(layout_base)
        self.setCentralWidget(widget)
        self.show()


app = QApplication([])
window = MainWindow()
app.exec_()
