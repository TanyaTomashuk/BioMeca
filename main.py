import numpy as np
from Tissue import Tissue
from Wave_dealer import wave_dealer
from meshing import mesh
import Physique


class BioMecaController:
    
    def __init__(self):
        """Initialisation du contrôleur"""
        self.tissues = []
        self.waves = []
        self.mesh = None
        
    def add_tissue(self, name, center, radius, absorption_coeff, refractive_index):
        """Ajouter un tissu à la simulation"""
        tissue = Tissue(name, center, radius, absorption_coeff, refractive_index)
        self.tissues.append(tissue)
        return tissue
    
    def add_wave(self, frequency, start_pos, phase, intensity):
        """Ajouter une onde à la simulation"""
        wave = wave_dealer(frequency, start_pos, phase, intensity, self.tissues)
        self.waves.append(wave)
        return wave
    
    def create_mesh(self, N):
        """Créer le maillage"""
        if len(self.tissues) >= 3:
            self.mesh = mesh(N, self.tissues)
            return self.mesh
        else:
            raise ValueError("Au moins 3 tissus nécessaires pour le maillage")
    
    def compute_absorption(self, intensity, coeff, distance):
        """Calculer l'absorption"""
        return Physique.absorption(intensity, coeff, distance)
    
    def compute_reflexion(self, intensity, coeff):
        """Calculer la réflexion"""
        return Physique.reflexion(intensity, coeff)
    
    def compute_transmission(self, intensity, coeff):
        """Calculer la transmission"""
        return Physique.transmission(intensity, coeff)
    
    def compute_thermal_power(self, intensity, coeff):
        """Calculer la puissance thermique"""
        return Physique.Puissance_thermique_par_Absorption(intensity, coeff)
    
    def get_status(self):
        """Afficher le statut de la simulation"""
        print(f"=== BioMeca Simulation Status ===")
        print(f"Tissus: {len(self.tissues)}")
        print(f"Ondes: {len(self.waves)}")
        print(f"Maillage: {'Créé' if self.mesh else 'Non créé'}")
        for i, tissue in enumerate(self.tissues):
            print(f"  Tissu {i+1}: {tissue.name} (R={tissue.Radius}m)")


# Exemple d'utilisation
if __name__ == "__main__":
    # Initialisation
    controller = BioMecaController()
    
    # Ajouter des tissus
    skull = controller.add_tissue("skull", np.array([0,0,0]), 0.15, 0.0, 1.8)
    brain = controller.add_tissue("brain", np.array([0,0,0]), 0.12, 0.0, 1.5)
    tumor = controller.add_tissue("tumor", np.array([0.05,0.05,0]), 0.00, 0.8, 1.6)
    
    # Ajouter une onde
    wave = controller.add_wave(frequency=1e6, 
                               start_pos=np.array([0,0,-0.2]), 
                               phase=0.0, 
                               intensity=100.0)
    
    # Créer le maillage
    controller.create_mesh(N=1000)
    
    # Calculs physiques
    absorption = controller.compute_absorption(100.0, 0.5, 0.1)
    print(f"Absorption: {absorption:.2f} W/m²")
    
    # Afficher le statut
    controller.get_status()