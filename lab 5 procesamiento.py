# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:37:07 2026

@author: pipe1
"""

# -*- coding: utf-8 -*-
"""
Lectura de ECG desde txt, Análisis HRV y Visualización de Filtro IIR
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks, freqz

# ==========================================
# 1. PARÁMETROS GENERALES
# ==========================================
fs = 1000  # Frecuencia de muestreo en Hz
archivo_entrada = 'senal_ad8232_bruta3.txt'

# ==========================================
# 2. LECTURA DE LA SEÑAL DESDE TXT
# ==========================================
print(f"Leyendo señal del archivo '{archivo_entrada}'...")
try:
    # Se usa skiprows=1 para saltar el encabezado original
    senal_bruta = np.loadtxt(archivo_entrada, skiprows=1)
    num_muestras = len(senal_bruta)
    duracion = num_muestras / fs
    print(f"Señal leída con éxito. Duración total: {duracion:.2f} segundos.")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    print("Generando señal simulada con ruido para pruebas...")
    duracion = 240
    num_muestras = fs * duracion
    t_sim = np.linspace(0, duracion, num_muestras)
    # Señal base de 1.2 Hz (72 BPM) con variabilidad añadida
    senal_bruta = np.sin(2 * np.pi * 1.2 * t_sim) + np.random.normal(0, 0.2, num_muestras)

# ==========================================
# 3. DISEÑO E IMPLEMENTACIÓN DEL FILTRO IIR
# ==========================================
nyquist = 0.5 * fs
low = 5.0 / nyquist
high = 15.0 / nyquist
# Filtro Butterworth pasabanda de 2do orden
b, a = butter(2, [low, high], btype='band')

print("\n--- Coeficientes de la Función de Transferencia H(z) ---")
print("Numerador (b):", np.round(b, 6))
print("Denominador (a):", np.round(a, 6))

# Calcular la respuesta en frecuencia del filtro
w, h = freqz(b, a, worN=8000)
frecuencias = (w * fs) / (2 * np.pi)  # Convertir radianes/muestra a Hz
magnitud_db = 20 * np.log10(np.abs(h) + 1e-12) # Se suma 1e-12 para evitar log(0)
fase_rad = np.unwrap(np.angle(h))

# Graficar la Función de Transferencia
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(frecuencias, magnitud_db, color='b')
plt.title('Función de Transferencia del Filtro IIR (Butterworth Pasabanda 5-15 Hz)')
plt.ylabel('Magnitud [dB]')
plt.axvline(5, color='r', linestyle='--', alpha=0.6, label='Corte Inferior (5 Hz)')
plt.axvline(15, color='r', linestyle='--', alpha=0.6, label='Corte Superior (15 Hz)')
plt.xlim(0, 50)  # Limitamos a 50 Hz para ver claramente la banda de paso
plt.ylim(-60, 5)
plt.legend()
plt.grid(True, alpha=0.5)

plt.subplot(2, 1, 2)
plt.plot(frecuencias, fase_rad, color='g')
plt.ylabel('Fase [rad]')
plt.xlabel('Frecuencia [Hz]')
plt.xlim(0, 50)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()

# Aplicar el filtro a la señal
senal_filtrada = lfilter(b, a, senal_bruta)

# ==========================================
# 4. DIVISIÓN DE LA SEÑAL (2 segmentos)
# ==========================================
mitad_muestras = int(num_muestras / 2)
segmento_1 = senal_filtrada[:mitad_muestras]
segmento_2 = senal_filtrada[mitad_muestras:]

