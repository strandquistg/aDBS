import datetime
from threading import Thread
import cv2

class WebcamVideoStream:

    #Constructor
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
	    # calling update method causes the method to be placed in separate thread from main script - hence better FPS!
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				print("returning")
				cv2.destroyAllWindows()
				return
			# otherwise, read the next frame from the stream
			print("before")
			(self.grabbed, self.frame) = self.stream.read()
			print("after")
	def read(self):
		# return the frame most recently read
		print("in read func func")
		return self.frame
	def stop(self):
		# indicate that the thread should be stopped
		print("Stop in thread!")
		self.stopped = True
