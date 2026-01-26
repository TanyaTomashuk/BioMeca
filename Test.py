import cupy as cp  # drop-in replacement de numpy
import numpy as np
import matplotlib.pyplot as plt

# Config
n_ondes = 10000  # très grand
t = cp.linspace(0, 1, 100000)
frequencies = cp.random.uniform(4, 6, n_ondes)
phases = cp.random.uniform(0, 2*cp.pi, n_ondes)
amplitudes = cp.ones(n_ondes)

# Calcul vectorisé (matrice temps × fréquences)
# Shape: (len(t), n_ondes)
ondes = amplitudes * cp.sin(2*cp.pi * frequencies[None, :] * t[:, None] + phases[None, :])

# Superposition (somme sur l'axe des ondes)
interference = cp.sum(ondes, axis=1)

# Ramener sur CPU si besoin
result = cp.asnumpy(interference)

plt.figure()
plt.plot(t, result)
plt.show()