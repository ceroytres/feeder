import random
import sys
from collections import deque
import threading
import queue
import time
import argparse

import pyfakewebcam
import numpy as np
import cv2

from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QPushButton, QVBoxLayout)
                             
parser = argparse.ArgumentParser(description='Creates a DnD dice roller GUI and overlays the results on webcam stream')
parser.add_argument('-f', action='store_true', help = 'Flips stream about the vertical axis')
parser.add_argument('-c', default=2, type=int, help = 'Select camera device')
args = parser.parse_args()




class VideoOverlayThread(QThread):


    def __init__(self, flip = False):
        super(VideoOverlayThread,self).__init__()
        self.flip = flip

    def run(self):
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        camera = pyfakewebcam.FakeWebcam(f'/dev/video{args.c}', width, height)


        
        while True:
            ret, frame = cap.read()
            
            frame = self.set_txt(frame)
            if self.flip:
                frame = frame[:,::-1]
            frame = np.ascontiguousarray(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera.schedule_frame(frame)


    def set_txt(self, img):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        fontScale              = .5
        fontColor              = (255,255,255)
        loc_x, loc_y = (10,100)

        if len(self.roll_queue) == 0:
            loc = (loc_x, loc_y)
            roll_txt = "DnD Roller On!"
            img = cv2.putText(img, roll_txt, loc, font, fontScale, fontColor, thickness = 2)
        else:
            for i, (roll_no, dice_type, val) in enumerate(self.roll_queue):
                roll_txt = f"Roll: {roll_no} Dice: d{dice_type} Value: {val}"
                _,y_size= cv2.getTextSize(roll_txt, font, fontScale, thickness=2)
                loc = (loc_x, loc_y + y_size * i * 10)
                img = cv2.putText(img, roll_txt, loc, font, fontScale, fontColor, thickness = 2)
   


        
        return img

class DiceWindow(QMainWindow): 

    def __init__(self, num_rolls_save: int = 8, flip = args.f):

        super(DiceWindow, self).__init__()


        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.num_clicks = 0
        self.num_rolls_save = num_rolls_save
        self.roll_queue = deque([], self.num_rolls_save)
        self.roll_txt = ""


        for dice in [4,6, 8, 10, 100, 12, 20]:
            button = QPushButton(f'd{dice}', self.central_widget)
            dice_click = lambda ch, d = dice: self.on_button_clicked(d)
            button.clicked.connect(dice_click)
            self.layout.addWidget(button)


        self.setCentralWidget(self.central_widget)

        self.video_thread = VideoOverlayThread(flip=flip)
        self.video_thread.roll_queue= self.roll_queue
        self.video_thread.start()



    def on_button_clicked(self, dice: int):
        if dice == 10:
            res = random.randrange(0,10)
        elif dice == 100:
            res = random.randrange(0,100,10)
        else:
            res = random.randrange(1,dice+1)
        
        self.num_clicks +=1
        self.roll_queue.appendleft((self.num_clicks,dice,res))
        self.video_thread.roll_queue= self.roll_queue


        







if __name__ == "__main__":



    app = QApplication(["DnD Dice Roller"])
    window = DiceWindow()                                          
    window.show()
    sys.exit( app.exec_() )
    
