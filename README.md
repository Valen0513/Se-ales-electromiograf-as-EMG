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

Se carga los datos que se tienen en el archivo creado arteriormente, se ignora el encabezado para solo tener los datos, se separan los datos en dos arreglos en tiempo almacena los datos de tiempo y voltaje almacena los datos de voltaje, se coloca la frecuencia de muestreo, se calcula el tiempo total en egundos 120 segundos, la longitud de la señal con len(voltaje), se grafican esos datos ele je x el tiempo y en el eje y el voltaje, el musculo medido fue bíceps braquial. Cantidad de contracciones detectadas: 58. 

 ![image](https://github.com/user-attachments/assets/90fae1e9-dfa7-45bc-a4ef-48e4013061e5)

4. Filtrado de la Señal:
• Aplicar un filtro pasa altas para eliminar componentes de baja frecuencia
(ruido asociado a la línea base o al movimiento).
• Utilizar un filtro pasa bajas para eliminar frecuencias altas no deseadas, como
el ruido electromagnético o de interferencia de alta frecuencia.

Se calcula la frecuencia de Nyquist (fs / 2), que es el límite máximo de frecuencia que podemos analizar, Se establecen las frecuencias de corte para el filtro pasa-banda:- lowcut = 20 Hz: elimina componentes de muy baja frecuencia. - highcut = 450 Hz: elimina componentes de muy alta frecuencia, se aumenta la margen para definir la banda de rechazo mejorando la selectividad del filtro, se tienen que definir las frecuencias de paso para eso es wp y ws en terminos de la frecuancia de Nyquist, tambien se indican los dB permitidos en la banda de paso y los atenuados en las variables gpass y gstop. Se usa la funcion buttord() para calcular el orden del filtro Butterworth que cumple con los requisitos de atenuacion, los coeficientes b y a representan el filtro en su forma de función de transferencia. La funcion lfilter() aplica un filtro a la señal voltge produciendo una señal filtrada, y se grafica por ultimo la señal filtrada, mostrando solo los primero cuatro segundos. Se utiliza un frecuencia de corte baje de 20 Hz ya que la actividad de EMG se encuentra principalmente en frecuencias superiores a 20 Hz.Frecuencia de corte alta 450 Hz ya que la actividad EMG por encima de 450 Hz es mínima y contiene principalmente ruido electromagnético y térmico.

![image](https://github.com/user-attachments/assets/f61b5aff-b8b1-453f-a6dd-e0cff2875059)

 




