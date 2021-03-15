import numpy as np
from PyQt5.QtWidgets import * #QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider
from PyQt5.QtCore import Qt, QThread, QTimer
from pyqtgraph import ImageView
from PyQt5.QtGui import QPixmap, QColor
import sys, cv2


class StartWindow(QMainWindow):
    def __init__(self, camera = None):
        super().__init__()
        self.camera = camera
        self.setWindowTitle("Qt live label demo")

        self.central_widget = QWidget()
        self.button_screenshot = QPushButton('Acquire Frame', self.central_widget)
        self.button_video_start = QPushButton('Start Video', self.central_widget)
        self.button_video_stop = QPushButton('Stop Video', self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_screenshot)
        self.layout.addWidget(self.button_video_start)
        self.layout.addWidget(self.button_video_stop)
        self.image_view = None
        #self.layout.addWidget(self.image_view)
        self.setCentralWidget(self.central_widget)

        self.button_screenshot.clicked.connect(self.update_image)

        #Start button
        self.button_video_start.clicked.connect(self.start_video)
        #Stop button
        self.button_video_stop.clicked.connect(self.stop_video)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_video)

    def update_image(self):
        frame = self.camera.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.image_view = cv2.imshow('frame',frame)
        #self.image_view.setImage(frame.T)

    def update_video(self):
        self.image_view.setImage(self.camera.last_frame.T)

    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)

    def start_video(self):
        self.video_thread = VideoThread(self.camera)
        self.video_thread.start()
        self.update_timer.start(30)

    def stop_video(self):
        self.update_timer.stop()

class VideoThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_video(200)

# if __name__ == '__main__':
#     app = QApplication([])
#     window = StartWindow()
#     window.show()
#     app.exit(app.exec_())
