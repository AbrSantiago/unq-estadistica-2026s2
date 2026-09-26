# Trabajo Práctico

## Regresión, análisis multivariante y métodos de remuestreo aplicados a datos de dinámica molecular

### Análisis estadístico de la dinámica de un túnel del canal TMEM63A

---

## 1. Introducción

En bioinformática y biología estructural es frecuente trabajar con datos generados a partir de simulaciones de dinámica molecular (Molecular Dynamics, MD).

En una simulación de MD, una estructura molecular se registra a intervalos regulares de tiempo, generando una secuencia de configuraciones denominadas **frames**. Cada frame puede ser analizado para obtener diferentes características estructurales y fisicoquímicas.

En este trabajo se analizará una trayectoria correspondiente al canal de membrana **TMEM63A**. Para cada frame se identificó y caracterizó un túnel dentro de la estructura del canal.

El archivo `results.csv` contiene **1055 frames** y diferentes variables que describen las propiedades geométricas y fisicoquímicas del túnel.

El objetivo no será simplemente describir los datos, sino utilizar diferentes herramientas estadísticas para responder una pregunta general:

> **¿Cómo podemos caracterizar estadísticamente la variabilidad estructural y fisicoquímica de un túnel de TMEM63A a lo largo de una dinámica molecular?**

A lo largo del trabajo se utilizarán:

* análisis exploratorio de datos;
* correlación;
* regresión lineal;
* regresión múltiple;
* diagnóstico de modelos;
* análisis de componentes principales (PCA);
* clustering;
* bootstrap;
* pruebas de permutación;
* validación y cross-validation.

Además, se discutirá una característica fundamental de este conjunto de datos: **los frames pertenecen a una misma trayectoria temporal y, por lo tanto, no necesariamente son observaciones independientes**.

---

# 2. Objetivos

## Objetivo general

Aplicar herramientas de estadística para estudiar la relación entre las características geométricas y fisicoquímicas de un túnel de TMEM63A a lo largo de una trayectoria de dinámica molecular.

## Objetivos específicos

Al finalizar el trabajo deberán ser capaces de:

1. Explorar y caracterizar un conjunto de datos bioinformáticos.
2. Identificar variables relevantes y redundantes.
3. Analizar asociaciones entre variables mediante correlación.
4. Construir e interpretar modelos de regresión lineal.
5. Evaluar los supuestos de un modelo estadístico.
6. Detectar posibles problemas de multicolinealidad.
7. Utilizar PCA para resumir información multivariada.
8. Aplicar métodos de clustering para explorar posibles estados del sistema.
9. Utilizar bootstrap para estimar la incertidumbre de parámetros.
10. Comprender las limitaciones del bootstrap convencional cuando existe dependencia temporal.
11. Analizar la importancia de la validación y del data leakage.
12. Diferenciar asociación estadística de causalidad biológica.

---

# 3. Descripción del conjunto de datos

El archivo contiene una fila por frame de la trayectoria.

Hay **1055 observaciones y 20 variables**.

Las variables principales son:

| Variable                 | Descripción                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `frame`                  | Identificador temporal del frame                                 |
| `recipe_id`              | Identificador de la configuración/análisis                       |
| `length`                 | Longitud del túnel                                               |
| `dz`                     | Extensión del túnel en el eje z                                  |
| `tortuosity`             | Tortuosidad del túnel                                            |
| `bottleneck_radius`      | Radio del cuello de botella                                      |
| `bottleneck_free_radius` | Radio libre en el cuello de botella                              |
| `bottleneck_bradius`     | Medida alternativa del radio del cuello de botella               |
| `n_layers`               | Número de capas/residuos involucrados en la definición del túnel |
| `charge`                 | Carga neta asociada al túnel                                     |
| `ionizable`              | Número de residuos ionizables                                    |
| `num_positives`          | Número de residuos con carga positiva                            |
| `num_negatives`          | Número de residuos con carga negativa                            |
| `hydrophobicity`         | Medida de hidrofobicidad                                         |
| `hydropathy`             | Medida de hidropatía                                             |
| `polarity`               | Medida de polaridad                                              |
| `logp`                   | Coeficiente relacionado con partición/lipofilia                  |
| `logd`                   | Coeficiente de distribución                                      |
| `logs`                   | Medida relacionada con solubilidad                               |
| `mutability`             | Medida de mutabilidad de los residuos                            |


---

# 4. Pregunta central

Durante el trabajo deberán intentar responder:

