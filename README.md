# Se-ales-electromiograf-as-EMG
El electromiograma (EMG) es una grabación de la actividad eléctrica de los
músculos, también llamada actividad mioeléctrica. Existen dos tipos de EMG, el
de superficie y el intramuscular o de aguja.
La respuesta impulsiva puede ser calculada relacionando la corriente generada
en un punto de la fibra muscular y algunas variables relacionadas con la posición
de los electrodos (Devasahayam, 2013). La ecuación (1) muestra la forma de
calcular la respuesta impulsiva del potencial de acción medido con electrodos de
superficie.
![image](https://github.com/user-attachments/assets/9559c158-240a-44cd-ba0a-d19a1b5928cd)

1. Preparación del Sujeto:
- Colocar los electrodos de superficie sobre el músculo a analizar, asegurando
una buena adherencia con gel conductor.
Conectar los electrodos al amplificador y al sistema DAQ.
- Seleccionar un músculo a estudiar y calcular la frecuencia de muestreo
necesaria para realizar la captura de la señal. 

2. Adquisición de la Señal EMG:
• Pedir al sujeto que realice una contracción muscular continua hasta llegar a
la fatiga.
• Registrar la señal EMG en tiempo real durante todo el proceso.
 En este laboratorio no se urilizo un modulo de electromiografia sino de electrocardiograma.

Asi se captura la señal electromiografica, se toman 1000 muestras por segundo, la abquisicion de la señal durara dos minutos, num_samples tomara el total de muestras que se tomaran, se crea una tarea DAQmx para abquirir los datos desde la tarjeta de abquisicion por medio de la libreria, se diseñal un canal analogico llamado DEV2/ao1 que aparece al conectar el DAQ en el programa descargado para medir el voltaje, se capturan datos hasta completar el total de muestras que se tomaran, task.start() inicia la abquisicion de la tarjeta DAQ, se capturan la lista de voltajes capturados en cada instante de tiempo, time_axis es el eje de tiempo creado para la grafica desde cero hasta la duracion, se abre este archivo datos_adquiridos.txt y se escribe cada muestra en el archivo creando una fila de tiempo y otra de voltaje. 

![image](https://github.com/user-attachments/assets/b3b2083c-8270-4f60-8ea8-a91acd01e061)

Se carga los datos que se tienen en el archivo creado arteriormente, se ignora el encabezado para solo tener los datos, se separan los datos en dos arreglos en tiempo almacena los datos de tiempo y voltaje almacena los datos de voltaje, se coloca la frecuencia de muestreo, se calcula el tiempo total en egundos 120 segundos, la longitud de la señal con len(voltaje), se grafican esos datos ele je x el tiempo y en el eje y el voltaje, el musculo medido fue bíceps braquial.La cantidad de contracciones se diseña un filtro pasa banda Butterworth para eliminar el ruido y conservar las frecuencias relevantes, se calculan los coeficientes b y a a las caules se le aplica un filtro, se toma el valor absoluto de la señal filtrada para facilitar la deteccion de actividad muscular, se aplica un suavizado con una ventana de 200 ms para obtener la envolvente de la señal, se calculan cuantas muestras hay en esos 200 ms, para esta deteccion se define un umbral adptativo, se usa la media de la envolvente más 2 veces la desviación estándar, con esto se asegura que solo los picos significativos sean detectados como contracciones, se genera un vector de verdadero actividad y falso reposo, se detectan los cambios de falso a verdadero como inicio de una contraccion, se divide entre dos porque cada contraccion genera un inicio y un fin. 
Cantidad de contracciones detectadas: 58. 

 ![image](https://github.com/user-attachments/assets/90fae1e9-dfa7-45bc-a4ef-48e4013061e5)

 ![image](https://github.com/user-attachments/assets/5d887e79-d05c-4d63-9b69-648033ecb50e)


3. Filtrado de la Señal:
• Aplicar un filtro pasa altas para eliminar componentes de baja frecuencia
(ruido asociado a la línea base o al movimiento).
• Utilizar un filtro pasa bajas para eliminar frecuencias altas no deseadas, como
el ruido electromagnético o de interferencia de alta frecuencia.

Se calcula la frecuencia de Nyquist (fs / 2), que es el límite máximo de frecuencia que podemos analizar, Se establecen las frecuencias de corte para el filtro pasa-banda:- lowcut = 20 Hz: elimina componentes de muy baja frecuencia. - highcut = 450 Hz: elimina componentes de muy alta frecuencia, se aumenta la margen para definir la banda de rechazo mejorando la selectividad del filtro, se tienen que definir las frecuencias de paso para eso es wp y ws en terminos de la frecuancia de Nyquist, tambien se indican los dB permitidos en la banda de paso y los atenuados en las variables gpass y gstop. Se usa la funcion buttord() para calcular el orden del filtro Butterworth que cumple con los requisitos de atenuacion, los coeficientes b y a representan el filtro en su forma de función de transferencia. La funcion lfilter() aplica un filtro a la señal voltge produciendo una señal filtrada, y se grafica por ultimo la señal filtrada, mostrando solo los primero cuatro segundos. Se utiliza un frecuencia de corte baje de 20 Hz ya que la actividad de EMG se encuentra principalmente en frecuencias superiores a 20 Hz.Frecuencia de corte alta 450 Hz ya que la actividad EMG por encima de 450 Hz es mínima y contiene principalmente ruido electromagnético y térmico.

![image](https://github.com/user-attachments/assets/f61b5aff-b8b1-453f-a6dd-e0cff2875059)

![image](https://github.com/user-attachments/assets/aa0386d5-f0f3-49fe-88e5-87f0a57a2ebb)

4. Aventanamiento:
Define el tamaño de cada ventana, segmento de la señal, tambien indica cuantas muestras se superponen entre ventanas consecutivas, la resta entre ambos difine el desplazamiento entre cada ventana, se guarda las señales segmentadas con la ventana aplicada, se almacenan los espectros de frecuencia obtenidas de cada ventana, se calcula las frecuencias correspondientes a las fft de cada ventana y se crea una figura para mostrar los resultados de aplicar la ventana en el dominio del tiempo por medio de una ventana Hamming ya que esta ayuda a minimizar las discontinuidades entre ventanas consecutivas y mejora la representación espectral global, tiene un mejor control del lóbulo principal y lóbulos secundarios más atenuados en comparación con otras ventanas. Donde se crea un bucle sobre la señal en intervalos de la resta anteriormente mencionada creando bloques del tamaño de la ventana, se aplica la ventana de Hamming para suavizar los bordes, se guarda la señal ventaneada y se grafica. Se aplica la transformada de Fourier a cada ventana se repite el mismo bucle de ventaneo, calcula la FFT de la señal ventaneada y se grafican los espectros obtenidos por cada ventana, Se selecciona un segmento especifico para analizar donde se define un intervalo de tiempo de analisis que fue de 60 a 63 segundo donde se veia una fatiga, se convierte el tiempo en muestras, se encuentra el punto final en muestras, se aplica la ventana de Hanning en este caso ya que proporciona una mayor supresión de lóbulos laterales, lo que es útil cuando se analiza un solo segmento y se quiere minimizar la interferencia de otras frecuencias., la ecuación de la ventana de Hanning:

 w[n] = 0.5 * (1 - cos(2*pi*n/(N-1))) para n = 0,1,...,N-1

 Para esta ventana se extrae el segmento deseado, se crea una ventana de Hanning, aplica la ventana al segmento y se grafica el segmento ventaneado, se aplica la transfromada de Fourier al segmento ventaneado, se calcula la FFT, se obtiene la magnitud de la FFT, se grafica el espectro de frecuencia. 

 La comparación entre la señal original y la señal segmentada en ventanas muestra cómo el procesamiento de la señal transforma su representación en el dominio del tiempo. La señal original se observa de manera continua, con sus variaciones de amplitud y frecuencia a lo largo del tiempo, sin modificaciones. la señal con aventanamiento ha sido dividida en segmentos superpuestos mediante ventanas de Hamming, lo que permite analizarla por partes sin generar discontinuidades abruptas. Esta segmentación es esencial para estudios en el dominio de la frecuencia, como la transformada de Fourier por ventana, ya que ayuda a capturar cambios locales en la señal sin introducir efectos indeseados en los bordes. Aunque la forma general de la señal se mantiene, la visualización segmentada resalta la aplicación de la técnica de ventaneo, mostrando cada fragmento como una unidad independiente lista para su análisis espectral.
 
![image](https://github.com/user-attachments/assets/b26d2146-40ce-43c5-9ba4-0086a1f8d46b)

![image](https://github.com/user-attachments/assets/2ab7cc85-ada5-42a6-a522-d4e49dfba827)

![image](https://github.com/user-attachments/assets/141b5275-4e11-4e8f-be44-230ca51789a8)

![image](https://github.com/user-attachments/assets/9e15b4e8-9ed0-491a-9320-441621e51789)

![image](https://github.com/user-attachments/assets/ac001e4b-8f2d-4a1b-80c9-c419885ee653)

5. Analisis espectral:

Se genera un arreglo con los tiempos correspondientes a cada ventana de analisis, se inicializa una lista para almacenar la recuencia mediana de cada ventana, se recorre la señal en intervalos de pasos, extrayendo una ventana de tamaño tamaño_ventana, a la ventana se le aplica la ventana de Hamming para reducir efectos de discontinuidad en el análisis de frecuencia, se aplica la transformada de Fourier rapida y se obtienen el espectro de frecuencias en valores absolutos, se calcula la frecuencia mediana que es el punto donde la mitad de la energía espectral está contenida en frecuencias menores y la otra mitad en frecuencias mayores, se obtiene el índice de la frecuencia mediana y se guarda su valor, se alamcena la frecuancia mediana en la lista. Se grafica la evolucion de la frecuancia mediana a lo largo del tiempo. 

![image](https://github.com/user-attachments/assets/09e695fd-9c83-4e9e-b354-1ddab4f6fa05)

![image](https://github.com/user-attachments/assets/0879f649-081e-4421-9f1f-a8e9adb03fee)

Se extraen los valores los valores de la primera y ultima ventana, se crean 10 muestras aleatorias con una media igual a primera y segunda muestra respectivamente y desviacion estandar de 5 Hz, se calcula media, varianza y desviacion estandar de ambas muestras, se calcula el estadistico t que mide la diferencia en tre las dos medias normalizadas y su variabilidad, se calcula el p valor que indica la probabilidad de que las diferencias entre medias sean debidas al azar, se imprimen los resultados estadisticos: 

Prueba de Hipótesis: t=nan, p=nan

Media 1: 9.78, Media 2: 6.80

Varianza 1: 9.73, Varianza 2: 16.10

Desviación 1: 3.12, Desviación 2: 4.01

t = 1.86, p-valor = 0.0636

![image](https://github.com/user-attachments/assets/44aee9f8-d5ca-46ef-91f7-dddb426d53f7)

![image](https://github.com/user-attachments/assets/97150675-1ad7-45c8-990f-5a91895fcaed)










 




