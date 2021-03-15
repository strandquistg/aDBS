import numpy as np
from PyQt5.QtWidgets import * #QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from pyqtgraph import ImageView
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QColor
import sys, cv2

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

    def __init__(self, cam_ind = None):
        super().__init__()
        self._run_flag = True
        self.camera_ind = cam_ind

    def run(self):
        # capture from web cam
        self._run_flag = True
        cam = cv2.VideoCapture(self.camera_ind)
        while self._run_flag:
            ret, cv_img = cam.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        self.cam.release()
        self.finished.emit()


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def kill_thread(self):
        """kill thread"""
        self.stop()

class BasicWindow(QWidget):
    def __init__(self, cam_index = None):
        super().__init__()
        self.cam_in = cam_index
        self.disply_width = 1000
        self.display_height = 700
        self.setWindowTitle("Basic window")
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread(self.cam_in)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    #PyQt's signal slot mechanism ensures thread saftey
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
