from __future__ import print_function
import numpy as np
from PyQt5.QtWidgets import * #QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from pyqtgraph import ImageView
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QColor
import sys, cv2, argparse
import datetime
from threading import Thread
from FPS import *
from WebcamVideoStream import *


class Worker(QThread):
    #Constructor
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should be stopped
		self.stopped = False


class gui_thread_fps(QMainWindow):
    # Constructor
    def __init__(self, src=0):
        super().__init__()
        self.cam_index = src
        self.recording = False
        self.cam = None
        self.setWindowTitle("Basic window")

        self.cam = WebcamVideoStream(self.cam_index).start()

        #Init buttons
        self.central_widget = QWidget()
        self.button_video_start = QPushButton('Start Video', self.central_widget)
        self.button_video_stop = QPushButton('Stop Video', self.central_widget)

        # create a vertical box layout and add buttons
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_video_start)
        self.layout.addWidget(self.button_video_stop)
        self.setCentralWidget(self.central_widget)



        #Start button
        self.button_video_start.clicked.connect(self.start_video)
        #Stop button
        #self.button_video_stop.clicked.connect(self.stop_video)
        self.button_video_stop.clicked.connect(self.cam.stop)


    def record(self):
        #self.cam.start() # = WebcamVideoStream(self.cam_index).start()
        while (self.recording == True):
            frame = self.cam.read()
            print(self.recording)
            #cv2.imshow("Frame", frame)

    def start_video(self):
        self.recording = True
        self.record()

    def stop_video(self):
        print("\nstopping")
        self.recording = False
        cv2.destroyAllWindows()
        self.cam.stop()
        print(self.recording)
