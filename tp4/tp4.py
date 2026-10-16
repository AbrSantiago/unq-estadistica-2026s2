# ============================================
# EL JUEGO DE LA SIMULACIÓN - Grupo X
# Escenario: [nombre]
# ============================================

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# 1. CONFIGURACIÓN
rng = np.random.default_rng(seed=2024) # SEMILLA FIJA
N = 100 # tamaño de muestra
# ... parámetros del escenario


# 2. GENERACIÓN DE DATOS
def generar_datos(rng, n, **params):
    """
    Genera datos simulados según la distribución elegida.
    Justificar la elección aquí.
    """
    # ... implementación
    return datos


# 3. VALIDACIÓN
def validar(datos, distribucion, **params):
    """
    Compara datos simulados con la distribución teórica.
    - QQ-plot
    - Media y varianza empíricas vs teóricas
    - Test de bondad de ajuste
    """
    # ... implementación
    pass


# 4. LÓGICA DEL JUEGO
def jugar(rng):
    """
    Implementa las reglas del juego.
    """
    pass


# 5. DEMOSTRACIÓN
if __name__ == "__main__":
    datos = generar_datos(rng, N)
    validar(datos, stats.norm, loc=0, scale=1)
    jugar(rng)