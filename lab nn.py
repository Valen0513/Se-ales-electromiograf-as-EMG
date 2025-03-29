import csv
import matplotlib.pyplot as plt

# Leer el archivo CSV
filename = "senal_.csv"
timestamps = []
data = []

with open(filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Saltar encabezado

    for row in reader:
        timestamps.append(float(row[0]))  # Tiempo
        data.append(float(row[1]))  # Voltaje

# Verificar si hay datos
if timestamps:
    print("Primeros valores:", list(zip(timestamps, data))[:10])

    # Graficar
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, data, label="Señal EMG", color="blue")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG Guardada")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("El archivo está vacío. Verifica la captura de datos.")

#%%
import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np

# Parámetros de adquisición
sample_rate = 1000         # Frecuencia de muestreo en Hz
duration_minutes = 0.5    # Duración de la adquisición en minutos
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