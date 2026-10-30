# Hackathon INE: perfiles ciudadanos de participación electoral (2009–2024)

**Hackathon INE 2026 — «Hackea la participación: Datos que construyen democracia»**  
**Reto 1:** Perfiles ciudadanos de participación · **Equipo Bugs Bunny**

## Resumen

Este proyecto identifica **cuatro perfiles de participación electoral en unidades sociodemográficas y territoriales agregadas** a partir de los Conteos Censales de Participación Ciudadana (CCPC) del INE de 2009, 2012, 2015, 2018, 2021 y 2024. Se homologaron las seis bases con una unidad común (**entidad + grupo de edad + sexo + tipo de sección**), se obtuvieron **2,496 unidades comparables** y se aplicó K-means a sus seis tasas históricas de participación estandarizadas.

| Perfil | Unidades | Porcentaje de unidades | Participación histórica promedio por unidad |
|---|---:|---:|---:|
| Históricamente alta | 623 | 24.96 % | 71.67 % |
| Históricamente media-alta | 835 | 33.45 % | 61.26 % |
| Históricamente media-baja | 676 | 27.08 % | 50.32 % |
| Históricamente baja | 362 | 14.50 % | 38.59 % |

Los porcentajes de la tercera columna corresponden al **número de unidades**, no al número de personas que votaron. Los promedios históricos tampoco representan tasas nacionales de participación. Las cifras porcentuales de unidades pueden sumar 99.99 % por redondeo.

La solución con `k = 4` obtuvo el mayor coeficiente de silueta entre las alternativas evaluadas (`0.2895`) y mostró estabilidad al excluir temporalmente grupos pequeños (índice de Rand ajustado, `ARI = 0.9157`).

## Integrantes

- Aguilar Lara Ericka
- Bautista Reyes Sofía
- Cruz Basilio Ximena Carolina
- Jardón Marín Rodrigo

## Organización de archivos

```text
Bugs_Bunny_Reto1_Perfiles_Ciudadanos/
├── README.md                   # Descripción, metodología y guía de reproducción
├── documento_tecnico/
│   ├── Hackathon_INE_Documento.pdf
│   └── Hackathon_INE_Documento.tex
├── presentacion/
│   └── Hackathon INE presentación.pdf
├── fichas_visuales/
│   ├── Participación Consolidada.png
│   ├── Participación Constante.png
│   ├── Participación Intermitente.png
│   ├── Participación por Activar.png
│   └── README.md
├── graficas/
│   └── graficos finales/      # Nueve gráficas, cada una en PNG y PDF
├── datos/
│   ├── originales/            # Reservada; los ZIP originales del INE no se incluyen
│   ├── procesados/            # Bases agrupadas y serie histórica comparable
│   └── compatibilidad/        # Correspondencias de variables por elección
├── notebooks/                 # Diez cuadernos de procesamiento y análisis
├── perfiles/                  # Asignaciones, centroides y caracterización
└── src/
    └── graficas_finales.py   # Generación de las nueve gráficas finales
```

El **documento técnico**, la **presentación ejecutiva** y las **fichas visuales** se encuentran en carpetas independientes para facilitar su consulta. Las demás carpetas contienen los datos, el código y los resultados que respaldan el análisis.

## Datos y criterios de análisis

