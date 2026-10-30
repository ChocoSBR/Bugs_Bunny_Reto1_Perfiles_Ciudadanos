"""
Generación de gráficas - Hackathon INE 2026, Reto 1.

Equipo Bugs Bunny.

El script utiliza las bases procesadas y los resultados del
clustering para generar nueve gráficas en formatos PNG y PDF.

Ejecución desde la raíz del proyecto:
    python src/graficas_finales.py

Los archivos se guardan en graficas/graficos finales/.
"""
from pathlib import Path
import unicodedata

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Configuración
# ------------------------------------------------------------------
RAIZ = Path(".")
PERFILES = RAIZ / "perfiles"
PROCESADOS = RAIZ / "datos" / "procesados"
SALIDA = RAIZ / "graficas" / "graficos finales"
SALIDA.mkdir(parents=True, exist_ok=True)

YEARS = [2009, 2012, 2015, 2018, 2021, 2024]

# Escribe aquí el nombre exacto de la columna si la detección automática falla
COLS = {"perfil": None, "sexo": None, "seccion": None, "edad": None}

# De mayor a menor participación: alta, media-alta, media-baja, baja
PALETA = ["#8B2D6F", "#C9588F", "#F0A04B", "#2E86AB"]

plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.axisbelow": True,
})


# ------------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------------
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return s.lower()


def leer(ruta):
    if not ruta.exists():
        raise FileNotFoundError(f"No existe {ruta}. ¿Ejecutas desde la raíz del repo?")
    return pd.read_csv(ruta)


def col(df, *opciones):
    """Busca columnas por prioridad de opciones (prefiere PERFIL a CLUSTER)."""
    for o in opciones:
        for c in df.columns:
            if o in norm(c):
                return c
    raise KeyError(f"No encontré columna con {opciones}. Columnas: {list(df.columns)}")


def buscar(df, clave, *opciones):
    return COLS[clave] if COLS.get(clave) else col(df, *opciones)


def columnas_anio(df):
    """Una columna de tasa por cada año (prefiere las que contienen 'part')."""
    salida = []
    for y in YEARS:
        cands = [c for c in df.columns if str(y) in str(c)]
        pref = [c for c in cands if "part" in norm(c)] or cands
        if not pref:
            raise KeyError(f"No encontré columna del año {y}. Columnas: {list(df.columns)}")
        salida.append(pref[0])
    return salida


def rango(nombre):
    n = norm(nombre)
    if "media" in n and "alta" in n:
        return 1
    if "media" in n and "baja" in n:
        return 2
    if "alta" in n:
        return 0
    if "baja" in n:
        return 3
    return 9


def color_de(nombre):
    r = rango(nombre)
    return PALETA[r] if r < len(PALETA) else "#888888"


def etiqueta(nombre):
    t = str(nombre)
    for pref in ("Participación históricamente ", "Participacion historicamente "):
        t = t.replace(pref, "")
    return t.strip().capitalize()


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(SALIDA / f"{nombre}.png", dpi=300, bbox_inches="tight")
    fig.savefig(SALIDA / f"{nombre}.pdf", bbox_inches="tight")
    plt.close(fig)
    print("✓", nombre)


def asignaciones():
    df = leer(PERFILES / "asignaciones_perfiles_k4.csv")
    return df, buscar(df, "perfil", "perfil", "cluster")


