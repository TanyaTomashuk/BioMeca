#!/usr/bin/env python3
"""
Test simple: Interférence entre deux ondes avec diffusion sur un plan
Visualisation 2D et 3D avec normalisation correcte
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


class InterferenceSimulator:
    """Simulateur d'interférence entre deux sources d'ondes"""
    
    def __init__(self, frequency, wavelength, grid_size=200):
        """
        Initialisation
        
        Args:
            frequency: Fréquence de l'onde (Hz)
            wavelength: Longueur d'onde (m)
            grid_size: Taille de la grille de calcul
        """
        self.f = frequency
        self.wavelength = wavelength
        self.k = 2 * np.pi / wavelength  # Nombre d'onde
        self.grid_size = grid_size
        
        # Sources d'ondes
        self.sources = []
        
    def add_source(self, position, amplitude=1.0, phase=0.0):
        """
        Ajouter une source d'onde
        
        Args:
            position: Position [x, y] de la source
            amplitude: Amplitude de l'onde
            phase: Phase initiale (radians)
        """
        self.sources.append({
            'position': np.array(position),
            'amplitude': amplitude,
            'phase': phase
        })
        
    def compute_interference_pattern(self, plane_bounds, z_plane=0, normalize=True):
        """
        Calculer le pattern d'interférence sur un plan
        
        Args:
            plane_bounds: [(x_min, x_max), (y_min, y_max)]
            z_plane: Position z du plan d'observation
            normalize: Si True, normalise l'intensité entre 0 et 1
            
        Returns:
            X, Y, intensity: Grilles pour la visualisation
        """
        # Créer la grille du plan
        x = np.linspace(plane_bounds[0][0], plane_bounds[0][1], self.grid_size)
        y = np.linspace(plane_bounds[1][0], plane_bounds[1][1], self.grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Initialiser le champ total
        field_real = np.zeros_like(X)
        field_imag = np.zeros_like(X)
        
        # Calculer la contribution de chaque source
        for source in self.sources:
            # Distance de la source à chaque point du plan
            dx = X - source['position'][0]
            dy = Y - source['position'][1]
            dz = z_plane  # Si les sources sont à z=0
            
            r = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # Onde plane (pas de décroissance en 1/r pour éviter les singularités)
            # On garde juste la phase
            amplitude = source['amplitude']
            phase = self.k * r + source['phase']
            
            # Décomposition en partie réelle et imaginaire
            field_real += amplitude * np.cos(phase)
            field_imag += amplitude * np.sin(phase)
        
        # Intensité = |champ|^2
        intensity = field_real**2 + field_imag**2
        
        # Normalisation pour meilleure visualisation
        if normalize:
            intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min() + 1e-10)
        
        return X, Y, intensity
    
    def visualize_2d(self, plane_bounds, z_plane=0, title="Interférence entre deux ondes"):
        """
        Visualiser le pattern d'interférence en 2D
        
        Args:
            plane_bounds: [(x_min, x_max), (y_min, y_max)]
            z_plane: Position z du plan d'observation
            title: Titre du graphique
        """
        X, Y, intensity = self.compute_interference_pattern(plane_bounds, z_plane)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pattern d'interférence
        im1 = ax1.contourf(X, Y, intensity, levels=50, cmap='RdYlBu_r')
        ax1.set_xlabel('x (m)')
        ax1.set_ylabel('y (m)')
        ax1.set_title(title)
        ax1.set_aspect('equal')
        
        # Marquer les positions des sources
        for i, source in enumerate(self.sources):
            ax1.plot(source['position'][0], source['position'][1], 
                    'r*', markersize=15, label=f'Source {i+1}')
        ax1.legend()
        plt.colorbar(im1, ax=ax1, label='Intensité normalisée')
        
        # Coupe transversale au milieu
        mid_idx = self.grid_size // 2
        ax2.plot(X[mid_idx, :], intensity[mid_idx, :], 'b-', linewidth=2)
        ax2.set_xlabel('x (m)')
        ax2.set_ylabel('Intensité')
        ax2.set_title('Coupe transversale (y = 0)')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1])
        
        plt.tight_layout()
        return fig
    
    def visualize_3d(self, plane_bounds, z_plane=0, title="Interférence 3D"):
        """
        Visualiser le pattern d'interférence en 3D avec normalisation
        
        Args:
            plane_bounds: [(x_min, x_max), (y_min, y_max)]
            z_plane: Position z du plan d'observation
            title: Titre du graphique
        """
        X, Y, intensity = self.compute_interference_pattern(plane_bounds, z_plane, normalize=True)
        
        fig = plt.figure(figsize=(18, 6))
        
        # Vue 3D - Surface
        ax1 = fig.add_subplot(131, projection='3d')
        surf = ax1.plot_surface(X*1000, Y*1000, intensity, cmap='hot', 
                                linewidth=0, antialiased=True, alpha=0.9,
                                vmin=0, vmax=1)
        ax1.set_xlabel('x (mm)')
        ax1.set_ylabel('y (mm)')
        ax1.set_zlabel('Intensité normalisée')
        ax1.set_zlim([0, 1])
        ax1.set_title('Vue 3D - Surface')
        ax1.view_init(elev=25, azim=45)
        fig.colorbar(surf, ax=ax1, shrink=0.5)
        
        # Vue 3D - Wireframe avec plus de détails
        ax2 = fig.add_subplot(132, projection='3d')
        # Sous-échantillonner pour le wireframe (plus lisible)
        step = max(1, self.grid_size // 40)
        ax2.plot_wireframe(X[::step, ::step]*1000, Y[::step, ::step]*1000, 
                          intensity[::step, ::step], 
                          color='blue', alpha=0.7, linewidth=1)
        ax2.set_xlabel('x (mm)')
        ax2.set_ylabel('y (mm)')
        ax2.set_zlabel('Intensité normalisée')
        ax2.set_zlim([0, 1])
        ax2.set_title('Vue 3D - Wireframe')
        ax2.view_init(elev=25, azim=135)
        
        # Vue de dessus avec contours
        ax3 = fig.add_subplot(133)
        contour = ax3.contourf(X*1000, Y*1000, intensity, levels=30, cmap='hot', vmin=0, vmax=1)
        ax3.contour(X*1000, Y*1000, intensity, levels=10, colors='black', linewidths=0.5, alpha=0.4)
        
        # Marquer les sources
        for i, source in enumerate(self.sources):
            ax3.plot(source['position'][0]*1000, source['position'][1]*1000, 
                    'w*', markersize=20, markeredgecolor='red', markeredgewidth=2,
                    label=f'Source {i+1}')
        
        ax3.set_xlabel('x (mm)')
        ax3.set_ylabel('y (mm)')
        ax3.set_title('Vue de dessus')
        ax3.set_aspect('equal')
        ax3.legend()
        cbar = fig.colorbar(contour, ax=ax3)
        cbar.set_label('Intensité normalisée')
        
        plt.suptitle(title, fontsize=14, y=0.98)
        plt.tight_layout()
        return fig


def test_two_sources():
    """Test avec deux sources cohérentes"""
    
    print("=" * 60)
    print("TEST: Interférence entre deux sources cohérentes")
    print("=" * 60)
    
    # Créer le dossier results s'il n'existe pas
    os.makedirs('results', exist_ok=True)
    
    # Paramètres
    frequency = 1e6  # 1 MHz
    wavelength = 1.5e-3  # 1.5 mm
    
    # Créer le simulateur
    sim = InterferenceSimulator(frequency, wavelength, grid_size=300)
    
    # Ajouter deux sources séparées
    distance_sources = 5 * wavelength  # Séparation = 5 longueurs d'onde
    sim.add_source(position=[-distance_sources/2, 0], amplitude=1.0, phase=0.0)
    sim.add_source(position=[distance_sources/2, 0], amplitude=1.0, phase=0.0)
    
    print(f"Fréquence: {frequency/1e6} MHz")
    print(f"Longueur d'onde: {wavelength*1e3:.2f} mm")
    print(f"Séparation des sources: {distance_sources*1e3:.2f} mm")
    print(f"Nombre de sources: {len(sim.sources)}")
    
    # Plan d'observation
    plane_bounds = [(-0.02, 0.02), (-0.01, 0.03)]
    
    # Visualisation 2D
    fig_2d = sim.visualize_2d(plane_bounds, z_plane=0, 
                              title="Interférence - Deux sources cohérentes en phase")
    output_2d = 'results/interference_2sources_2D.png'
    plt.savefig(output_2d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 2D sauvegardé: {output_2d}")
    plt.close()
    
    # Visualisation 3D
    fig_3d = sim.visualize_3d(plane_bounds, z_plane=0,
                              title="Interférence 3D - Deux sources cohérentes")
    output_3d = 'results/interference_2sources_3D.png'
    plt.savefig(output_3d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 3D sauvegardé: {output_3d}")
    plt.close()


def test_destructive_interference():
    """Test avec deux sources en opposition de phase"""
    
    print("\n" + "=" * 60)
    print("TEST: Interférence destructive (sources déphasées π)")
    print("=" * 60)
    
    os.makedirs('results', exist_ok=True)
    
    frequency = 1e6
    wavelength = 1.5e-3
    
    sim = InterferenceSimulator(frequency, wavelength, grid_size=300)
    
    # Deux sources avec opposition de phase
    distance_sources = 5 * wavelength
    sim.add_source(position=[-distance_sources/2, 0], amplitude=1.0, phase=0.0)
    sim.add_source(position=[distance_sources/2, 0], amplitude=1.0, phase=np.pi)
    
    print(f"Source 1: phase = 0")
    print(f"Source 2: phase = π (opposition de phase)")
    
    plane_bounds = [(-0.02, 0.02), (-0.01, 0.03)]
    
    # 2D
    fig_2d = sim.visualize_2d(plane_bounds, z_plane=0,
                              title="Interférence destructive (π déphasage)")
    output_2d = 'results/interference_destructive_2D.png'
    plt.savefig(output_2d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 2D sauvegardé: {output_2d}")
    plt.close()
    
    # 3D
    fig_3d = sim.visualize_3d(plane_bounds, z_plane=0,
                              title="Interférence 3D - Opposition de phase")
    output_3d = 'results/interference_destructive_3D.png'
    plt.savefig(output_3d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 3D sauvegardé: {output_3d}")
    plt.close()


def test_multiple_sources():
    """Test avec 4 sources en carré"""
    
    print("\n" + "=" * 60)
    print("TEST: Interférence avec 4 sources (configuration carrée)")
    print("=" * 60)
    
    os.makedirs('results', exist_ok=True)
    
    frequency = 1e6
    wavelength = 1.5e-3
    
    sim = InterferenceSimulator(frequency, wavelength, grid_size=400)
    
    # 4 sources aux coins d'un carré
    d = 3 * wavelength
    sim.add_source(position=[-d, -d], amplitude=1.0, phase=0.0)
    sim.add_source(position=[d, -d], amplitude=1.0, phase=0.0)
    sim.add_source(position=[-d, d], amplitude=1.0, phase=0.0)
    sim.add_source(position=[d, d], amplitude=1.0, phase=0.0)
    
    print(f"4 sources en configuration carrée")
    print(f"Côté du carré: {2*d*1e3:.2f} mm")
    
    plane_bounds = [(-0.015, 0.015), (-0.015, 0.015)]
    
    # 2D
    fig_2d = sim.visualize_2d(plane_bounds, z_plane=0,
                              title="Interférence - 4 sources en carré")
    output_2d = 'results/interference_4sources_2D.png'
    plt.savefig(output_2d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 2D sauvegardé: {output_2d}")
    plt.close()
    
    # 3D
    fig_3d = sim.visualize_3d(plane_bounds, z_plane=0,
                              title="Interférence 3D - 4 sources en carré")
    output_3d = 'results/interference_4sources_3D.png'
    plt.savefig(output_3d, dpi=150, bbox_inches='tight')
    print(f"✓ Graphique 3D sauvegardé: {output_3d}")
    plt.show()
    plt.close()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  SIMULATION D'INTERFÉRENCE - DIFFUSION SUR UN PLAN      ║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Exécuter les tests
    test_two_sources()
    test_destructive_interference()
    test_multiple_sources()
    
    print("\n" + "=" * 60)
    print("✓ Tous les tests terminés avec succès!")
    print(f"✓ Tous les fichiers sauvegardés dans: {os.path.abspath('results')}")
    print("=" * 60)