# Hackathon_INE: perfiles ciudadanos de participación electoral (2009–2024)

**Hackathon INE 2026 – "Hackea la participación: Datos que construyen democracia"**
Reto 1: Perfiles ciudadanos de participación · Equipo **Bugs Bunny**

## Resumen

Este proyecto identifica **cuatro perfiles ciudadanos de participación electoral** a partir de los Conteos Censales de Participación Ciudadana (CCPC) del INE para 2009, 2012, 2015, 2018, 2021 y 2024. Se homologaron las seis bases en una unidad común (entidad + grupo de edad + sexo + tipo de sección), se obtuvieron 2,496 unidades comparables y se aplicó K-means sobre sus seis tasas históricas estandarizadas.

| Perfil | Unidades | % | Participación promedio |
|---|---|---|---|
| Históricamente alta | 623 | 24.96 | 71.67 % |
| Históricamente media-alta | 835 | 33.45 | 61.26 % |
| Históricamente media-baja | 676 | 27.08 | 50.32 % |
| Históricamente baja | 362 | 14.50 | 38.59 % |

La solución con k = 4 obtuvo la mayor silueta (0.2895) y fue estable al excluir grupos pequeños (índice de Rand ajustado = 0.9157).

## Integrantes

- Aguilar Lara Ericka
- Bautista Reyes Sofía
- Cruz Basilio Ximena Carolina
- Jardón Marín Rodrigo

## Estructura del repositorio

```
Hackathon_INE/
├── datos/
│   ├── originales/       # Bases originales de los CCPC
│   ├── procesados/       # Bases agrupadas, base histórica e insumos de segmentación
│   └── compatibilidad/   # Tablas de compatibilidad de variables por año
├── notebooks/            # Análisis completo (01 a 10)
├── perfiles/             # Resultados del clustering y caracterización (k = 4)
├── graficas/             # Gráficas finales (PNG y PDF)
├── documentos/           # Documento técnico
├── presentacion/         # Presentación ejecutiva
├── src/                  # Scripts auxiliares (incluye graficas_finales.py)
└── README.md
```

### Notebooks

| Notebook | Contenido |
|---|---|
| `01` – `06_exploracion_AAAA` | Exploración, validación y agrupación de cada elección (2024, 2021, 2018, 2015, 2012, 2009) |
| `07_integracion_historica` | Integración de las seis elecciones y construcción de la base comparable |
| `08_analisis_exploratorio_historico` | Promedios, correlaciones y diferencias por edad, sexo y tipo de sección |
| `09_clustering_perfiles` | Evaluación de K-means con k = 4, 5 y 6 |
| `10_caracterizacion_perfiles_k4` | Caracterización de los cuatro perfiles |

### Archivos principales

- `datos/procesados/conteos_censales_AAAA_agrupado.csv`: base agrupada de cada elección.
- `datos/procesados/base_historica_comparable_2009_2024.csv`: 2,496 unidades con información en las seis elecciones.
- `datos/procesados/matriz_clustering_estandarizada.csv`: matriz de entrada para K-means.
- `perfiles/asignaciones_perfiles_k4.csv`: perfil asignado a cada unidad.
- `perfiles/centroides_k4.csv`, `comparacion_kmeans_k4_k6.csv`: resultados de la segmentación.
- `perfiles/composicion_*_perfiles_k4.csv`, `resumen_trayectorias_perfiles_k4.csv`, `resumen_interpretacion_perfiles_k4.csv`: caracterización.

## Datos

- **Fuente:** [Conteos Censales de Participación Ciudadana (INE)](https://www.ine.mx/transparencia/datos-abiertos/visualizacion-datos/conteos-censales-participacion/)
- **Unidad de análisis:** entidad + grupo de edad (13 intervalos) + sexo + tipo de sección.
- **Participación** = SV / (SV + NV) × 100; los registros NS no entran en el denominador.
- Los datos son agregados y no contienen información personal identificable.
- Se homologó *Distrito Federal* como *Ciudad de México*. De las 2,546 unidades integradas, 2,496 tienen información en las seis elecciones y forman la base comparable.

## Metodología

1. **Validación** de cada elección (32 entidades, LN = SV + NV + NS).
2. **Integración histórica** de las seis bases.
3. **Análisis exploratorio** de las tasas históricas.
4. **Segmentación** con K-means (k = 4, 5, 6) sobre las seis tasas estandarizadas; selección por silueta, inercia, tamaño de conglomerados e interpretabilidad.
5. **Robustez:** exclusión de grupos pequeños (SV + NV < 100) y comparación con ARI.
6. **Caracterización** de los perfiles por edad, sexo, entidad y tipo de sección, y propuesta de estrategias institucionales diferenciadas.

## Cómo reproducir

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ChocoSBR/Hackathon_INE.git
   cd Hackathon_INE
   ```
2. Instala las dependencias: `pip install pandas numpy scikit-learn matplotlib`
3. Ejecuta los notebooks de `notebooks/` en Google Colab o Jupyter. Los notebooks `01` a `06` son independientes entre sí; después se ejecutan en orden `07` → `08` → `09` → `10`.
4. Para regenerar las gráficas finales, desde la raíz del repositorio:
   ```bash
   python src/graficas_finales.py
   ```

## Resultados

![Trayectorias de los perfiles](graficas/01_trayectorias_perfiles.png)

![Selección de k](graficas/02_seleccion_k.png)

![Tamaño de los perfiles](graficas/03_tamano_perfiles.png)

Las demás gráficas (composición por sexo, tipo de sección y edad; participación por elección y por grupo de edad; correlaciones) están en [`graficas/`](graficas/).

## Documentos

- Documento técnico: [`documentos/`](documentos/)
- Presentación ejecutiva: [`presentacion/`](presentacion/)

## Limitaciones

- Los datos son agregados: los perfiles describen unidades, no personas ni trayectorias individuales.
- La silueta (0.29) indica separación moderada; los perfiles son una síntesis útil de patrones históricos, no categorías absolutas.
- Las 50 unidades de sexo no binario de 2024 no tienen historia previa y quedan fuera del clustering.
- Las asociaciones con edad, sexo o tipo de sección no deben interpretarse como determinantes del comportamiento electoral.

## Referencias

- Instituto Nacional Electoral. *Conteos Censales de Participación Ciudadana 2009–2024: Manual de uso de la plataforma para el análisis y la consulta*. INE, 2025.
- Instituto Nacional Electoral. *Hackathon 2026: Hackea la participación, Datos que construyen democracia*. INE, 2026.
