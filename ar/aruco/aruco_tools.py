from typing import List,Tuple
import warnings


import numpy as np
import cv2 as cv



class FourCornerArucoDetector():

    def __init__(self, aruco_dict: str):
        self.parameters =  cv.aruco.DetectorParameters_create()

        self.dictionary = cv.aruco.Dictionary_get(getattr(cv.aruco, aruco_dict))

        self.detector = lambda im: cv.aruco.detectMarkers(im, self.dictionary, parameters=self.parameters)

    def detect(self, im: np.ndarray)->Tuple[np.ndarray, List[int]]:

        corners, ids, rejected = self.detector(im)

        return corners, ids



        



class FourCornerArucoTagGenerator():

    def __init__(self, aruco_dict: str, tag_size:int, ids: List[int], borderBits: int,
                space_row: int, space_col:int, pad_size: int):


        self.dictionary = cv.aruco.Dictionary_get(getattr(cv.aruco, aruco_dict))
        self.space_col = space_col
        self.space_row = space_row
        self.ids = ids
        self.borderBits = borderBits
        self.space_row = space_row
        self.space_col = space_col
        self.tag_size = tag_size
        self.pad_size = pad_size


    def generate_tag(self) -> np.ndarray:

        drawMarker = lambda ids, out: cv.aruco.drawMarker(self.dictionary, ids, self.tag_size,
                                                         out, self.borderBits)

        markers = [drawMarker(ids, np.zeros((self.tag_size, self.tag_size))) for ids in self.ids]

        top = np.concatenate([markers[0], np.zeros((self.tag_size, self.space_col), dtype=np.uint8)+255, markers[1]],
                             axis = 1)
        bottom = np.concatenate([markers[2], np.zeros((self.tag_size, self.space_col),dtype=np.uint8)+255, markers[3]],
                             axis = 1)

        middle = np.zeros((self.space_row, self.space_col + 2*self.tag_size), dtype=np.uint8) + 255


        tag = np.concatenate([top, middle, bottom], axis = 0)

        pad_shape = ((self.pad_size,self.pad_size), (self.pad_size,self.pad_size))

        self.tag = np.pad(tag, pad_shape, 'constant', constant_values=255)

        return self.tag

    def save(self, fname:str):

        if not hasattr(self,'tag'):
            self.generate_tag()
            

        cv.imwrite(fname, self.tag)


