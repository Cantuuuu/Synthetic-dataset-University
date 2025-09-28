import pandas as pd
import numpy as np


def generarDatosEstudiantes(numRegistros=500):

    # Semilla para reproducir nuevamente
    np.random.seed(42)

    # 1. Variables base
    generos = np.random.choice(['Femenino', 'Masculino', 'Otro'], numRegistros, p=[0.51, 0.47, 0.02]) #Recibe los porcentajes de cada genero
    lugarOrigen = np.random.choice(['Ciudad', 'Rural'], numRegistros, p=[0.75, 0.25]) #Recibe los porcentajes de cada origen
    edades = np.random.randint(17, 23, size=numRegistros) #Genera edades entre 17 y 22 años
    nivelesSocioEconomicos = np.random.choice(['Bajo', 'Medio', 'Alto'],numRegistros, p=[0.40, 0.45, 0.15]) #Recibe los porcentajes de cada nivel socioeconomico

    promedioBachillerato = np.random.normal(8.5, 0.8, numRegistros).clip(6.0, 10.0) #Para simular el promedio de bachillerato se usar una distribución normal con media 8.5 y desviación estándar 0.8, limitando los valores entre 6.0 y 10.0
    # Simulación semejante a EXCOBA en México (Examen de Competencias Básicas)
    # La media suele estar cerca de 65-70 puntos
    # Un puntaje por encima de 80 se considera bueno
    examenAdmision = np.random.normal(70, 10, numRegistros).clip(30, 100).round(1) #Puntaje del examen de admisión, con media 70 y desviación estándar 10, limitando entre 30 y 100

    # 2. Variables derivadas

    # La beca depende del nivel socioeconómico
    probaBeca = np.where(nivelesSocioEconomicos == 'Bajo', 0.6, np.where(nivelesSocioEconomicos == 'Medio', 0.25, 0.05)) #Si es nivel socioeconómico bajo, 60% de probabilidad de beca; medio 25%; alto 5%
    tieneBeca = (np.random.rand(numRegistros) < probaBeca).astype(int) #Genera una variable binaria (0 o 1) indicando si el estudiante tiene beca o no

    # Las notas del primer semestre dependen de las notas de bachillerato y el examen de admisión
    promedioPrimerSemestreLimpio = (promedioBachillerato * 0.6) + (examenAdmision / 100 * 10 * 0.4) #Es una combinación ponderada del promedio de bachillerato (60%) y el puntaje del examen de admisión (40%), completamente arbitrario
    promedioPrimerSemestreFinal = (promedioPrimerSemestreLimpio + np.random.normal(0, 0.5, numRegistros)).clip(0.0, 10.0) #Se añade algo de ruido aleatorio para simular variabilidad, limitando entre 0.0 y 10.0

    # 3. Deserción, la variable objetivo
    # La probabilidad de desertar aumenta con: bajo promedio, nivel socioeconómico bajo, sin beca.
    puntajeRiesgo = -1 * (promedioPrimerSemestreFinal / 10) + (np.where(nivelesSocioEconomicos == 'Bajo', 0.8, np.where(nivelesSocioEconomicos == 'Medio', 0.3, -0.5))) - (tieneBeca * 0.8) + np.random.normal(0, 0.2, numRegistros)
    #Si el promedio de primer semestre es bajo, el puntaje de riesgo aumenta (mayor probabilidad de deserción)
    #Si el nivel socioeconómico es bajo, el puntaje de riesgo aumenta
    #Si el estudiante tiene beca, el puntaje de riesgo disminuye
    #Se añade algo de ruido aleatorio para simular variabilidad

    #Una manera muy sencilla de hacerlo sería  asignar un abandono o no aleatorio:
    #desercion = np.random.choice([0, 1], numRegistros, p=[0.7, 0.3]) #30% de probabilidad de deserción


    probaDesercion = 1 / (1 + np.exp(-puntajeRiesgo)) # Función sigmoide para convertir el puntaje de riesgo en una probabilidad entre 0 y 1, valores más altos indican mayor probabilidad de deserción.
    desercion = (np.random.rand(numRegistros) < probaDesercion).astype(int) # Variable binaria (0 o 1) indicando si el estudiante desertó (1) o no (0)

    # 4. Creación las columnas del DataFrame
    df = pd.DataFrame({
        'Edad': edades,
        'Genero': generos,
        'LugarOrigen': lugarOrigen,
        'PromedioBachillerato': promedioBachillerato.round(2),
        'PuntajeExamenAdmision': examenAdmision.astype(int),
        'NivelSocioeconomico': nivelesSocioEconomicos,
        'TieneBeca': tieneBeca,
        'PromedioPrimerSemestre': promedioPrimerSemestreFinal.round(2),
        'Desercion': desercion
    })

    # 5. Introducir valores atípicos (outliers) y nulos (nulls)
    # Valores atípicos en edades y puntajes de examen
    numerosDeOutliers = int(numRegistros * 0.05)  # Se puede ajustar el porcentaje de atípicos al que se desea llegar (5% en este caso).
    indicesOutlierns = np.random.choice(df.index, numerosDeOutliers, replace=False) #Arreglo de indices para usar como outliers

    # Estudiantes mayores
    df.loc[indicesOutlierns, 'Edad'] = np.random.randint(35, 50, size=numerosDeOutliers) #Edades entre 35 y 50 años al porcentaje de outliers
    # Puntajes atípicos (calificaciones muy bajas o altas en el examen)
    df.loc[indicesOutlierns, 'PuntajeExamenAdmision'] = np.random.randint(95, 100, size=numerosDeOutliers)

    # Nulls
    numeroNulos = int(numRegistros * 0.05)  # 5% de nulos

    # Nulos en el promedio del primer semestre
    indicesNulosPromedio = np.random.choice(df.index, numeroNulos, replace=False)
    df.loc[indicesNulosPromedio, 'PromedioPrimerSemestre'] = np.nan

    # Nulos en el nivel socioeconómico
    indicesNulosSocio = np.random.choice(df.index, numeroNulos, replace=False)
    df.loc[indicesNulosSocio, 'NivelSocioeconomico'] = np.nan

    return df


dfEstudiantes = generarDatosEstudiantes(500)
dfEstudiantes.to_csv('datosEscolaresInstituto.csv', index=False)

print("Conunto de datos generado:")
print(dfEstudiantes.head())
print("\nValores nulos:")
print(dfEstudiantes.isnull().sum())
print("\nCantidad de abandonos:")
print(dfEstudiantes['Desercion'].value_counts())
