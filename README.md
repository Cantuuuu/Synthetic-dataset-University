# Synthetic-dataset-University
Conjunto de datos que simula información de estudiantes universitarios con el objetivo de analizar factores que influyen en la deserción escolar.

##  Acerca de

Este conjunto de datos **sintético** simula información de estudiantes universitarios para analizar factores asociados a la **deserción escolar**. Está inspirado en el contexto educativo de México: calificaciones en escala **0–10** y un examen de admisión tipo **EXCOBA** (UAQ) representado como puntaje de **30–100**.

---
##  Diccionario de variables

| Variable                | Tipo       | Rango/Valores                                          | Descripción                                                        |
|-------------------------|------------|--------------------------------------------------------|--------------------------------------------------------------------|
| `Edad`                  | Entero     | 17–22 (outliers: 35–50)                                | Edad del estudiante en años.                                       |
| `Genero`                | Categórico | 'Femenino' (51%), 'Masculino' (47%), 'Otro' (2%)       | Género con el que se identifica el estudiante.                     |
| `LugarOrigen`           | Categórico | 'Ciudad' (75%), 'Rural' (25%)                          | Procedencia geográfica.                                            |
| `PromedioBachillerato`  | Decimal    | 6.0–10.0                                               | Promedio previo a la universidad (escala mexicana).                |
| `PuntajeExamenAdmision` | Entero     | 30–100 (media 70, σ≈10)                                | Simulación de EXCOBA.                                              |
| `NivelSocioeconomico`   | Categórico | 'Bajo' (40%), 'Medio' (45%), 'Alto' (15%)              | Nivel económico familiar.                                          |
| `TieneBeca`             | Binario    | 0 (No), 1 (Sí)                                         | Indica si cuenta con apoyo económico.                              |
| `PromedioPrimerSemestre`| Decimal    | 0.0–10.0                                               | Desempeño académico en el primer periodo universitario.            |
| `Desercion`             | Binario    | 0 (Continúa), 1 (Abandona)                             | **Variable objetivo**: abandono de estudios.                       |

---

##  Lógica de generación

### Variables derivadas

- **TieneBeca** (probabilidad condicionada por `NivelSocioeconomico`):
  - Bajo: 60%
  - Medio: 25%
  - Alto: 5%

- **PromedioPrimerSemestre** ≈  
  `0.6 × PromedioBachillerato + 0.4 × (PuntajeExamenAdmision/10)`  
  con **ruido aleatorio** para variabilidad realista y recorte a [0, 10].

- **Desercion** (riesgo base con efectos direccionales):
  - Menor `PromedioPrimerSemestre` → **mayor** riesgo.
  - Nivel socioeconómico **más bajo** → **mayor** riesgo.
  - `TieneBeca = 1` → **reduce** el riesgo.  
  Se añade aleatoriedad para capturar factores no observados.

### Outliers

Se introduce **5%** de valores atípicos:
- `Edad`: entre 35–50 para simular reingreso/educación continua.
- `PuntajeExamenAdmision`: picos altos 95–100 para estudiantes excepcionales.

### Valores nulos (NaN)

Se inyecta **5%** de nulos en:
- `PromedioPrimerSemestre`: estudiantes que abandonan antes de evaluar.
- `NivelSocioeconomico`: registros con información faltante.

---