- **Fuente oficial:** [Plataforma CCPC del INE](https://www.ine.mx/transparencia/datos-abiertos/visualizacion-datos/conteos-censales-participacion/).
- **Unidad:** entidad federativa + grupo de edad (13 intervalos) + sexo + tipo de sección.
- **Tasa de participación por unidad:** `SV / (SV + NV) × 100`; los registros `NS` no se incluyen en el denominador de esta tasa.
- **Compatibilidad temporal:** se homologó `Distrito Federal` como `Ciudad de México`. De las 2,546 unidades reunidas, 2,496 tienen información de las seis elecciones y constituyen la base comparable. Las otras 50 son unidades de sexo no binario disponibles solo en 2024; no se les imputaron antecedentes.
- **Alcance:** los datos son agregados, sin información personal identificable. Los perfiles describen combinaciones demográficas y territoriales, **no** personas ni historiales individuales de voto.

## Metodología

1. Validar cada elección: 32 entidades, conteos y la relación `LN = SV + NV + NS`.
2. Homologar las categorías e integrar las seis elecciones.
3. Realizar un análisis exploratorio de tasas, tendencias y correlaciones.
4. Estandarizar las seis tasas históricas y evaluar K-means con `k = 4, 5, 6`, considerando silueta, inercia, tamaños e interpretabilidad. Las variables de edad, sexo, entidad y tipo de sección se usaron **después** para caracterizar los conglomerados; no para asignarlos.
5. Evaluar robustez excluyendo de manera temporal las unidades con al menos un año con `SV + NV < 100`, y comparar las asignaciones con el índice ARI.
6. Caracterizar los cuatro perfiles y proponer estrategias institucionales de información electoral diferenciadas y no partidistas.

## Archivos clave

| Ruta | Contenido |
|---|---|
| `datos/procesados/conteos_censales_AAAA_agrupado.csv` | Conteos agregados de cada elección, desde 2009 hasta 2024. |
| `datos/procesados/base_historica_comparable_2009_2024.csv` | Las 2,496 unidades comparables, con seis tasas históricas. |
| `datos/procesados/matriz_clustering_estandarizada.csv` | Matriz de entrada para K-means. |
| `perfiles/asignaciones_clustering_k4_k6.csv` | Comparación de asignaciones para distintos valores de `k`. |
| `perfiles/asignaciones_perfiles_k4.csv` | Clasificación final de las unidades. |
| `perfiles/centroides_k4.csv` y `perfiles/comparacion_kmeans_k4_k6.csv` | Centroides y criterios para seleccionar la solución final. |
| `perfiles/composicion_*_perfiles_k4.csv` | Composición de perfiles por variables de caracterización. |
| `perfiles/resumen_trayectorias_perfiles_k4.csv` | Tasas promedio de cada perfil por elección. |

## Reproducción y requisitos

**El ZIP incluye los datos procesados y los resultados del modelo, pero no los ZIP originales del INE.** Estos se consultan y descargan desde la [fuente oficial](https://www.ine.mx/transparencia/datos-abiertos/visualizacion-datos/conteos-censales-participacion/). Para revisar los resultados y regenerar las figuras finales no es necesario descargarlos.

### Opción A: regenerar las gráficas con los archivos incluidos

1. Extrae este ZIP y abre una terminal en la carpeta `Bugs_Bunny_Reto1_Perfiles_Ciudadanos` (donde está este README).
2. Instala las bibliotecas utilizadas para las gráficas:

   ```bash
   python -m pip install pandas numpy matplotlib
   ```

3. Ejecuta desde esa misma carpeta:

   ```bash
   python src/graficas_finales.py
   ```

El script lee los CSV de `datos/procesados/` y `perfiles/`, y guarda las nueve gráficas en `graficas/graficos finales/`.

### Opción B: revisar y volver a ejecutar los notebooks

Los notebooks están preparados principalmente para **Google Colab** y varios contienen rutas absolutas como `/content/`. Para ejecutarlos en Jupyter local es necesario cambiar esas rutas; no basta con abrir los `.ipynb` desde la carpeta del repositorio.

Dependencias utilizadas a lo largo del proceso: `pandas`, `numpy`, `scikit-learn`, `matplotlib` y `requests`; en Colab se usan además funciones de carga de archivos propias del entorno. Las bibliotecas se pueden instalar con:

```bash
python -m pip install pandas numpy scikit-learn matplotlib requests
```

| Notebook | Función | Archivo o insumo que espera en `/content/` |
|---|---|---|
| `01_exploracion_2024` a `06_exploracion_2009` | Limpieza y agregación de las bases originales. | ZIP correspondiente al año de elección; estos archivos no se incluyen en la entrega. |
| `07_integracion_historica` | Construcción de la serie histórica. | Los seis `conteos_censales_AAAA_agrupado.csv`, incluidos en `datos/procesados/`. |
| `08_analisis_exploratorio_historico` | Análisis exploratorio y matriz estandarizada. | `base_historica_comparable_2009_2024.csv`, incluida en `datos/procesados/`. |
| `09_clustering_perfiles` | Comparación de `k = 4, 5, 6`. | `base_historica_comparable_2009_2024.csv`, incluida en `datos/procesados/`. |
| `10_caracterizacion_perfiles_k4` | Caracterización y perfiles. | `asignaciones_clustering_k4_k6.csv`, incluido en `perfiles/`. |

En Colab, carga los archivos requeridos en `/content/` antes de ejecutar cada notebook, o modifica las variables de ruta al principio del código. Los productos intermedios se generan en `/content/` y pueden guardarse después en las carpetas equivalentes del proyecto. No se proporciona aquí un comando único que ejecute automáticamente los diez notebooks.

## Entregables y gráficas

![Trayectorias de los perfiles](graficas/graficos%20finales/01_trayectorias_perfiles.png)

![Selección de k](graficas/graficos%20finales/02_seleccion_k.png)

![Tamaño de los perfiles](graficas/graficos%20finales/03_tamano_perfiles.png)

- [Gráficas finales](graficas/graficos%20finales/)
- [Documento técnico (PDF)](documento_tecnico/Hackathon_INE_Documento.pdf)
- [Código LaTeX del documento](documento_tecnico/Hackathon_INE_Documento.tex) (para compilar con XeLaTeX y fuente Arial)
- [Presentación ejecutiva (PDF)](presentacion/Hackathon%20INE%20presentaci%C3%B3n.pdf)
- [Cuatro fichas visuales](fichas_visuales/README.md)

## Limitaciones

- Se utilizan **datos agregados**: las clases se asignan a unidades comparables y no a personas individuales.
- La silueta de aproximadamente `0.29` indica separación moderada; los perfiles son una descripción de patrones históricos, no una clasificación definitiva de individuos.
- Las 50 unidades de sexo no binario de 2024 no cuentan con historia comparable en las cinco elecciones anteriores y quedaron fuera del clustering histórico.
- Las asociaciones observadas con edad, sexo y tipo de sección no constituyen relaciones causales.
- La ejecución integral desde los archivos originales requiere obtener los ZIP oficiales y preparar las rutas de los notebooks.

## Referencias

1. Instituto Nacional Electoral. *Conteos Censales de Participación Ciudadana 2009–2024: Manual de uso de la plataforma para el análisis y la consulta*. INE, 2025.
2. Instituto Nacional Electoral. *Hackathon 2026: Hackea la participación, Datos que construyen democracia*. INE, 2026.
