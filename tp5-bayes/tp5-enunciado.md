# Trabajo Práctico Individual
# Probabilidades condicionales, teorema de Bayes, axiomas de Cox-Jaynes


## Objetivos

Al finalizar este trabajo práctico, deberías poder:

    Aplicar la regla del producto y el teorema de Bayes a un problema de inferencia evolutiva.

    Calcular probabilidades condicionales sobre un árbol filogenético simplificado.

    Interpretar el efecto del prior en la inferencia bayesiana.

    Relacionar la práctica con los axiomas de Cox-Jaynes sobre razonamiento coherente con información incompleta.

    Ejecutar un flujo básico de inferencia filogenética bayesiana con herramientas informáticas y responder una pregunta biológica concreta.

## Marco biológico

MICU1 y MICU2 son proteínas parálogas humanas que regulan el uniporter de calcio mitocondrial. Comparten aproximadamente 42% de similitud de secuencia y una arquitectura de dominios conservada (lóbulos N y C, cuatro motivos EF-hand), pero cumplen funciones distintas: MICU1 actúa como gatekeeper y MICU2 modula la sensibilidad al calcio. Experimentos de quimeras demostraron que el dominio N-terminal (residuos ~1–205 en MICU1, ~1–159 en MICU2) es el determinante principal de la diferencia funcional entre ambas proteínas.

En este TP vas a usar esa diferencia funcional como excusa para aplicar probabilidad condicional y teorema de Bayes. Primero harás los cálculos a mano sobre un árbol simplificado. Luego aplicarás el mismo razonamiento a un sitio real del alineamiento MICU1/MICU2. Finalmente, usarás herramientas informáticas para hacer una inferencia filogenética bayesiana sobre la proteína completa y responder una pregunta evolutiva.

## PARTE A: Cálculo a mano sobre un árbol simplificado
### Contexto

Tenés un alineamiento de cuatro secuencias hipotéticas. En un sitio determinado, los estados observados en las puntas de un árbol enraizado son:

    Especie A: I (Isoleucina)

    Especie B: V (Valina)

    Especie C: L (Leucina)

    Especie D: I (Isoleucina)

La topología del árbol es:
text

        raíz
       /    \
      X      Y
     / \    / \
    A   B  C   D

Los nodos internos son X (ancestro de A y B) e Y (ancestro de C y D). La raíz es el ancestro de X e Y.

### Modelo de sustitución simplificado

Usá un modelo tipo Jukes-Cantor con cuatro estados (I, V, L, F). La probabilidad de que un sitio cambie a lo largo de una rama es p=0.3

La probabilidad de que se mantenga igual es 1−p=0.7

Las frecuencias de equilibrio son:

    πI=0.4,πV=0.3,πL=0.2,πF=0

Las probabilidades de transición en una rama son:

    Si i=j: P(i→i)=0.7+0.3⋅πi​

    Si i≠j: P(i→j)=0.3⋅πj

Verificá que para cada estado i, la suma sobre todos los j da 1.

### Consigna A1: Probabilidad condicional directa

Calculá la probabilidad de observar los datos en las cuatro puntas dado que el estado en la raíz es I:

*P(datos∣raíz=I)*

Pasos sugeridos:

    Calculá la probabilidad de que X sea I, V, L o F, dado que la raíz es I.

    Para cada estado posible de X, calculá la probabilidad de observar A = I y B = V (dado ese estado de X).

    Hacé lo mismo para Y, C y D.

    Sumá sobre todos los estados posibles de X e Y (marginalización).

Como X e Y son independientes dado el estado de la raíz, podés calcular la contribución de la rama izquierda y la rama derecha por separado, y luego multiplicarlas y sumar sobre la raíz.

Mostrá las tablas intermedias.

### Consigna A2: Aplicar el teorema de Bayes

Asumí un prior uniforme sobre los cuatro estados de la raíz:

*P(raíz=I)=P(V)=P(L)=P(F)=0.25*

Calculá la probabilidad posterior de cada estado de la raíz dados los datos observados:

$$
P(raíz=r∣datos)= \frac{P(datos∣raíz=r)⋅P(raíz=r)​}{∑sP(datos∣raıˊz=s)⋅P(raíz=s)}
$$

Preguntas:

    ¿Cuál es el estado ancestral más probable en la raíz?

    ¿Coincide con lo que hubieras adivinado por parsimonia (el estado que requiere menos cambios)? Explicá.

### Consigna A3: Cambio de prior

Repetí el cálculo de A2 usando ahora un prior basado en las frecuencias de equilibrio:

$$
P(raíz=I)=0.4,P(V)=0.3,P(L)=0.2,P(F)=0.1
$$

