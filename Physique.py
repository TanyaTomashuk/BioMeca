import numpy as np


def absorption(intensity_incidente, coefficient_absorption, distance):
    return intensity_incidente * np.exp(-coefficient_absorption * distance)

def reflexion(intensity_incidente, coefficient_reflexion):
    return intensity_incidente * coefficient_reflexion

def transmission(intensity_incidente, coefficient_transmission):
    return intensity_incidente * coefficient_transmission

def Puissance_thermique_par_Absorption(intensity_incidente, coefficient_absorption):
    return intensity_incidente * coefficient_absorption