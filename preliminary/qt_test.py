#Following: https://www.pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
import cv2, pdb
import numpy as np

##Tester, just opens blank window
# app = QApplication([])
# win = QMainWindow()
# win.show()
# app.exit(app.exec_())

# def button_pressed():
#     print('Button Pressed')
#
# def new_button_pressed():
#     print('Another function')
#
cap = cv2.VideoCapture(3)
# cap = cv2.VideoCapture('rtsp://admin:LUm0s!nx@192.168.0.108/1')
# print("default hxw of camera", cap.get(3), cap.get(4) )
# default_fps = cap.get(cv2.CAP_PROP_FPS)
# print("Default fps",default_fps)
# while(True):
#     ret, frame = cap.read()
#     if not (cap.isOpened()):
#         print("Couldn't open", cap)
#         break
#      # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'): #cv2.waitKey(1) returns the character code of the currently pressed key
#         break
#
# cap.release()
# cv2.destroyAllWindows()
def button_min_pressed():
    ret, frame = cap.read()
    print(np.min(frame))

def button_max_pressed():
    ret, frame = cap.read()
    print(np.max(frame))


app = QApplication([])
win = QMainWindow()
central_widget = QWidget()

button_min = QPushButton('Get Minimum', central_widget)
button_max = QPushButton('Get Maximum', central_widget)
button_min.clicked.connect(button_min_pressed)
button_max.clicked.connect(button_max_pressed)

layout = QVBoxLayout(central_widget)
layout.addWidget(button_min)
layout.addWidget(button_max)

#
win.setCentralWidget(central_widget)
win.show()
app.exit(app.exec_()) #app.exec_() yields an infinite loop
cap.release()
