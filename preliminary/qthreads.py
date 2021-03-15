#Used helpful tutorial here: https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from FPS import *

import time, cv2
import traceback, sys

import numpy as np


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:

    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress
    '''
    finished = pyqtSignal() #no data to indicate when the task is complete
    error = pyqtSignal(tuple) #receives a tuple of Exception type, Exception value and formatted traceback
    result = pyqtSignal(object) #receiving any object type from the executed function
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''
    def __init__(self):
        super(Worker, self).__init__()
        self.record_loop = True

    def begin_job(self, fn, *args, **kwargs):
        # Store constructor arguments (re-used for processing)
        print("beginning thread job")
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        if self.record_loop == True:
            try:
                result = self.fn(*self.args, **self.kwargs)
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.finished.emit()
            #self.signals.result.emit(result)  # Return the result of the processing
        # finally:
        #     print("finally branch")
        #     self.signals.finished.emit()  # Done

    def close_record_loop(self):
        self.record_loop = False

    def open_record_loop(self):
        self.record_loop = True



class MainWindow(QMainWindow):

    def __init__(self, vid_path, src=0, src2=1, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        self.fps = FPS()
        self.sp = vid_path
        self.stream = cv2.VideoCapture(src)
        self.stream2 = cv2.VideoCapture(src2)
        self.default_fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.default_fps2 = self.stream2.get(cv2.CAP_PROP_FPS)
        self.cam_size = (int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.cam_size2 = (int(self.stream2.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.stream2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.writer = cv2.VideoWriter(self.sp+'outputVid.avi', cv2.VideoWriter_fourcc(*'XVID'),self.default_fps, self.cam_size)
        self.writer2 = cv2.VideoWriter(self.sp+'outputVid2.avi', cv2.VideoWriter_fourcc(*'XVID'),self.default_fps2, self.cam_size2)
        self.cam_ind = src
        self.cam_ind2 = src2
        self.stopped = False

        layout = QVBoxLayout()

        self.l = QLabel("Record demo")
        start_b = QPushButton("Start Video")
        start_b.pressed.connect(self.start_record)
        stop_b = QPushButton("Stop Video")
        stop_b.pressed.connect(self.stop_record)

        layout.addWidget(self.l)
        layout.addWidget(start_b)
        layout.addWidget(stop_b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        print("Cam 1 fps&size:",self.default_fps, self.cam_size)
        print("Cam 2 fps&size:",self.default_fps2, self.cam_size2)
        self.worker = Worker()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def show_frame(self):
        print("reading func!!!!")
        # return the frame most recently read
        return self.frame

    def thread_fc(self):
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped == True:
                print("[Record-Info] elasped time: {:.2f}".format(self.fps.elapsed()))
                print("[Record-Info] approx. FPS: {:.2f}".format(self.fps.fps()))
                self.stream.release()
                self.stream2.release()
                self.writer.release()
                self.writer2.release()
                cv2.destroyAllWindows()
                return "Done"
            # otherwise, read the next frame from the stream
            (self.success, self.frame) = self.stream.read()
            (self.success2, self.frame2) = self.stream2.read()
            self.fps.update()
            if self.success:
                self.writer.write(self.frame)
            if self.success2:
                self.writer2.write(self.frame2)
            # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Frame", gray)

    def print_output(self, s):
        print("output", s)

    def thread_complete(self):
        print("Thread complete")

    def execute_thread(self):
        # Pass the function to execute
        self.worker.begin_job(self.thread_fc) # Any other args, kwargs are passed to the run function
        self.worker.signals.result.connect(self.print_output)
        self.worker.signals.finished.connect(self.thread_complete)
        self.worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(self.worker)
        return self

    def start_record(self):
        print('start recording!', self.stopped)
        self.fps.start()
        if self.stopped == True:
            self.worker = Worker()
            self.stream = cv2.VideoCapture(self.cam_ind)
            self.stream2 = cv2.VideoCapture(self.cam_ind2)
            self.writer = cv2.VideoWriter(self.sp+'outputVid.avi', cv2.VideoWriter_fourcc(*'XVID'),self.default_fps, self.cam_size)
            self.writer2 = cv2.VideoWriter(self.sp+'outputVid2.avi', cv2.VideoWriter_fourcc(*'XVID'),self.default_fps2, self.cam_size2)
            self.stopped = False
            self.worker.open_record_loop()
        self.execute_thread()

    def stop_record(self):
        # indicate that the thread should be stopped
        print("Stop recording!")
        self.stopped = True
        self.worker.close_record_loop()
        self.fps.stop()
        self.execute_thread()

    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)



app = QApplication([])
sp = '/home/strandquistg/repos/aDBS/preliminary/vid_files/'
window = MainWindow(sp, 1, 7)
app.exec_()
