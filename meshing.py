import array
from ast import List
from csv import Error
from math import sqrt
import numpy as np
from Tissue import Tissue



class mesh():
    def __init__(self, N : int, List_Tissue : List[Tissue]) :

        for i in range(0, len(List_Tissue) - 1):
            if (np.linalg(List_Tissue[i+1].Center) + List_Tissue[i+1].Radius > List_Tissue[i].Radius) :
                raise Error("Liste des tissues mal créée")
        
        self.List_Tissue = List_Tissue

        self.meshs = self.meshing()
        

    def cercle(N : int, pos : np.array[float], R_min : float, R_max : float):
        Points = []
        i_max = int(N**(1/3))
        j_max = int(N**(1/3))
        l_max = int(N**(1/3))
        for i in range (0, i_max):
            for j in range (0, j_max):
                for l in range (0, l_max):
                    Rayon = i / i_max * (R_max - R_min) + R_min
                    Theta = 2 * np.pi * j / j_max
                    Phi = np.pi * l / l_max
                    Points.append(np.array([pos[0] + Rayon * np.sin(Theta) * np.cos(Phi), pos[1] + Rayon * np.sin(Theta) * np.sin(Phi), pos[2] + Rayon * np.cos(Theta)]))

        return np.array(Points)


    def mesh_exclude(mesh : List[np.array], pos : np.array[float], R_max : float):
        Point = []
        for point in mesh : 
            if np.linalg.norm(point - pos) > R_max :
                Point.append(point)
        
        return Point


    def meshing(self):

        skull_mesh = self.cercle(self.N ** (1/2), np.array([0,0,0]), self.R_brain, self.R_skull)
        brain_mesh = self.cercle(self.N ** (1/3), np.array([0,0,0]), 0e-2, self.R_brain)
        tumor_mesh = self.cercle(self.N ** (1/3), self.tumor_pos, 0e-2, self.R_tumor)
        
        skull_mesh = self.mesh_exclude(skull_mesh, np.array([0,0,0]), self.R_brain)
        brain_mesh = self.mesh_exclude(brain_mesh, self.tumor_pos, self.R_tumor)

        return [skull_mesh, brain_mesh, tumor_mesh]
    

    
    