# ==========================================
# 5. IDENTIFICACIÓN DE PICOS Y CÁLCULO HRV
# ==========================================
def analizar_hrv(senal_seg, fs_rate, nombre_segmento):
    # Detección de picos R
    distancia_minima = int(0.4 * fs_rate)
    altura_minima = np.mean(senal_seg) + 1.5 * np.std(senal_seg)
    picos, _ = find_peaks(senal_seg, height=altura_minima, distance=distancia_minima)
    
    # Calcular intervalos R-R y convertir a milisegundos
    rr_ms = (np.diff(picos) / fs_rate) * 1000
    
    print(f"\n{'='*40}")
    print(f"RESULTADOS: {nombre_segmento}")
    print(f"{'='*40}")
    print(f"Picos R encontrados: {len(picos)}")
    
    if len(rr_ms) > 1:
        # --- Dominio del Tiempo ---
        media_rr = np.mean(rr_ms)
        sdrr = np.std(rr_ms, ddof=1)
        
        # --- Diagrama de Poincaré ---
        rr_n = rr_ms[:-1]
        rr_n1 = rr_ms[1:]
        
        # Desviaciones estándar espaciales (elipse)
        sd1 = np.sqrt(0.5 * np.var(rr_n1 - rr_n, ddof=1))
        sd2 = np.sqrt(0.5 * np.var(rr_n1 + rr_n, ddof=1))
        
        # --- Índices Autonómicos ---
        cvi = np.log10((sd1 * sd2) + 1e-12)
        csi = sd2 / sd1 if sd1 != 0 else 0
        
        print(f"Frecuencia Cardíaca Media : {60 / (media_rr/1000):.1f} BPM")
        print(f"Media R-R                 : {media_rr:.2f} ms")
        print(f"Desviación Estándar (SDRR): {sdrr:.2f} ms")
        print(f"SD1 (Actividad Vagal)     : {sd1:.2f} ms")
        print(f"SD2 (Simpático/Vagal)     : {sd2:.2f} ms")
        print(f"CVI (Índice Vagal)        : {cvi:.4f}")
        print(f"CSI (Índice Simpático)    : {csi:.4f}")
        
        return picos, rr_ms, rr_n, rr_n1, sd1, sd2
    else:
        print("No hay suficientes picos para el análisis.")
        return picos, [], [], [], 0, 0

# Analizar ambos segmentos
res_1 = analizar_hrv(segmento_1, fs, "Segmento 1 (Primera Mitad)")
res_2 = analizar_hrv(segmento_2, fs, "Segmento 2 (Segunda Mitad)")

# ==========================================
# 6. VISUALIZACIÓN GRÁFICA (Tachograma y Poincaré)
# ==========================================
picos_1, rr_ms_1, rr_n_1, rr_n1_1, sd1_1, sd2_1 = res_1
picos_2, rr_ms_2, rr_n_2, rr_n1_2, sd1_2, sd2_2 = res_2

plt.figure(figsize=(16, 10))

# --- Gráfica 1: Tachograma Segmento 1 ---
plt.subplot(2, 2, 1)
plt.plot(rr_ms_1, marker='o', linestyle='-', color='g', markersize=4)
plt.title('Tachograma - Segmento 1')
plt.xlabel('Número de Latido')
plt.ylabel('Intervalo R-R [ms]')
plt.grid(True, alpha=0.5)

# --- Gráfica 2: Tachograma Segmento 2 ---
plt.subplot(2, 2, 2)
plt.plot(rr_ms_2, marker='o', linestyle='-', color='b', markersize=4)
plt.title('Tachograma - Segmento 2')
plt.xlabel('Número de Latido')
plt.ylabel('Intervalo R-R [ms]')
plt.grid(True, alpha=0.5)

# --- Gráfica 3: Diagrama de Poincaré Segmento 1 ---
plt.subplot(2, 2, 3)
plt.scatter(rr_n_1, rr_n1_1, alpha=0.6, color='g', edgecolor='k')
min_lim = min(min(rr_n_1), min(rr_n1_1)) - 50 if len(rr_n_1)>0 else 0
max_lim = max(max(rr_n_1), max(rr_n1_1)) + 50 if len(rr_n_1)>0 else 1000
plt.plot([min_lim, max_lim], [min_lim, max_lim], 'r--', label='Línea Identidad')
plt.title(f'Poincaré - Seg 1\nSD1: {sd1_1:.1f} | SD2: {sd2_1:.1f}')
plt.xlabel('$RR_n$ [ms]')
plt.ylabel('$RR_{n+1}$ [ms]')
plt.legend()
plt.grid(True, alpha=0.5)

# --- Gráfica 4: Diagrama de Poincaré Segmento 2 ---
plt.subplot(2, 2, 4)
plt.scatter(rr_n_2, rr_n1_2, alpha=0.6, color='b', edgecolor='k')
min_lim = min(min(rr_n_2), min(rr_n1_2)) - 50 if len(rr_n_2)>0 else 0
max_lim = max(max(rr_n_2), max(rr_n1_2)) + 50 if len(rr_n_2)>0 else 1000
plt.plot([min_lim, max_lim], [min_lim, max_lim], 'r--', label='Línea Identidad')
plt.title(f'Poincaré - Seg 2\nSD1: {sd1_2:.1f} | SD2: {sd2_2:.1f}')
plt.xlabel('$RR_n$ [ms]')
plt.ylabel('$RR_{n+1}$ [ms]')
plt.legend()
plt.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()