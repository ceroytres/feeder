from ar.aruco import FourCornerArucoDetector
from ar.webcam import Webcam


webcam = Webcam(0)
detector = FourCornerArucoDetector("DICT_6X6_250")


while True:

    frame = webcam.read()

    corners,ids = detector.detect(frame)

    if not (ids is None):
        print(ids)

