#https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
from __future__ import print_function
import datetime
from threading import Thread
import cv2, argparse
from FPS import *
from WebcamVideoStream import *




# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

#Baseline
# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(1)
fps = FPS().start()
# loop over some frames
while fps._numFrames < args["num_frames"]:
	# grab the frame from the stream
	(grabbed, frame) = stream.read()
    #r = 150.0 / frame.shape[1]
    # dim = (150, int(frame.shape[0] *  (150.0 / frame.shape[1]) ) )
    # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

def help():
    print("Help!!")

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=1).start()
fps = FPS().start()
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = help()#cv2.resize(frame, width=400)
	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
