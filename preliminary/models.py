import numpy as np
import cv2

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cam = None

    def initialize(self):
        self.cam = cv2.VideoCapture(self.cam_num)
        self.cam.set(3, 640) #set width
        self.cam.set(4, 480) #set height
        if not self.cam.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

    def get_frame(self):
        ret, self.last_frame = self.cam.read()
        return self.last_frame

    def acquire_video(self, num_frames):
        video = []
        for _ in range(num_frames):
            video.append(self.get_frame())
        return video

    def set_brightness(self, value):
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, value)
    def get_brightness(self):
        return self.cam.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cam.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


# if __name__ == '__main__':
#     cam = Camera(3)
#     cam.initialize()
#     print(cam)
#     cam.set_brightness(3)
#     print(cam.get_brightness())
#     cam.set_brightness(0.5)
#     print(cam.get_brightness())
#     cam.close_camera()
