import numpy as np
import string

class Tissue:
    def __init__(self, name : string,  Center : np.array[float], Radius : float, absoarption_coefficients : dict):
        self.Center = Center
        self.Radius = Radius
        self.name = name
        self.absoarption_coefficients = absoarption_coefficients