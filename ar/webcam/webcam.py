import pyfakewebcam
import numpy as np
import cv2 as cv


class Webcam():

    def __init__(self, id: int, write_id: int = None):

        self.transforms = []
        self.id = id
        self.write_id = write_id
        self.cap = cv.VideoCapture(self.id)
        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        
        if not (write_id is None):
            self.fake_cap = pyfakewebcam.FakeWebcam(f'/dev/video{self.write_id}', self.width, self.height)

    def read(self)->np.ndarray:

        _, frame = self.cap.read()
        #print(frame.dtype)
        return frame

    def write(self):
        pass

       

