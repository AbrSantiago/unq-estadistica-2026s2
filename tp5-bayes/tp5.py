# ============================================================
# TP5 - Probabilidad condicional, Bayes y Cox-Jaynes
# Esqueleto: lo marcado con TODO lo completás vos.
# Lo que NO es TODO es "plomería" (leer archivos, imprimir tablas).
#
# Correr:  uv run python tp5-bayes/tp5.py
# Cada sección que todavía tenga TODOs se muestra como "pendiente",
# así podés ir completando de a una y ver el progreso.
# ============================================================

from dataclasses import dataclass, field
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
DATOS = AQUI / "datafiles"


# ------------------------------------------------------------
# 0. ÁRBOLES
# Un árbol es un Nodo con 0 hijos (hoja = observada) o 2 hijos
# (nodo interno = variable oculta).
# ------------------------------------------------------------
@dataclass
class Nodo:
    nombre: str
    hijos: list["Nodo"] = field(default_factory=list)

    def es_hoja(self) -> bool:
        return not self.hijos


def H(nombre):  # atajo para hojas
    return Nodo(nombre)


#        raíz
#       /    \
#      X      Y
#     / \    / \
#    A   B  C   D
ARBOL_A = Nodo("raiz", [Nodo("X", [H("A"), H("B")]), Nodo("Y", [H("C"), H("D")])])
OBS_A = {"A": "I", "B": "V", "C": "L", "D": "I"}

#   N0 (raíz)
#   ├── MICU2_Dr
#   └── N1  ("Ancestro MICU1/2": el nodo de la duplicación)
#       ├── MICU1_Hs
#       └── N2  (ancestro de los MICU2 de mamíferos)
#           ├── MICU2_Mm
#           └── MICU2_Hs
ARBOL_B = Nodo(
    "N0",
    [H("MICU2_Dr"), Nodo("N1", [H("MICU1_Hs"), Nodo("N2", [H("MICU2_Mm"), H("MICU2_Hs")])])],
)
SITIOS_B = {  # columnas del alineamiento (coinciden con datafiles/micu.aln)
    182: {"MICU1_Hs": "R", "MICU2_Hs": "K", "MICU2_Mm": "K", "MICU2_Dr": "Q"},
    220: {"MICU1_Hs": "D", "MICU2_Hs": "E", "MICU2_Mm": "E", "MICU2_Dr": "I"},
    245: {"MICU1_Hs": "N", "MICU2_Hs": "D", "MICU2_Mm": "D", "MICU2_Dr": "T"},
}


# ------------------------------------------------------------
# 1. MODELO DE TRANSICIÓN (una rama = un paso de una cadena de Markov)
# ------------------------------------------------------------
P_CAMBIO = 0.3
ESTADOS_A = ["I", "V", "L", "F"]
PI_A = np.array([0.4, 0.3, 0.2, 0.0])  # tal cual el enunciado. Verificá y decidí.


def matriz_transicion(pi: np.ndarray, p: float) -> np.ndarray:
    """
    Devuelve la matriz M de k×k con M[i, j] = P(hijo = j | padre = i).
      i == j: (1-p) + p·pi[j]
      i != j: p·pi[j]
    Pista: se puede hacer en una línea con np.eye y np.outer (o broadcasting).
    """
    # TODO
    raise NotImplementedError


def verificar_filas(M: np.ndarray, estados: list[str]) -> pd.Series:
    """Suma de cada fila. Debería dar 1 en todas. ¿Da?"""
    # TODO
    raise NotImplementedError


# ------------------------------------------------------------
# 2. LIKELIHOOD: P(datos | estado de un nodo)
# ------------------------------------------------------------
def vector_hoja(estado_observado: str, estados: list[str]) -> np.ndarray:
    """
    Para una hoja, L(s) = P(dato de la hoja | hoja = s).
    Pregunta guía: si la hoja ES lo que observaste, ¿cuánto vale eso
    cuando s coincide con lo observado, y cuánto cuando no?
    """
    # TODO
    raise NotImplementedError


