# ============================================
# EL JUEGO DE LA SIMULACIÓN - Grupo X
# Escenario 1: RNA-seq con genes diferenciales
# ============================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# 1. CONFIGURACIÓN
rng = np.random.default_rng(seed=2024)  # SEMILLA FIJA
N_GENES = 100            # genes del dataset
N_DIFF = 5               # genes realmente diferenciales
N_REP = 6                # réplicas por condición (control y tratado)
MU_MIN, MU_MAX = 10, 1000  # rango de expresión base (log-uniforme)
DISPERSION = 0.1         # alpha: Var = mu + alpha * mu^2
FOLD_CHANGES = np.array([0.25, 0.5, 2, 3, 4])  # efecto de los genes DE
ALPHA_TEST = 0.05        # nivel de significación (FDR)


# 2. GENERACIÓN DE DATOS
def nb_params(mu, alpha):
    """Traduce (media, dispersión) a los (n, p) que usa numpy/scipy."""
    n = 1 / alpha
    p = n / (n + mu)
    return n, p

def generar_datos(rng, n_genes=N_GENES, n_diff=N_DIFF, n_rep=N_REP,
                  alpha=DISPERSION, fold_changes=FOLD_CHANGES):
    # 1. media base por gen, log-uniforme entre MU_MIN y MU_MAX
    mu_base = np.exp(rng.uniform(np.log(MU_MIN), np.log(MU_MAX), size=n_genes))
    # 2. elegir los genes diferenciales y su fold change
    genes_de = rng.choice(n_genes, size=n_diff, replace=False)
    fc = np.ones(n_genes)
    fc[genes_de] = rng.permutation(fold_changes)
    # 3. matriz de medias: columnas control y tratado
    mu_ctrl = np.repeat(mu_base[:, None], n_rep, axis=1)
    mu_trat = np.repeat((mu_base * fc)[:, None], n_rep, axis=1)
    mu = np.hstack([mu_ctrl, mu_trat])            # (n_genes, 2*n_rep)
    # 4. conteos NB
    n, p = nb_params(mu, alpha)
    conteos = rng.negative_binomial(n, p)
    grupos = np.array([0] * n_rep + [1] * n_rep)  # 0 = control, 1 = tratado
    return conteos, grupos, genes_de, mu