> **¿Qué características estructurales y fisicoquímicas están asociadas con la variabilidad del túnel de TMEM63A y podemos identificar diferentes estados del túnel a lo largo de la trayectoria?**


---

# PARTE I — ANÁLISIS EXPLORATORIO

## Actividad 1. Conociendo los datos

1. Cargar el archivo `results.csv`.
2. Indicar:

   * número de observaciones;
   * número de variables;
   * tipo de cada variable;
   * cantidad de datos faltantes por variable.
3. Identificar:

   * variables constantes;
   * posibles variables redundantes;
   * variables que representan tiempo o identificación.
4. Calcular para las variables cuantitativas:

   * media;
   * mediana;
   * desviación estándar;
   * mínimo;
   * máximo;
   * rango intercuartílico.

### Preguntas

**a.** ¿Todas las variables deberían analizarse de la misma manera?

**b.** ¿Qué variables excluirían de un análisis estadístico multivariante y por qué?

**c.** ¿La media resulta siempre una buena medida descriptiva para estas variables?

Justificar.

---

## Actividad 2. Distribuciones

Seleccionar al menos seis variables relevantes.

Para cada una:

1. realizar un histograma;
2. agregar una medida de tendencia central;
3. describir la distribución;
4. identificar posibles valores extremos.

Además, realizar al menos dos boxplots.

### Preguntas

1. ¿Qué variables presentan mayor variabilidad?
2. ¿Existen distribuciones claramente asimétricas?
3. ¿Los valores extremos deben eliminarse automáticamente?

Justificar estadísticamente.

---

# PARTE II — DINÁMICA TEMPORAL

## Actividad 3. El tiempo importa

Graficar en función de `frame`:

* `length`;
* `tortuosity`;
* `bottleneck_radius`;
* una variable fisicoquímica a elección.

### Preguntas

1. ¿Se observan tendencias temporales?
2. ¿Se observan períodos de estabilidad?
3. ¿Existen fluctuaciones?
4. ¿Se observan cambios abruptos?
5. ¿Las observaciones consecutivas parecen independientes?

Esta última pregunta será retomada al final del trabajo.

---

# PARTE III — CORRELACIÓN

## Actividad 4. Matriz de correlación

Construir una matriz de correlación para las variables cuantitativas seleccionadas.

Utilizar inicialmente la correlación de Pearson.

Representar la matriz mediante un heatmap.

Analizar especialmente las relaciones con: `bottleneck_radius`

### Preguntas

Seleccionar **tres asociaciones** que consideren interesantes.

Para cada una:

1. informar el coeficiente de correlación;
2. informar el intervalo de confianza;
3. realizar el contraste de hipótesis correspondiente;
4. representar gráficamente la relación;
5. interpretar la magnitud del efecto;
6. discutir su posible significado biológico.

### Atención

No basta con indicar:

> “La correlación es significativa.”

Deberán indicar también **qué tan fuerte es la asociación**.

Por ejemplo:

> Una asociación puede presentar un p-value pequeño pero representar una relación débil.

---

# PARTE IV — REGRESIÓN LINEAL

## Actividad 5. Regresión lineal simple

Utilizar:

```text
bottleneck_radius
```

como variable respuesta.

Construir un modelo de regresión lineal simple utilizando como predictor una variable que, según el análisis anterior, pueda estar relacionada con el radio del cuello de botella.

Una opción posible es:

```text
bottleneck_radius ~ tortuosity
```

pero deberán justificar su elección.

### Informar

* ecuación del modelo;
* intercepto;
* pendiente;
* error estándar;
* intervalo de confianza;
* p-value;
* R²;
* interpretación de la pendiente.

Realizar un gráfico con:

* observaciones;
* recta de regresión;
* intervalo de confianza.

### Pregunta

¿Qué significa biológicamente una pendiente negativa o positiva?

¿Podemos afirmar que el predictor **causa** cambios en el radio?

Justificar.

---

# PARTE V — REGRESIÓN MÚLTIPLE

## Actividad 6. Construcción del modelo

Construir un modelo de regresión múltiple para explicar:

```text
bottleneck_radius
```

Utilizar varios predictores.

Como punto de partida puede utilizarse:

```text
bottleneck_radius ~ tortuosity +
                    length +
                    polarity +
                    hydrophobicity +
                    charge
```

También podrán proponer otro modelo, pero deberán justificar la selección de las variables.

### Analizar

1. coeficientes;
2. errores estándar;
3. intervalos de confianza;
4. p-values;
5. R²;
6. R² ajustado.