Preguntas:

    ¿Cambió el estado más probable?

    ¿Qué te dice esto sobre el rol del prior cuando los datos son informativos (o poco informativos)?

    ¿Cómo se relaciona esto con la idea de Cox-Jaynes de que el prior no es un capricho sino una cuantificación de supuestos?

### Consigna A4: Conexión con Cox-Jaynes


a) En este ejercicio usamos la regla del producto y la marginalización. ¿Cuál de los dos desiderata de Cox estás usando implícitamente cuando sumás sobre los estados de X e Y?

b) Si te pidieran justificar por qué usás probabilidades para reconstruir un estado ancestral que nunca vas a observar directamente, ¿cómo responderías usando la idea de "lógica extendida" de Jaynes?

c) Un compañero dice: "El prior uniforme es objetivo porque no asume nada". ¿Qué le responderías desde la perspectiva de Cox-Jaynes?


## PARTE B: Caso real MICU1/MICU2
### Contexto

Ahora vas a aplicar el mismo razonamiento a un sitio real del alineamiento entre MICU1 y MICU2 humanas, con ortólogos de MICU2.

La tabla adjunta contiene tres sitios del dominio N-terminal donde MICU1 y MICU2 difieren, y donde hay datos de ortólogos disponibles. Los estados están codificados con el código de una letra de aminoácidos.

| Sitio | MICU1_Hs | MICU2_Hs | MICU2_Mm | MICU2_Dr |
| --- | --- | --- | --- | --- |
| 182 | R | K | K | Q |
| 220 | D | E | E | I |
| 245 | N | D | D | T |



Nota: Los ortólogos de MICU2 de ratón (Mus musculus, Q8CD10) y pez cebra (Danio rerio, Q1LCY6) están disponibles en UniProt.

Árbol simplificado


        Ancestro MICU2_Dr/MICUs
              /          \
         MICU2_Dr      Ancestro MICU1/2
                        /          \
                    MICU1_Hs      Ancestro MICU1/2
                                     /          \
                                MICU2_Mm      MICU2_Hs

### Consigna B1

Para cada uno de los tres sitios de la tabla:

    Calculá P(datos∣ancestro MICU=K) y P(datos∣ancestro MICU=R) (o los estados correspondientes a tu sitio), usando las mismas probabilidades de transición de la Parte A.

    Aplicá el teorema de Bayes con un prior uniforme sobre los estados posibles del ancestro de MICU2.

    Determiná el estado ancestral más probable.

¿El estado ancestral inferido favorece un cambio en el linaje MICU1, en el linaje MICU2, o es ambiguo? ¿Qué patrón emerge a partir de los tres sitios?

### Consigna B2

Ahora usá un prior basado en las frecuencias de aminoácidos del alineamiento completo 

¿Cambia alguna de las inferencias? ¿Qué supuestos estás haciendo sobre el proceso evolutivo al usar este prior?

## PARTE C: Análisis filogenético bayesiano con herramientas informáticas

### Objetivo

Hasta acá trabajaste sitio por sitio, a mano. Ahora vas a usar datos reales y herramientas de línea de comandos (o servidores web) para hacer una inferencia filogenética bayesiana sobre la proteína completa, y responder una pregunta biológica más amplia.

### Secuencias a utilizar

Descargá de UniProt las siguientes secuencias en formato FASTA:

| Proteína |	Organismo |	UniProt ID |
| --- | --- | --- |
| MICU1	| Homo sapiens| 	Q9BPX6 |
| MICU2	| Homo sapiens| 	Q8IYU8 |
| MICU2	| Mus musculus| 	Q8CD10 |
| MICU2	| Danio rerio| 	Q1LCY6 |


Cómo descargar de UniProt:

    Entrá a https://www.uniprot.org/

    Buscá el accession (por ejemplo, Q9BPX6).

    Hacé click en "Download" y elegí formato FASTA.


**Paso 1: Alineamiento con MAFFT**

Opción web (recomendada si no tenés experiencia con línea de comandos):

    Andá a https://mafft.cbrc.jp/alignment/server/

    Subí tu archivo FASTA con todas las secuencias.

    En "Advanced settings", seleccioná L-INS-i (preciso para menos de 200 secuencias).

    Hacé click en "Submit".

    Cuando termine, descargá el alineamiento en formato FASTA.

Opción local (si tenés MAFFT instalado):

```bash
mafft --auto input.fasta > output.aln
```


Entregable: captura de pantalla del alineamiento (o el archivo .aln).

**Paso 2: Selección del modelo de sustitución**

Opción simple: usá el modelo LG+G directamente. Es un modelo común para proteínas y es aceptable para un ejercicio didáctico.

Opción más rigurosa: usá ModelTest-NG si está disponible en tu institución o en un servidor web. El programa te dirá qué modelo usar.

