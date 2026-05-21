# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:18:11 2026

@author: pipe1
"""

import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from scipy.signal import butter, lfilter, find_peaks

# ==========================================
# 1. PARÁMETROS GENERALES
# ==========================================
fs = 1000  # Frecuencia de muestreo en Hz
duracion = 240  # 4 minutos = 240 segundos
num_muestras = fs * duracion
canal_daq = 'Dev5/ai0'  # Cambiar según la configuración de tu tarjeta DAQ
archivo_salida = 'senal_ad8232_bruta.txt'

# ==========================================
# 2. CAPTURA DE LA SEÑAL CON DAQ
# ==========================================
print("Iniciando captura de 4 minutos... Por favor, mantén la calma.")
try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(canal_daq)
        # Configurar el reloj de muestreo
        task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=num_muestras)
        
        # Leer datos (timeout de 250s para dar margen a los 4 minutos)
        senal_bruta = task.read(number_of_samples_per_channel=num_muestras, timeout=250.0)
    print("Captura finalizada con éxito.")
except Exception as e:
    print(f"Error con la DAQ: {e}")
    print("Generando señal simulada para continuar con la demostración...")
    # Señal simulada en caso de no tener la DAQ conectada para probar el código
    t_sim = np.linspace(0, duracion, num_muestras)
    senal_bruta = np.sin(2 * np.pi * 1.2 * t_sim) + np.random.normal(0, 0.5, num_muestras) 

# Convertir a arreglo de numpy
senal_bruta = np.array(senal_bruta)

# Guardar la señal bruta en un archivo txt
np.savetxt(archivo_salida, senal_bruta, fmt='%.6f', header='Amplitud (V)')
print(f"Señal guardada en {archivo_salida}")

# ==========================================
# 3. DISEÑO E IMPLEMENTACIÓN DEL FILTRO IIR
# ==========================================
# Filtro pasabanda Butterworth de 2do orden (5 a 15 Hz) para resaltar picos R
nyquist = 0.5 * fs
low = 5.0 / nyquist
high = 15.0 / nyquist
b, a = butter(2, [low, high], btype='band')

print("\n--- Ecuación en Diferencias del Filtro ---")
print(f"Coeficientes b (numerador): {b}")
print(f"Coeficientes a (denominador): {a}")
print("y[n] = {:.6f}*x[n] + {:.6f}*x[n-1] + ... - ({:.6f}*y[n-1] + ...)".format(b[0], b[1], a[1]))

# Implementar filtro con condiciones iniciales en 0 (comportamiento por defecto de lfilter sin pasar 'zi')
senal_filtrada = lfilter(b, a, senal_bruta)
np.savetxt(archivo_salida, senal_bruta, fmt='%.6f', header='Amplitud (V)')
print(f"Señal guardada en {archivo_salida}")



# ==========================================
# 4. DIVISIÓN DE LA SEÑAL (2 segmentos de 2 mins)
# ==========================================
mitad_muestras = int(num_muestras / 2)

segmento_1 = senal_filtrada[:mitad_muestras]
segmento_2 = senal_filtrada[mitad_muestras:]
tiempo_seg_1 = np.arange(0, mitad_muestras) / fs
tiempo_seg_2 = np.arange(mitad_muestras, num_muestras) / fs






# ==========================================
# 5. IDENTIFICACIÓN DE PICOS R Y CÁLCULO R-R
# ==========================================
def analizar_segmento(senal_seg, fs_rate, nombre_segmento):
    # La distancia mínima entre picos R (asumiendo max 150 latidos por minuto) es ~0.4 segundos
    distancia_minima = int(0.4 * fs_rate)
    
    # Encontrar picos. Se usa un umbral de altura basado en el RMS de la señal
    altura_minima = np.mean(senal_seg) + 1.5 * np.std(senal_seg)
    picos, _ = find_peaks(senal_seg, height=altura_minima, distance=distancia_minima)
    
    # Calcular intervalos R-R en segundos
    intervalos_rr = np.diff(picos) / fs_rate
    
    print(f"\n[{nombre_segmento}]")
    print(f"Picos R encontrados: {len(picos)}")
    if len(intervalos_rr) > 0:
        print(f"Intervalo R-R medio: {np.mean(intervalos_rr):.4f} segundos")
        print(f"Frecuencia Cardíaca Media: {60 / np.mean(intervalos_rr):.1f} BPM")
    
    return picos, intervalos_rr

picos_1, rr_1 = analizar_segmento(segmento_1, fs, "Segmento 1 (0-2 min)")
picos_2, rr_2 = analizar_segmento(segmento_2, fs, "Segmento 2 (2-4 min)")

# ==========================================
# 6. VISUALIZACIÓN
# ==========================================
plt.figure(figsize=(14, 8))

# Mostrar solo los primeros 10 segundos del Segmento 1 para que sea visible
muestras_10s = int(10 * fs)

plt.subplot(2, 1, 1)
plt.plot(tiempo_seg_1[:muestras_10s], segmento_1[:muestras_10s], label='Señal Filtrada')
# Filtrar los picos que caen dentro de esos primeros 10 segundos para la gráfica
picos_visibles = picos_1[picos_1 < muestras_10s]
plt.plot(tiempo_seg_1[picos_visibles], segmento_1[picos_visibles], "rx", label='Picos R')
plt.title('Segmento 1 (Primeros 10 segundos)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()

# Gráfica de los intervalos R-R del Segmento 1 (Tachograma)
plt.subplot(2, 1, 2)
plt.plot(rr_1, marker='o', linestyle='-', color='g')
plt.title('Nueva Señal: Variabilidad de Intervalos R-R (Tachograma) - Segmento 1')
plt.xlabel('Número de Latido')
plt.ylabel('Intervalo R-R [s]')
plt.grid()

plt.tight_layout()
plt.show()