### Preguntas

**a.** ¿Qué predictor parece tener mayor asociación con la respuesta?

**b.** ¿Todos los predictores significativos en modelos simples permanecen significativos en el modelo múltiple?

**c.** ¿Por qué podría cambiar el coeficiente de una variable al agregar otros predictores?

---

# PARTE VI — MULTICOLINEALIDAD

## Actividad 7. ¿Estamos midiendo lo mismo varias veces?

Calcular una matriz de correlación entre los predictores.

Calcular posteriormente el **Variance Inflation Factor (VIF)**.

### Preguntas

1. ¿Existen predictores fuertemente correlacionados?
2. ¿Hay evidencia de multicolinealidad?
3. ¿Qué consecuencias puede tener para la interpretación de los coeficientes?
4. ¿Eliminarían alguna variable?

Justificar.

### Reflexión

Si dos variables representan aspectos muy similares de la geometría del túnel:

> ¿Tiene sentido incluir ambas como predictores independientes?

---

# PARTE VII — DIAGNÓSTICO DEL MODELO

## Actividad 8. ¿Podemos confiar en nuestra regresión?

Analizar los residuos del modelo múltiple.

Realizar al menos:

1. residuos vs valores ajustados;
2. Q-Q plot;
3. distribución de residuos;
4. leverage;
5. Cook's distance.

### Evaluar

* linealidad;
* normalidad de residuos;
* homocedasticidad;
* observaciones influyentes.

### Preguntas

**a.** ¿Se cumplen razonablemente los supuestos del modelo?

**b.** ¿Existen observaciones potencialmente influyentes?

**c.** ¿Eliminarían alguna observación? ¿Por qué?

---

# PARTE VIII — PCA

## Actividad 9. Reduciendo la dimensionalidad

Realizar un **Principal Component Analysis (PCA)** utilizando las variables cuantitativas apropiadas.

No incluir:

* `frame`;
* `recipe_id`;
* variables constantes.

Deberán justificar si utilizan o no estandarización.

### Realizar

1. scree plot;
2. porcentaje de varianza explicado;
3. varianza acumulada;
4. gráfico PC1 vs PC2;
5. análisis de loadings.

### Preguntas

**a.** ¿Cuántos componentes conservarían?

**b.** ¿Qué variables contribuyen principalmente a PC1?

**c.** ¿Qué variables contribuyen principalmente a PC2?

**d.** ¿Puede interpretarse alguno de estos componentes como una dimensión principalmente geométrica?

**e.** ¿Puede interpretarse alguno como una dimensión fisicoquímica?

Justificar utilizando los loadings.

---

# PARTE IX — CLUSTERING

## Actividad 10. ¿Existen diferentes estados del túnel?

Utilizar las variables seleccionadas para realizar clustering.

Aplicar al menos uno de los siguientes métodos:

* k-means;
* clustering jerárquico.

Si es posible, comparar ambos.

### Determinación del número de clusters

No elegir arbitrariamente el número de grupos.

Utilizar alguna estrategia estadística, por ejemplo:

* silhouette;
* elbow method;
* dendrograma.

### Preguntas

1. ¿Cuántos clusters parecen razonables?
2. ¿Los clusters están claramente separados?
3. ¿Qué características diferencian los grupos?
4. ¿Los clusters pueden interpretarse como diferentes estados estructurales?

### Importante

**No es obligatorio encontrar estados discretos.**

Si los datos sugieren una variación continua, esa también es una conclusión válida.

---

# PARTE X — CLUSTERS A LO LARGO DEL TIEMPO

## Actividad 11. Clustering + dinámica molecular

Una vez definidos los clusters, representar:

```text
cluster
  │
  │ ████
  │     █████
  │           ███
  │
  └──────────────── frame
```

### Preguntas

1. ¿Los clusters aparecen de manera persistente?
2. ¿Se producen transiciones entre estados?
3. ¿Hay períodos en los que el sistema permanece en un mismo cluster?
4. ¿Los cambios de cluster coinciden con cambios en `bottleneck_radius`?
5. ¿La clasificación obtenida por clustering parece representar estados estructurales reales o simplemente fluctuaciones?

---

# PARTE XI — BOOTSTRAP

## Actividad 12. Bootstrap de una correlación

Seleccionar una asociación de interés, por ejemplo:

```text
bottleneck_radius
```

vs.

```text
tortuosity
```

Calcular la correlación observada.