# 3. VALIDACIÓN
def validar(datos, distribucion, titulo="", **params):
    datos = np.asarray(datos).ravel()
    dist = distribucion(**params)

    print(f"--- {titulo} (N={len(datos)}) ---")
    print(f"media:    empírica={datos.mean():9.2f}   teórica={dist.mean():9.2f}")
    print(f"varianza: empírica={datos.var(ddof=1):9.2f}   teórica={dist.var():9.2f}")
    print(f"var/media empírica = {datos.var(ddof=1) / datos.mean():.2f}  (Poisson daría 1)")

    k = max(5, min(20, len(datos) // 10))
    cortes = np.unique(dist.ppf(np.linspace(0, 1, k + 1)[1:-1]))
    bordes = np.concatenate([[-0.5], cortes + 0.5, [np.inf]])
    observados = np.histogram(datos, bins=bordes)[0]
    esperados = len(datos) * np.diff(dist.cdf(bordes - 0.5))
    esperados *= observados.sum() / esperados.sum()   # ajuste numérico: chisquare exige sumas iguales
    chi2, pval = stats.chisquare(observados, esperados)
    print(f"chi-cuadrado = {chi2:.2f}, gl = {len(observados) - 1}, p-valor = {pval:.3g}")

    fig, ax = plt.subplots(figsize=(5, 5))
    probs = (np.arange(1, len(datos) + 1) - 0.5) / len(datos)
    teoricos = dist.ppf(probs)
    ax.scatter(teoricos, np.sort(datos), s=8, alpha=0.6)
    lim = [0, max(teoricos.max(), datos.max())]
    ax.plot(lim, lim, "r--", label="y = x")
    ax.set_xlabel("cuantiles teóricos"); ax.set_ylabel("cuantiles empíricos")
    ax.set_title(f"QQ-plot {titulo}"); ax.legend()
    return {"chi2": chi2, "pval": pval, "fig": fig}

def validar_matriz(conteos, mu, alpha, genes_de):
    no_de = np.setdiff1d(np.arange(conteos.shape[0]), genes_de)
    m = conteos[no_de].mean(axis=1)
    v = conteos[no_de].var(axis=1, ddof=1)
    print(f"genes con varianza > media: {(v > m).sum()} de {len(no_de)}")
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(m, v, s=12, label="genes simulados")
    x = np.logspace(np.log10(m.min()), np.log10(m.max()), 100)
    ax.plot(x, x, "k--", label="Poisson: var = media")
    ax.plot(x, x + alpha * x**2, "r-", label=r"NB: var = $\mu + \alpha\mu^2$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("media por gen"); ax.set_ylabel("varianza por gen"); ax.legend()
    return fig

# 4. LÓGICA DEL JUEGO
def benjamini_hochberg(pvals):
    """p-valores ajustados por FDR (Benjamini-Hochberg)."""
    m = len(pvals)
    orden = np.argsort(pvals)
    ajustados = pvals[orden] * m / np.arange(1, m + 1)
    ajustados = np.minimum.accumulate(ajustados[::-1])[::-1]   # forzar monotonía
    resultado = np.empty(m)
    resultado[orden] = np.minimum(ajustados, 1)
    return resultado


def test_por_gen(conteos, grupos):
    """t de Welch sobre log2(conteo + 1), un test por gen."""
    log_c = np.log2(conteos + 1)
    _, pvals = stats.ttest_ind(log_c[:, grupos == 0], log_c[:, grupos == 1],
                               axis=1, equal_var=False)
    return pvals


def puntuar(eleccion, genes_de):
    eleccion, genes_de = set(eleccion), set(genes_de)
    aciertos = len(eleccion & genes_de)
    falsos = len(eleccion - genes_de)
    return aciertos, falsos, aciertos - falsos     # +1 por acierto, -1 por falso positivo


def jugar(rng, eleccion=None):
    """
    Reglas:
    1. Se genera una matriz de conteos (100 genes x 8 muestras: 4 control, 4 tratado).
    2. El jugador ve la tabla y puede correr test_por_gen / benjamini_hochberg.
    3. Elige 5 genes que cree diferenciales.
    4. Puntaje: +1 por cada acierto, -1 por cada falso positivo.
    5. Se revela la respuesta y cómo le fue al test automático.
    """
    conteos, grupos, genes_de, mu = generar_datos(rng)
    cols = [f"ctrl_{i+1}" for i in range(N_REP)] + [f"trat_{i+1}" for i in range(N_REP)]
    tabla = pd.DataFrame(conteos, columns=cols, index=[f"gen_{g:03d}" for g in range(N_GENES)])
    print(tabla.to_string())

    if eleccion is None:
        texto = input(f"\nElegí {N_DIFF} genes (números separados por coma): ")
        eleccion = [int(x) for x in texto.split(",")]

    aciertos, falsos, puntaje = puntuar(eleccion, genes_de)
    print(f"\nTu elección: {sorted(eleccion)}")
    print(f"Genes diferenciales reales: {sorted(genes_de.tolist())}")
    print(f"Aciertos: {aciertos}  Falsos positivos: {falsos}  Puntaje: {puntaje}")

    # Lo que hubiera hecho la estadística
    pvals = test_por_gen(conteos, grupos)
    padj = benjamini_hochberg(pvals)
    sin_corregir = np.where(pvals < ALPHA_TEST)[0]
    con_fdr = np.where(padj < ALPHA_TEST)[0]
    top5 = np.argsort(pvals)[:N_DIFF]
    print(f"\nTest sin corregir (p < {ALPHA_TEST}): {len(sin_corregir)} genes -> "
          f"{puntuar(sin_corregir, genes_de)[:2]} (aciertos, falsos)")
    print(f"Con FDR de Benjamini-Hochberg: {len(con_fdr)} genes -> "
          f"{puntuar(con_fdr, genes_de)[:2]} (aciertos, falsos)")
    print(f"Top {N_DIFF} p-valores: {sorted(top5.tolist())} -> puntaje {puntuar(top5, genes_de)[2]}")

    resumen = pd.DataFrame({"mu_ctrl": mu[genes_de, 0].round(1),
                            "mu_trat": mu[genes_de, -1].round(1),
                            "p": pvals[genes_de], "p_FDR": padj[genes_de]},
                           index=[f"gen_{g:03d}" for g in genes_de])
    print("\nDetalle de los genes diferenciales:\n", resumen.to_string())
    return {"conteos": conteos, "genes_de": genes_de, "pvals": pvals, "padj": padj}


# 5. DEMOSTRACIÓN
if __name__ == "__main__":
    # Validación del generador: una sola NB con muchas muestras
    n, p = nb_params(100, DISPERSION)
    muestra = rng.negative_binomial(n, p, size=1000)
    validar(muestra, stats.nbinom, titulo="NB(mu=100, alpha=0.1)", n=n, p=p)
    validar(muestra, stats.poisson, titulo="mismos datos vs Poisson", mu=100)  # control: debe fallar

    # Validación de la matriz del juego: varianza > media
    conteos, grupos, genes_de, mu = generar_datos(rng)
    validar_matriz(conteos, mu, DISPERSION, genes_de)
    plt.show()

    jugar(rng)