# ------------------------------------------------------------------
# Gráficas
# ------------------------------------------------------------------
def g01_trayectorias():
    df = leer(PERFILES / "resumen_trayectorias_perfiles_k4.csv")
    c_p = buscar(df, "perfil", "perfil", "cluster")
    c_y = columnas_anio(df)
    df = df.assign(_o=df[c_p].map(rango)).sort_values("_o")

    fig, ax = plt.subplots(figsize=(8, 5))
    for _, f in df.iterrows():
        ax.plot(YEARS, f[c_y].astype(float).values, marker="o", lw=2.2,
                color=color_de(f[c_p]), label=etiqueta(f[c_p]))
    ax.set_xticks(YEARS)
    ax.set_xlabel("Elección")
    ax.set_ylabel("Participación promedio (%)")
    ax.set_title("Trayectoria de participación por perfil, 2009–2024")
    ax.legend(title="Perfil", frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left")
    guardar(fig, "01_trayectorias_perfiles")


def g02_seleccion_k():
    df = leer(PERFILES / "comparacion_kmeans_k4_k6.csv")
    c_k = next((c for c in df.columns
                if norm(c) in ("k", "n_clusters", "clusters")), df.columns[0])
    c_s = col(df, "silueta", "silhouette")
    c_i = col(df, "inercia", "inertia")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, c, titulo in ((axes[0], c_s, "Coeficiente de silueta"),
                          (axes[1], c_i, "Inercia")):
        ax.plot(df[c_k], df[c], marker="o", lw=2, color=PALETA[0])
        for k, v in zip(df[c_k], df[c]):
            ax.annotate(f"{v:,.4g}", (k, v), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=9)
        ax.set_xticks(list(df[c_k]))
        ax.set_xlabel("Número de conglomerados (k)")
        ax.set_title(titulo)
    fig.suptitle("Selección del número de perfiles (K-means)")
    guardar(fig, "02_seleccion_k")


def g03_tamano_perfiles():
    df, c_p = asignaciones()
    cuenta = df[c_p].value_counts()
    nombres = sorted(cuenta.index, key=rango)
    vals = [cuenta[n] for n in nombres]
    total = sum(vals)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    barras = ax.bar([etiqueta(n) for n in nombres], vals,
                    color=[color_de(n) for n in nombres])
    for b, v in zip(barras, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,}\n({v / total:.1%})",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.18)
    ax.set_ylabel("Unidades")
    ax.set_title("Tamaño de cada perfil")
    guardar(fig, "03_tamano_perfiles")


def composicion(clave, opciones, titulo, archivo, cmap):
    df, c_p = asignaciones()
    c_x = buscar(df, clave, *opciones)
    tab = pd.crosstab(df[c_p], df[c_x], normalize="index") * 100
    tab = tab.loc[sorted(tab.index, key=rango)]
    tab = tab[sorted(tab.columns, key=lambda x: str(x))]
    tab.index = [etiqueta(i) for i in tab.index]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    tab.iloc[::-1].plot(kind="barh", stacked=True, ax=ax, colormap=cmap, width=0.75)
    ax.set_xlabel("% de unidades del perfil")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    ax.set_title(titulo)
    ax.legend(title=str(c_x), bbox_to_anchor=(1.01, 1), loc="upper left", frameon=False)
    guardar(fig, archivo)


def base_comparable():
    df = leer(PROCESADOS / "base_historica_comparable_2009_2024.csv")
    return df, columnas_anio(df)


def g07_participacion_por_eleccion():
    df, c_y = base_comparable()
    medias = df[c_y].astype(float).mean()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.bar([str(y) for y in YEARS], medias.values, color=PALETA[0])
    for b, v in zip(barras, medias.values):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.1f}%", ha="center",
                va="bottom", fontsize=9)
    ax.set_ylim(0, 80)
    ax.set_ylabel("Promedio simple de participación (%)")
    ax.set_title("Participación promedio por elección (unidades comparables)")
    guardar(fig, "07_participacion_por_eleccion")


def g08_participacion_por_edad():
    df, c_y = base_comparable()
    c_e = buscar(df, "edad", "edad")
    df = df.assign(_prom=df[c_y].astype(float).mean(axis=1))
    serie = df.groupby(c_e)["_prom"].mean()
    serie = serie.loc[sorted(serie.index, key=lambda x: str(x))]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    colores = [PALETA[0] if v == serie.max() else "#C9A3BB" for v in serie.values]
    barras = ax.bar(serie.index.astype(str), serie.values, color=colores)
    for b, v in zip(barras, serie.values):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.1f}", ha="center",
                va="bottom", fontsize=8)
    ax.set_ylabel("Participación histórica promedio (%)")
    ax.set_xlabel("Grupo de edad")
    ax.set_title("Participación histórica promedio por grupo de edad")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    guardar(fig, "08_participacion_por_edad")


def g09_correlaciones():
    df = pd.read_csv(PROCESADOS / "correlaciones_participacion_2009_2024.csv", index_col=0)
    m = df.astype(float).values

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(m, cmap="Purples", vmin=0.6, vmax=1)
    ax.set_xticks(range(m.shape[1]))
    ax.set_xticklabels(df.columns, rotation=45, ha="right")
    ax.set_yticks(range(m.shape[0]))
    ax.set_yticklabels(df.index)
    ax.grid(False)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            ax.text(j, i, f"{m[i, j]:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if m[i, j] > 0.85 else "black")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Correlación")
    ax.set_title("Correlación de participación entre elecciones")
    guardar(fig, "09_correlaciones")


# ------------------------------------------------------------------
if __name__ == "__main__":
    tareas = [
        ("01", g01_trayectorias),
        ("02", g02_seleccion_k),
        ("03", g03_tamano_perfiles),
        ("04", lambda: composicion("sexo", ("sexo",), "Composición por sexo de cada perfil",
                                   "04_composicion_sexo", "Set2")),
        ("05", lambda: composicion("seccion", ("tiposec", "seccion"), "Composición por tipo de sección de cada perfil",
                                   "05_composicion_seccion", "Set2")),
        ("06", lambda: composicion("edad", ("edad",), "Composición por grupo de edad de cada perfil",
                                   "06_composicion_edad", "tab20")),
        ("07", g07_participacion_por_eleccion),
        ("08", g08_participacion_por_edad),
        ("09", g09_correlaciones),
    ]
    for id_, f in tareas:
        try:
            f()
        except Exception as e:  # sigue con las demás gráficas
            print(f"✗ gráfica {id_}: {type(e).__name__}: {e}")