def likelihood_parcial(nodo: Nodo, obs: dict, M: np.ndarray, estados: list[str], tablas: dict) -> np.ndarray:
    """
    Devuelve el vector L_nodo, con L_nodo[s] = P(hojas debajo de nodo | nodo = s).
    - Si es hoja: vector_hoja.
    - Si no: combinar los vectores de los hijos usando M.
      Preguntas guía:
        * Para UN hijo h: P(hojas debajo de h | padre = s) = ?
          (marginalizá sobre el estado t del hijo: suma sobre t de ... · ...)
        * ¿Cómo combinás los dos hijos? (¿qué son entre sí, dado el padre?)
        * ¿Se puede escribir la suma sobre t como un producto matriz-vector?
    Guardá cada vector intermedio en tablas[nodo.nombre] (son las "tablas
    intermedias" que pide A1).
    """
    # TODO (recursivo)
    raise NotImplementedError


def likelihood_fuerza_bruta_A(obs: dict, M: np.ndarray, estados: list[str]) -> np.ndarray:
    """
    Versión "literal" de A1 SOLO para el árbol de la Parte A:
    para cada estado r de la raíz, sumá sobre TODAS las combinaciones (x, y)
    de estados de X e Y la probabilidad conjunta
        P(X=x, Y=y, A, B, C, D | raíz = r)
    escrita como producto de transiciones (regla del producto + independencias).
    Usá itertools.product. Devuelve un vector indexado por r.
    Sirve para validar likelihood_parcial: ambos tienen que dar lo mismo.
    """
    # TODO
    raise NotImplementedError


# ------------------------------------------------------------
# 3. BAYES
# ------------------------------------------------------------
def posterior(likelihood: np.ndarray, prior: np.ndarray) -> np.ndarray:
    """P(raíz = r | datos) para todo r. Debe sumar 1."""
    # TODO
    raise NotImplementedError


# ------------------------------------------------------------
# 4. PARSIMONIA (para comparar en A2 y en la Parte D)
# ------------------------------------------------------------
def cambios_minimos(nodo: Nodo, obs: dict, estados: list[str]) -> np.ndarray:
    """
    Opcional (en 4 hojas se puede hacer a ojo, pero codearlo está bueno).
    Devuelve C[s] = cantidad MÍNIMA de cambios en el subárbol si nodo = s.
    Es la misma recursión que likelihood_parcial, pero en vez de
    (suma, producto) usás (mínimo, suma): para cada hijo, el costo es
    min sobre t de [costo del hijo en t + (1 si t != s si no 0)].
    Hojas: 0 si coincide con lo observado, infinito si no.
    """
    # TODO
    raise NotImplementedError


# ------------------------------------------------------------
# 5. PARTE B: espacio de estados y prior desde el alineamiento
# ------------------------------------------------------------
def leer_alineamiento(ruta: Path = DATOS / "micu.aln") -> dict[str, str]:
    """Lee el CLUSTAL del profe -> {nombre: secuencia alineada con '-'}. (plomería)"""
    seqs: dict[str, str] = {}
    for linea in ruta.read_text().splitlines():
        if not linea.startswith("sp|"):
            continue
        nombre, trozo = linea.split()
        clave = nombre.split("|")[2].split("/")[0]
        seqs[clave] = seqs.get(clave, "") + trozo
    return seqs


def frecuencias_aa(seqs: dict[str, str], estados: list[str]) -> np.ndarray:
    """
    Frecuencia relativa de cada estado en TODO el alineamiento (ignorando '-').
    Es el prior de B2. Debe sumar 1.
    """
    # TODO
    raise NotImplementedError


# DECISIÓN TUYA (justificala en el PDF):
# El modelo de la Parte A tiene 4 estados (I, V, L, F) y estos sitios usan
# otras letras. Opciones razonables:
#   (a) los 20 aminoácidos, con pi uniforme (1/20) en la matriz de transición
#   (b) solo las letras observadas en ese sitio, con pi uniforme
# Pensá: ¿qué cambia entre (a) y (b)? ¿Cuál permite hacer B2 con sentido?
AMINOACIDOS = list("ACDEFGHIKLMNPQRSTVWY")
ESTADOS_B: list[str] = AMINOACIDOS  # TODO: confirmar/cambiar
PI_B: np.ndarray | None = None  # TODO


