from typing import List

import numpy as np
import cv2 as cv


class FourCornerTagGenerator():

    def __init__(self, tag_size:int, ids: List[int], borderBits: int,
                space_row: int, space_col:int):

        self.dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
        self.space_col = space_col
        self.space_row = space_row
        self.ids = ids
        self.borderBits = borderBits
        self.space_row = space_row
        self.space_col = space_col
        self.tag_size = tag_size


    def generate_tag(self) -> np.ndarray:

        drawMarker = lambda ids, out: cv.aruco.drawMarker(self.dictionary, ids, self.tag_size,
                                                         out, self.borderBits)

        markers = [drawMarker(ids, np.zeros((self.tag_size, self.tag_size))) for ids in self.ids]

        top = np.concatenate([markers[0], np.zeros((self.tag_size, self.space_col), dtype=np.uint8)+255, markers[1]],
                             axis = 1)
        bottom = np.concatenate([markers[2], np.zeros((self.tag_size, self.space_col),dtype=np.uint8)+255, markers[3]],
                             axis = 1)

        middle = np.zeros((self.space_row, self.space_col + 2*self.tag_size), dtype=np.uint8) + 255


        self.tag = np.concatenate([top, middle, bottom], axis = 0)

        return self.tag