Luego realizar un **bootstrap con al menos 2000 réplicas**.

Para cada réplica:

1. remuestrear las observaciones;
2. calcular la correlación;
3. almacenar el resultado.

Representar la distribución bootstrap.

Calcular un intervalo de confianza del 95 %.

### Comparar

* intervalo de confianza paramétrico;
* intervalo bootstrap.

### Preguntas

1. ¿Los resultados son similares?
2. ¿La distribución bootstrap es aproximadamente simétrica?
3. ¿Qué información proporciona la distribución bootstrap?

---

# PARTE XII — BOOTSTRAP DE REGRESIÓN

## Actividad 13. Estabilidad de la pendiente

Realizar bootstrap de la pendiente del modelo:

```text
bottleneck_radius ~ tortuosity
```

Obtener una distribución de pendientes.

Calcular un intervalo de confianza del 95 %.

### Preguntas

1. ¿La pendiente es estable?
2. ¿El intervalo contiene el valor cero?
3. ¿El resultado coincide con la inferencia paramétrica?
4. ¿Qué interpretación biológica darían?

---

# PARTE XIII — EL PROBLEMA DEL BOOTSTRAP

## Actividad 14. ¿Podemos remuestrear frames libremente?

Hasta este momento hemos tratado los frames como observaciones.

Pero recordemos que:

> Los frames consecutivos pertenecen a una misma trayectoria temporal.

Por lo tanto, pueden estar correlacionados.

### Preguntas

**a.** ¿Qué supuesto del bootstrap convencional puede verse comprometido?

**b.** ¿Qué ocurre si los frames 100, 101, 102 y 103 contienen información muy similar?

**c.** ¿Estamos obteniendo realmente 1055 unidades independientes de información?

**d.** ¿Qué problema puede producir esto en los intervalos de confianza y p-values?

Investigar conceptualmente el **block bootstrap**.

No es necesario implementarlo si no se dispone de tiempo, pero deberán explicar:

> ¿Por qué podría ser más apropiado para este tipo de datos?

---

# PARTE XIV — PRUEBA DE PERMUTACIÓN

## Actividad 15. ¿Los estados presentan diferentes propiedades?

Seleccionar dos grupos o clusters obtenidos previamente.

Comparar el:

```text
bottleneck_radius
```

entre ambos grupos.

Utilizar una prueba de permutación.

Por ejemplo:

> diferencia de medias entre grupos.

### Procedimiento conceptual

1. Calcular la diferencia observada.
2. Permutar las etiquetas de los grupos.
3. Recalcular la diferencia.
4. Repetir muchas veces.
5. Construir la distribución nula.
6. Comparar el valor observado con la distribución.

### Preguntas

1. ¿Existe evidencia de diferencia entre los grupos?
2. ¿Qué supuesto permite realizar la permutación?
3. ¿La dependencia temporal vuelve problemática esta prueba?

---

# PARTE XV — VALIDACIÓN Y DATA LEAKAGE

## Actividad 16. Un modelo demasiado optimista

Considerar el siguiente procedimiento:

```text
Todos los datos
      ↓
Buscar variables con mayor correlación
      ↓
Seleccionar las mejores variables
      ↓
Construir modelo
      ↓
5-fold cross-validation
      ↓
Calcular RMSE
```

### Pregunta

¿Este procedimiento proporciona una estimación válida del rendimiento predictivo?

Justificar.

---

## Actividad 17. Diseñar un pipeline correcto

Proponer un esquema de validación en el que:

1. los datos sean divididos;
2. la selección de variables se realice únicamente con los datos de entrenamiento;
3. el modelo sea ajustado con entrenamiento;
4. el modelo sea evaluado sobre datos no utilizados durante el entrenamiento.

Representar gráficamente el pipeline.

Explicar qué es **data leakage** y por qué puede producir una estimación artificialmente optimista del rendimiento.

---

# PARTE XVI — INTEGRACIÓN

## Actividad 18. La investigación estadística

Integrar los resultados de al menos **tres métodos diferentes**.

Responder:

> **¿Qué características parecen estar asociadas con la variabilidad del túnel de TMEM63A a lo largo de la trayectoria?**

La respuesta deberá integrar, como mínimo:

* un resultado de asociación/regresión;
* un resultado multivariante;
* un resultado de remuestreo o análisis temporal.

No se espera simplemente una lista de resultados.

Deberán construir una interpretación coherente.

---

# PARTE XVII — ¿QUÉ NO PODEMOS CONCLUIR?