# ------------------------------------------------------------
# 6. SALIDA (plomería)
# ------------------------------------------------------------
def tabla(vectores: dict[str, np.ndarray], estados: list[str], decimales: int = 6) -> pd.DataFrame:
    return pd.DataFrame(vectores, index=estados).round(decimales)


def seccion(titulo, fn):
    print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")
    try:
        fn()
    except NotImplementedError:
        print("  (pendiente: hay TODOs sin completar)")


# ------------------------------------------------------------
# 7. EJERCICIOS
# ------------------------------------------------------------
def modelo():
    M = matriz_transicion(PI_A, P_CAMBIO)
    print(tabla({e: M[i] for i, e in enumerate(ESTADOS_A)}, ESTADOS_A).T)
    print("\nSuma por fila:\n", verificar_filas(M, ESTADOS_A))


def a1():
    M = matriz_transicion(PI_A, P_CAMBIO)
    tablas: dict[str, np.ndarray] = {}
    L = likelihood_parcial(ARBOL_A, OBS_A, M, ESTADOS_A, tablas)
    print(tabla(tablas, ESTADOS_A))
    print(f"\nP(datos | raíz = I) = {L[ESTADOS_A.index('I')]:.6g}")
    # chequeo cruzado
    L_bruto = likelihood_fuerza_bruta_A(OBS_A, M, ESTADOS_A)
    print("¿pruning == fuerza bruta?", np.allclose(L, L_bruto))


def a2_a3():
    M = matriz_transicion(PI_A, P_CAMBIO)
    L = likelihood_parcial(ARBOL_A, OBS_A, M, ESTADOS_A, {})
    priors = {
        "uniforme (A2)": np.full(4, 0.25),
        "equilibrio (A3)": np.array([0.4, 0.3, 0.2, 0.1]),
    }
    cols = {"likelihood": L}
    for nombre, pr in priors.items():
        cols[f"post {nombre}"] = posterior(L, pr)
    print(tabla(cols, ESTADOS_A))
    print("\nCambios mínimos (parsimonia):")
    print(pd.Series(cambios_minimos(ARBOL_A, OBS_A, ESTADOS_A), index=ESTADOS_A))


def parte_b():
    if PI_B is None:
        raise NotImplementedError
    M = matriz_transicion(PI_B, P_CAMBIO)
    seqs = leer_alineamiento()
    priors = {"uniforme (B1)": np.full(len(ESTADOS_B), 1 / len(ESTADOS_B)),
              "frec. alineamiento (B2)": frecuencias_aa(seqs, ESTADOS_B)}
    for sitio, obs in SITIOS_B.items():
        tablas: dict[str, np.ndarray] = {}
        likelihood_parcial(ARBOL_B, obs, M, ESTADOS_B, tablas)
        # TODO: ¿sobre qué nodo hacés Bayes? (N0, N1 o N2) -> ver nota abajo
        # TODO: imprimir solo las filas relevantes (las letras observadas)
        print(f"\n--- Sitio {sitio}: {obs}")
        raise NotImplementedError


def chequeos():
    """Si todo esto pasa, la Parte A está bien armada."""
    M = matriz_transicion(np.array([0.4, 0.3, 0.2, 0.1]), P_CAMBIO)
    assert np.allclose(M.sum(axis=1), 1), "las filas no suman 1"
    L = likelihood_parcial(ARBOL_A, OBS_A, M, ESTADOS_A, {})
    assert np.allclose(L, likelihood_fuerza_bruta_A(OBS_A, M, ESTADOS_A)), "pruning != fuerza bruta"
    for pr in (np.full(4, 0.25), np.array([0.4, 0.3, 0.2, 0.1])):
        assert np.isclose(posterior(L, pr).sum(), 1), "el posterior no suma 1"
    print("OK: todos los chequeos pasan")


if __name__ == "__main__":
    seccion("Modelo: matriz de transición", modelo)
    seccion("A1: P(datos | raíz)", a1)
    seccion("A2 / A3: posteriores y parsimonia", a2_a3)
    seccion("B1 / B2: sitios reales", parte_b)
    seccion("Chequeos", chequeos)
