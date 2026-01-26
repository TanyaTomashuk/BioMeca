from math import *
from re import I
import numpy as np

class wave_dealer:
    def __init__(self, f : float, start_pos : List[float], dephasage : float, Intensity : float):
        self.f = f
        self.start_pos = start_pos
        self.dephasage = dephasage
        self.Intensity = Intensity

    def wave_at(self, pos : List[float], meshs : np.array[np.array(float)]):
        dist = np.linalg.norm(pos - self.start_pos)
        list