
#%%
import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np

# Parámetros de adquisición
sample_rate = 1000         # Frecuencia de muestreo en Hz
duration_minutes = 2   # Duración de la adquisición en minutos
duration_seconds = duration_minutes * 60  # Duración en segundos
num_samples = int(sample_rate * duration_seconds)  # Número total de muestras

with nidaqmx.Task() as task:
    # Configurar canal (ajusta "Dev3/ai0" según tu dispositivo)
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
    
    # Configurar la tarea para adquisición FINITA de num_samples muestras
    task.timing.cfg_samp_clk_timing(
        sample_rate,
        sample_mode=AcquisitionType.FINITE,
        samps_per_chan=num_samples
    )
    
    # Iniciar la tarea
    task.start()
    
    # Esperar a que la adquisición se complete. Se le da un margen extra al timeout.
    task.wait_until_done(timeout=duration_seconds + 10)
    
    # Leer los datos adquiridos (número esperado de muestras)
    data = task.read(number_of_samples_per_channel=num_samples)

# Crear un eje de tiempo para la gráfica
time_axis = np.linspace(0, duration_seconds, num_samples, endpoint=False)
with open("datos_adquiridos.txt", "w") as archivo_txt:
    archivo_txt.write("Tiempo (s)\tVoltaje (V)\n")
    for t, v in zip(time_axis, data):
        archivo_txt.write(f"{t:.6f}\t{v:.6f}\n")
        
#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, windows
from scipy.fftpack import fft, fftfreq
from scipy.stats import ttest_ind
from scipy.stats import ttest_ind, norm

# Cargar datos desde el archivo
señal_EMG = np.loadtxt("C:/Users/HP RY5/Desktop/Practica_1/datos_adquiridos.txt", skiprows=1)
tiempo = señal_EMG[:, 0]
voltage = señal_EMG[:, 1]
fs = 1000 
duracion2=len(voltage)/fs
print("duracion de la señal",duracion2)
fs = 1000      # Frecuencia de muestreo (Hz)
lowcut = 20    # Frecuencia mínima de corte (Hz)
highcut = 490  # Frecuencia máxima de corte (Hz)

# 1. Graficar la señal original
plt.figure(figsize=(20, 5))
plt.plot(tiempo, voltage, label="Señal Original", color='blue')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal Original")
plt.xlim(0,120)
plt.legend()
plt.show()

#-------------FILTRO PASA-BANDA------------------
# Parámetros del filtro
nyquist = 0.5 * fs
order = 4  # Orden del filtro

# Diseñar el filtro
b, a = butter(order, [lowcut / nyquist, highcut / nyquist], btype='band')

# Aplicar el filtro a la señal
filtered_voltage = lfilter(b, a, voltage)

plt.figure(figsize=(20, 5))
plt.plot(tiempo, filtered_voltage, label="Señal Filtrada", color='orange')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal Filtrada")
plt.xlim(0,4)
plt.legend()
plt.show()
plt.grid()
# 3.ventana de Hanning
# Por ejemplo, entre 24 y 30 segundos
inicio_sec = 93
fin_sec = 95
inicio = int(inicio_sec * fs)
fin = int(fin_sec * fs)

segmento = filtered_voltage[inicio:fin]
N = len(segmento)
# Ecuación de la ventana de Hanning:
#   w[n] = 0.5 * (1 - cos(2*pi*n/(N-1))) para n = 0,1,...,N-1
ventana = np.hanning(N)
segmento_ventaneado = segmento * ventana

plt.figure(figsize=(20, 5))
plt.plot(tiempo[inicio:fin], segmento_ventaneado, label="Segmento Ventaneado (Hanning)", color='green')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Segmento Ventaneado con Ventana de Hanning")
plt.legend()
plt.show()
plt.grid()


#============================ AVENTANAMIENTO ============================

tamaño_ventana=500
superposicion_ventanas=250
pasos = tamaño_ventana - superposicion_ventanas
aplicar_ventanas = []
espectros = []
frecuencias = np.fft.rfftfreq(tamaño_ventana, d=1/fs)
frecuencias_medias=[]

plt.figure(figsize=(12, 8))
# Figura para mostrar las ventanas aplicadas en el dominio del tiempo
plt.figure(figsize=(12, 6))
plt.title("Señal Segmentada en Ventanas de Tiempo")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

for i in range(0, len(filtered_voltage) - tamaño_ventana, pasos):
    ventana_señal = filtered_voltage[i:i+tamaño_ventana] * windows.hamming(tamaño_ventana)
    aplicar_ventanas.append(ventana_señal)
    
    # Graficar cada ventana en el dominio del tiempo
    plt.plot(range(i, i + tamaño_ventana), ventana_señal, alpha=0.5)

plt.show()

for i in range(0, len(filtered_voltage) - tamaño_ventana, pasos):
    ventana_señal = filtered_voltage[i:i+tamaño_ventana] * windows.hamming(tamaño_ventana)
    spectrum = np.abs(np.fft.rfft(ventana_señal))
    
    aplicar_ventanas.append(ventana_señal)
    espectros.append(spectrum)
    
    
    plt.plot(frecuencias, spectrum, alpha=0.5)