## Actividad 19. Estadística ≠ causalidad

Escribir:

### Tres conclusiones que los datos permiten sostener.

y

### Tres conclusiones que NO pueden sostenerse a partir del análisis.

Por ejemplo, una asociación estadística entre tortuosidad y radio del cuello de botella **no permite afirmar automáticamente que la tortuosidad cause cambios en el radio**.

Para cada conclusión deberán explicar por qué.

---

# 5. Informe final

El informe deberá tener la siguiente estructura:

## 1. Introducción

Presentar brevemente:

* problema biológico;
* características de los datos;
* pregunta estadística.

## 2. Materiales y métodos

Describir:

* dataset;
* variables utilizadas;
* métodos estadísticos;
* criterios utilizados para seleccionar variables;
* métodos de remuestreo;
* métodos de validación.

No es necesario copiar código completo en esta sección.

## 3. Resultados

Presentar los principales resultados de:

* exploración;
* correlación;
* regresión;
* diagnóstico;
* PCA;
* clustering;
* bootstrap;
* permutación;
* análisis temporal.

## 4. Discusión

Interpretar los resultados.

Discutir:

* magnitud de los efectos;
* incertidumbre;
* supuestos;
* dependencia temporal;
* posibles limitaciones;
* significado biológico.

## 5. Conclusiones

Responder brevemente a la pregunta central.

## 6. Código

Incluir el código utilizado para reproducir los análisis.

---

# 6. Requisitos mínimos de figuras

El informe deberá contener como mínimo:

1. **2 gráficos exploratorios**.
2. **1 gráfico temporal**.
3. **1 matriz de correlación**.
4. **2 gráficos de regresión**.
5. **2 gráficos de diagnóstico**.
6. **1 scree plot**.
7. **1 gráfico PCA**.
8. **1 visualización de clustering**.
9. **1 gráfico de clusters vs frame**.
10. **1 distribución bootstrap**.
11. **1 distribución de permutación**.

Las figuras deberán tener:

* título;
* ejes correctamente identificados;
* unidades cuando correspondan;
* leyenda cuando sea necesaria;
* una breve explicación en el texto.

---

# 7. Requisitos estadísticos mínimos

El informe deberá incluir obligatoriamente:

* estadísticos descriptivos;
* al menos tres correlaciones;
* una regresión lineal simple;
* una regresión múltiple;
* análisis de VIF;
* diagnóstico de residuos;
* PCA;
* clustering;
* bootstrap;
* una prueba de permutación;
* discusión de dependencia temporal;
* discusión de data leakage/cross-validation.

---

# 8. Preguntas conceptuales finales

Responder brevemente:

### 1. ¿Cuál es la diferencia entre asociación y causalidad?

### 2. ¿Por qué un p-value pequeño no implica necesariamente un efecto biológicamente importante?

### 3. ¿Por qué dos variables altamente correlacionadas pueden generar problemas en una regresión múltiple?

### 4. ¿Qué información aporta PCA que no aporta una matriz de correlación?

### 5. ¿Encontrar tres clusters implica necesariamente que existen tres estados biológicos reales?

### 6. ¿Por qué el bootstrap convencional puede ser problemático para una trayectoria de MD?

### 7. ¿Qué es data leakage?

### 8. ¿Por qué la validación debe realizarse sobre datos que no participaron en el entrenamiento?

### 9. ¿Los 1055 frames deben considerarse necesariamente como 1055 observaciones independientes?

### 10. Si tuvieran que repetir este análisis para otra proteína, ¿qué aspectos del pipeline estadístico mantendrían y cuáles modificarían?

---

# 9. Producto final

El objetivo del trabajo no es obtener un determinado resultado estadístico.

Se evaluará la capacidad para:

> **formular una pregunta, seleccionar métodos apropiados, evaluar sus supuestos, cuantificar la incertidumbre e interpretar los resultados dentro de un contexto bioinformático.**

Una respuesta estadísticamente correcta pero biológicamente injustificada no será considerada una interpretación completa.

Del mismo modo, una conclusión negativa o inconclusa puede ser completamente válida si está correctamente sustentada por los análisis.

---

## Criterio transversal de evaluación

Durante todo el trabajo se valorará especialmente la capacidad de responder:

> **¿Este método estadístico es apropiado para estos datos y qué supuestos estoy haciendo al utilizarlo?**

No se evaluará únicamente la obtención de números o gráficos.

Se evaluará la capacidad de **razonar estadísticamente** a partir de ellos.