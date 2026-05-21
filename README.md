<div align="justify">
  
# Variabilidad de la frecuencia cardíaca y balance autonómico 
## Quinto laboratorio de procesamiento digital de señales

**Maria Camila Ospina Jara, Juan Felipe Serna Alarcón**
## Descripción
La práctica consistió en analizar la variabilidad de la frecuencia cardíaca (HRV) a partir de señales ECG en reposo y durante lectura en voz alta. Se aplicaron filtros digitales, se calcularon intervalos R-R y parámetros HRV, y se utilizaron diagramas de Poincaré para evaluar el balance autonómico.
## Introducción
La variabilidad de la frecuencia cardíaca (HRV) es una medida que permite evaluar las fluctuaciones en los intervalos de tiempo entre latidos consecutivos del corazón, conocidas como intervalos R-R. Estas variaciones reflejan la interacción entre las ramas simpática y parasimpática del sistema nervioso autónomo, encargadas de regular la actividad cardíaca según las condiciones fisiológicas y emocionales del organismo. Debido a esto, el análisis de la HRV se ha convertido en una herramienta importante para el estudio del balance autonómico y del comportamiento cardiovascular frente a diferentes estímulos.

La señal electrocardiográfica (ECG) constituye una de las principales fuentes para el análisis de la HRV, ya que permite identificar con precisión los complejos QRS y obtener los intervalos R-R necesarios para el procesamiento de la información. Sin embargo, las señales adquiridas suelen estar afectadas por ruido e interferencias, por lo que es necesario aplicar técnicas de procesamiento digital de señales, como el diseño e implementación de filtros digitales, para mejorar la calidad de la señal y garantizar resultados confiables.

En esta práctica de laboratorio se realizó la adquisición de una señal ECG bajo dos condiciones diferentes: reposo y lectura en voz alta, con el fin de observar posibles cambios en la actividad autonómica asociados a la verbalización. Posteriormente, se llevó a cabo el preprocesamiento de la señal, la detección de picos R y el cálculo de parámetros de HRV en el dominio del tiempo. Además, se construyeron diagramas de Poincaré para analizar gráficamente la dispersión de los intervalos R-R y calcular índices relacionados con la actividad simpática y vagal. De esta manera, la práctica permitió relacionar conceptos de fisiología cardiovascular y procesamiento digital de señales con aplicaciones en ingeniería biomédica.

## Desarrollo de la práctica
### Parte A: 
a. Fundamento teórico
a.1 El corazón no late de forma rítmica constante como un metrónomo; su cadencia está sujeta a una modulación continua por parte del Sistema Nervioso Autónomo (SNA). Este control se divide en dos ramas con funciones antagónicas que buscan mantener la homeostasis:
- Sistema Nervioso Simpático (SNS): Actúa como el acelerador del organismo ante situaciones de estrés, peligro o actividad física ("respuesta o huida"). A nivel celular, la liberación de noradrenalina estimula los receptores beta-1 adrenérgicos, lo que aumenta la permeabilidad a los iones sodio y calcio, acelerando la despolarización del nódulo sinusal y aumentando la frecuencia cardíaca (efecto cronotrópico positivo).
- Sistema Nervioso Parasimpático (SNP): Actúa como el freno, predominando en estados de reposo. A través del nervio vago (X par craneal), libera acetilcolina, la cual interactúa con los receptores muscarínicos M2. Esto provoca una disminución del AMP cíclico y una salida de potasio, generando una hiperpolarización que retrasa la generación del potencial de acción, disminuyendo así la frecuencia cardíaca (efecto cronotrópico negativo).

a.2 Variabilidad de la Frecuencia Cardíaca (HRV): 
La HRV se define como la fluctuación en los intervalos de tiempo entre latidos cardíacos consecutivos, conocidos como intervalos R-R. Una HRV elevada es un marcador de un sistema cardiovascular adaptable y resiliente, mientras que una HRV baja se asocia con fatiga, estrés crónico o patologías cardiovasculares. La medición de la HRV en milisegundos permite detectar cambios ínfimos en el balance autonómico que no son perceptibles a simple vista.

a.3 Análisis No Lineal: El Diagrama de Poincaré: 
Debido a que la regulación del corazón es un proceso complejo y no lineal, se utilizan herramientas como el Diagrama de Poincaré (o mapa de Lorenz). Este método grafica el intervalo (R-R)n actual frente al siguiente intervalo (R-R)n+1. En un individuo sano, los puntos forman una configuración elipsoide.
- SD1 (Eje Transversal): Representa la desviación estándar de la variabilidad a corto plazo latido a latido. Está vinculada casi exclusivamente a la modulación vagal (parasimpática).
- SD2 (Eje Longitudinal): Representa la variabilidad a largo plazo y refleja el balance entre los sistemas simpático y parasimpático.
Índices de Toichi (CVI y CSI): Para cuantificar estas funciones de forma independiente, se utilizan el Cardiac Vagal Index (CVI), calculado como log 
10 (SD1⋅SD2), y el Cardiac Sympathetic Index (CSI), que es la relación SD2/SD1.

b. Para obtener datos fiables, la señal ECG fue capturada a una frecuencia de muestreo de 1000 Hz, lo cual es esencial para una detección precisa de los picos R en estudios de HRV. El filtrado digital se realizó mediante un filtro IIR Butterworth pasabanda (5-15 Hz). Este diseño es útil porque:
- Elimina el offset de DC y el ruido de baja frecuencia causado por la respiración y el movimiento de los electrodos.
- Atenúa el ruido de alta frecuencia y la interferencia de la red eléctrica (60 Hz).
- Preserva la morfología del complejo QRS, permitiendo que el algoritmo de detección localice con exactitud el pico de la onda R, fundamental para calcular los intervalos en milisegundos.

### Parte B

### Parte C
### Análisis de resultados y conclusiones
### Referencias


```python

```
|     |     |     |     |     |
|-----|-----|-----|-----|-----|
|     |     |     |     |     |
|     |     |     |     |     |
|     |     |     |     |     |
|     |     |     |     |     |
|     |     |     |     |     |
|     |     |     |     |     |


</div>