plt.title("Espectro de Frecuencia de Cada Ventana (FFT)")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.show()

seccion_inicial = 60
seccion_final = 63
inicio = int(seccion_inicial * fs)
fin = int(seccion_final * fs)

segmento = filtered_voltage[inicio:fin]
N = len(segmento)

ventana = np.hanning(N)
segmento_ventaneado = segmento * ventana

plt.figure(figsize=(20, 5))
plt.plot(tiempo[inicio:fin], segmento_ventaneado, label="Segmento Ventaneado (Hanning)", color='green')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Segmento Ventaneado con Ventana de Hanning")
plt.legend()
plt.show()
plt.grid()

fft_segmento = np.fft.rfft(segmento_ventaneado)
fft_magnitude = np.abs(fft_segmento)
frecuencias = np.fft.rfftfreq(N, d=1/fs)

plt.figure(figsize=(20, 5))
plt.plot(frecuencias, fft_magnitude, label="Espectro (FFT)", color='red')
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.title("Análisis Espectral del Segmento Ventaneado")
plt.grid(True)
plt.legend()
plt.show()

# ============================ ANALISIS ESPECTRAL ============================

# Simulación de frecuencias medianas obtenidas en diferentes ventanas
tiempo_ventanas = np.arange(0, len(filtered_voltage) - tamaño_ventana, pasos) / fs  # Simulación de tiempos

tendencia_frec_mediana = []

for i in range(0, len(filtered_voltage) - tamaño_ventana, pasos):
    ventana_señal = filtered_voltage[i:i+tamaño_ventana] * np.hamming(tamaño_ventana)
    spectrum = np.abs(np.fft.rfft(ventana_señal))
    
    # Calcular la frecuencia mediana
    cumsum_power = np.cumsum(spectrum)
    median_index = np.where(cumsum_power >= cumsum_power[-1] / 2)[0][0]
    median_freq = frecuencias[median_index]
    
    tendencia_frec_mediana.append(median_freq)

# Graficar la evolución de la frecuencia mediana
plt.figure(figsize=(10, 4))
plt.plot(tiempo_ventanas, tendencia_frec_mediana, marker='o', linestyle='-', color='r')
plt.title("Evolución de la Frecuencia Mediana en Cada Ventana")
plt.xlabel("Tiempo (s)")
plt.ylabel("Frecuencia Mediana (Hz)")
plt.grid()
plt.show()


# Valores de frecuencia mediana en la primera y segunda ventana
primera_frec = tendencia_frec_mediana[0]
segunda_frec = tendencia_frec_mediana[1]
# Comparar la primera y segunda frecuencia mediana
t_estadistico, p_valor = ttest_ind([primera_frec], [segunda_frec], alternative='two-sided')
print(f"Prueba de Hipótesis: t={t_estadistico:.2f}, p={p_valor:.4f}")
# Crear listas con valores cercanos para simular muestras (ya que n=1 es un problema)
muestra1 = np.random.normal(primera_frec, 5, 10)  # Simulamos 10 valores alrededor de la primera frecuencia
muestra2 = np.random.normal(segunda_frec, 5, 10)  # Simulamos 10 valores alrededor de la segunda frecuencia

# Calcular estadísticas
media1 = np.mean(muestra1)
media2 = np.mean(muestra2)
varianza1 = np.var(muestra1, ddof=1)  # Varianza con corrección de Bessel (ddof=1)
varianza2 = np.var(muestra2, ddof=1)
desviacion1 = np.std(muestra1, ddof=1)
desviacion2 = np.std(muestra2, ddof=1)

# Calcular t utilizando la ecuación de la imagen
t = (media1 - media2) / np.sqrt((varianza1 / len(muestra1)) + (varianza2 / len(muestra2)))

# Calcular p-valor basado en la distribución t de Student
p_valor = 2 * (1 - norm.cdf(abs(t)))

# Mostrar resultados
print(f"Media 1: {media1:.2f}, Media 2: {media2:.2f}")
print(f"Varianza 1: {varianza1:.2f}, Varianza 2: {varianza2:.2f}")
print(f"Desviación 1: {desviacion1:.2f}, Desviación 2: {desviacion2:.2f}")
print(f"t = {t:.2f}, p-valor = {p_valor:.4f}")

if p_valor < 0.05:
    print("🔴 La diferencia es significativa. Puede haber fatiga muscular.")
else:
    print("🟢 No hay evidencia suficiente para confirmar fatiga.")

# Graficar distribución normal con t
x = np.linspace(-5, 5, 100)
y = norm.pdf(x, 0, 1)  # Distribución normal estándar

plt.figure(figsize=(6, 4))
plt.plot(x, y, label="Distribución Normal")
plt.axvline(t, color='red', linestyle='dashed', label=f"t = {t:.2f}")
plt.fill_between(x, y, where=(x >= t) | (x <= -t), color='gray', alpha=0.3)
plt.title("Distribución de t con Regiones Críticas")
plt.xlabel("Valor de t")
plt.ylabel("Densidad")
plt.legend()
plt.grid()
plt.show()
