from ast import In
from math import *
import numpy as np
from Tissue import Tissue

class wave_dealer:
    def __init__(self, f : float, start_pos : np.array[float], dephasage : float, Intensity : float, List_Tissue : List[Tissue]):
        self.f = f
        self.start_pos = start_pos
        self.dephasage = dephasage
        self.Intensity = Intensity
        self.List_Tissue = List_Tissue


    def intersect_sphere(self, tissue : Tissue, p2 : np.array[float]):
        d = p2 - self.start_pos
        f = self.start_pos - tissue.center

        a = np.dot(d, d)
        b = 2 * np.dot(f, d)
        c = np.dot(f, f) - tissue.R**2

        DELTA = b**2 - 4*a*c

        if DELTA < 0 : 
            return None
        
        else : 
            sqrt_DELTA = np.sqrt(DELTA)
            t1 = (-b - sqrt_DELTA) / (2*a)
            t2 = (-b + sqrt_DELTA) / (2*a)

        intersect_p = []

        if 0 < t1 < 1 : 
            intersect_p.append(self.start_pos + d * t1)

        if 0 < t2 < 1 and abs(t2 - t1) > 1e-6:
            intersect_p.append(self.start_pos + d * t2)

        return intersect_p


    def get_distance_in_tissue(self, p2 : np.array[float]):

        List_intersect_point = []
        Next_intersect_point = []
        for tissue in self.List_Tissue:
            current_intersect_p = self.intersect_sphere(tissue, self.start_pos, p2)
            if len(current_intersect_p) == 0:
                return List_intersect_point + Next_intersect_point
            elif len(current_intersect_p) == 1 :
                List_intersect_point.append((tissue, current_intersect_p[0]))
            else :
                List_intersect_point.append((tissue, current_intersect_p[0]))
                Next_intersect_point.append((tissue, current_intersect_p[1]))

        return List_intersect_point + Next_intersect_point
    

    def wave_at_target(self, Target : np.array[float], meshs : np.array[np.array[float]]):
        Intensity = self.Intensity
        dephasage = self.dephasage

        List_distance = self.get_distance_in_tissue(Target)

        for tissue in self.List_Tissue:
            for i in range (0, len(List_distance)-1):
                if tissue == tissue:
                    distance = np.linalg.norm(List_distance[i+1][1] - List_distance[i][1])
                    absorption_coeff = tissue.absorption_coefficients["Intensity"]
                    Intensity = Intensity * np.exp(-absorption_coeff * distance)
                    c = 3e8 / np.sqrt(tissue.absorption_coefficients["refractive_index"])
                    dephasage += 2 * np.pi * self.f * (distance / c) % (2 * np.pi)