import random
import sys
from collections import deque
import threading
import queue

import time
import pyfakewebcam
import numpy as np
import cv2

from PyQt5.QtCore import Qt, QThread, QTimer

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QPushButton, QVBoxLayout)

class Camera:

    def __init__(self, cam_num: int = 0):
        self.cam_num = cam_num

    def get_frame(self):
        ret, self.frame = self.cap.read()
        return self.frame

    def start(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def __repr__(self):

        return f"Frame Size {self.width}x{self.height}  FPS {self.fps}"


class DiceWindow(QMainWindow): 

    def __init__(self, num_rolls_save: int = 4):

        super().__init__()

        self.camera = Camera(0)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.num_clicks = 0
        self.num_rolls_save = num_rolls_save
        self.roll_queue = deque([], self.num_rolls_save)


        for dice in [4,6]:
            button = QPushButton(f'd{dice}', self.central_widget)
            dice_click = lambda ch, d = dice: self.on_button_clicked(d)
            button.clicked.connect(dice_click)
            self.layout.addWidget(button)


        self.setCentralWidget(self.central_widget)



    def on_button_clicked(self, dice: int):
        if dice == 10:
            res = random.randrange(0,10)
        elif dice == 100:
            res = random.randrange(0,100,10)
        else:
            res = random.randrange(1,dice+1)
        
        self.num_clicks +=1
        self.roll_queue.appendleft((self.num_clicks,dice,res))

        print(self.roll_queue)


class VideoThread(QThread):

    def __init__(self, camera):
        super().__init__()
        self.camera = camera
    
    def run(self):
        self.camera.get_frame()

if __name__ == "__main__":
    app = QApplication(["Dice Roller"])
    window = DiceWindow()                                          
    window.show()



    sys.exit( app.exec_() )
    