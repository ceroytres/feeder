import time
import pyfakewebcam
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Frame Size {width}x{height}  FPS {fps}")

camera = pyfakewebcam.FakeWebcam('/dev/video2', width, height)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
    dy = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)

    D = np.sqrt(dx**2 + dy**2)
    D_min = D.min()
    D_max = D.max()

    D = 255 * (D - D_min)/(D_max - D_min)
    D = np.uint8(D)

    D = cv2.cvtColor(D, cv2.COLOR_GRAY2RGB)

    camera.schedule_frame(D)
    time.sleep(1/fps)