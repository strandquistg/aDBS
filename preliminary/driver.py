from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
import pdb, os, sys
from models import Camera
from basic_gui import StartWindow
from basic_widge import BasicWindow
from gui_thread_fps import *

ui_path = '/home/strandquistg/repos/aDBS/qt_tester/'



# camera = Camera(1) #7
# camera.initialize()
app = QApplication([])
#window = uic.loadUi(ui_path + "mainwindow.ui")
# window.show()
# app.exec()
start_window = gui_thread_fps(1)
start_window.show()
app.exit(app.exec_())