**Paso 3: MrBayes vía CIPRES**

Si no podés instalar MrBayes localmente, usá el servidor web CIPRES:

    Andá a https://www.phylo.org/

    Creá una cuenta gratuita.

    Buscá la herramienta MrBayes en el portal.

    Importante: MrBayes requiere el alineamiento en formato NEXUS, no FASTA. Podés convertirlo con una herramienta online (buscá "FASTA to NEXUS converter") o con el mismo MrBayes si lo instalás local.

    Subí tu archivo NEXUS.

    En los parámetros de MrBayes, configurá:

        prset aamodelpr=fixed(lg) (para usar el modelo LG en proteínas)

        mcmc ngen=1000000 samplefreq=100 nchains=4 nruns=2

        sump y sumt para resumir los resultados

    Enviá el trabajo. Te llega un email cuando termine.

Advertencia importante: MrBayes por defecto asume ADN. Para proteínas, tenés que especificar **prset aamodelpr=...** con un modelo de aminoácidos. Si no lo hacés, el programa tratará los caracteres como nucleótidos y fallará o dará resultados sin sentido.

Si tenés MrBayes instalado localmente, el bloque de comandos dentro del archivo NEXUS debería verse similar a:

```
begin mrbayes;
  prset aamodelpr=fixed(lg);
  mcmc ngen=1000000 samplefreq=100 nchains=4 nruns=2;
  sump;
  sumt;
end;
```

**Paso 4: Visualización con FigTree**

    Descargá FigTree desde https://github.com/rambaut/figtree/releases (requiere Java).

    Abrí el archivo que termina en .con.tre (árbol de consenso).

    En el panel izquierdo, activá "Node Labels" y seleccioná "prob" para ver las probabilidades posteriores.

    Guardá la imagen como PDF.

### Consigna C1

A partir del árbol de consenso obtenido:

    ¿Las secuencias de MICU1 y las de MICU2 se agrupan cada una en su propio clado (monofilia)? ¿Con qué probabilidad posterior?

    ¿Este resultado es consistente con lo que inferiste a mano en la Parte B para el dominio N-terminal? Si no lo es, ¿cómo lo explicarías (por ejemplo: azar en un solo sitio, diferencias de tasa evolutiva entre el N-terminal y el resto de la proteína, o evolución asimétrica tras la duplicación génica)?

### Consigna C2

Respondé brevemente:

a) En la Parte A calculaste el posterior de forma exacta (sumando sobre todos los estados posibles). En la Parte C, MrBayes usa MCMC para aproximar el posterior. ¿Por qué no podés calcular el posterior de forma exacta para una proteína completa con 6–8 secuencias y cientos de sitios?

b) ¿Qué relación tiene el uso de MCMC con la idea de Cox-Jaynes de que la probabilidad es una herramienta para razonar con información incompleta?


## PARTE D

Escribí un texto breve (máximo 15 líneas) que responda:

    ¿Qué aporta el enfoque bayesiano a la reconstrucción de estados ancestrales y a la inferencia filogenética, en comparación con la máxima parsimonia? Mencioná al menos una ventaja y una limitación, y conectá tu respuesta con los axiomas de Cox-Jaynes.

# Entregables

| Parte |	Qué entregar |
| --- | --- |
| A |	Tablas de cálculos de A1 y A2, y respuestas a las preguntas de A3 y A4 |
| B |	Cálculos para los tres sitios, respuestas a las preguntas biológicas de B1 y B2 |
| C |	Captura del alineamiento de MAFFT, nombre del modelo usado, árbol de consenso con valores de probabilidad posterior, respuestas a C1 y C2 |
| D |	Reflexión final |

Formato: PDF único. Podés incluir imágenes (capturas de pantalla) y tablas.


# Rúbrica de evaluación

| Criterio |	Puntos |
| --- | --- |
| Corrección de los cálculos de la Parte A |	25 |
| Aplicación al caso real y interpretación biológica (Parte B) |	20 |
| Ejecución correcta del flujo MAFFT → MrBayes → FigTree (Parte C) |	25 |
| Calidad de la interpretación del árbol y respuesta a la pregunta biológica |	15 |
| Reflexión conceptual (Cox-Jaynes, comparación con parsimonia) |	15 |
| Total |	100 |


# Recursos de ayuda

    UniProt: https://www.uniprot.org/

    MAFFT web: https://mafft.cbrc.jp/alignment/server/

    CIPRES Science Gateway (MrBayes online): https://www.phylo.org/

    FigTree (visualización de árboles): https://github.com/rambaut/figtree/releases

    Conversor FASTA a NEXUS: buscá "FASTA to NEXUS converter" en tu navegador