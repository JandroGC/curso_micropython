# Ejemplo 12, leemos un sensor de temperatura
# y humedad DHT11, mostramos sus valores en una
# pantalla OLED y guardamos un log en una tarjeta SD

from mi_RTC import MyRTC
from machine import Pin, SoftI2C, RTC, SPI
from sdcard import SDCard
import ssd1306
import time
import os
import dht

# Función que graba los datos en tarjeta SD
def logging (horas, temperatura, humedad):
    # Buscamos el archivo con el número mayor y
    # copiamos los valores de hora, temperatura
    # y humedad separados por comas
    listado = os.listdir()
    numeros = []
    for i in listado:
        x = i.find('log')
        if x !=0:
            continue
        y = i.find('.csv')
        numero = int(i[(x+3):y])
        numeros.append(numero)
    print  (numeros)
    max_value = max (numeros)
    archivo = 'log'+str(max_value)+'.csv'
    f = open(archivo, 'a')
    f.write (horas+','+temperatura+','+humedad+'\n')
    f.close()

# Función que crea un nuevo archivo de log
def new_log ():
    # Funcion para crear un nuevo archivo log.
    # Buscamos el archivo con el número mayor y
    # creamos un nuevo archivo con el número siguiente
    listado = os.listdir()
    numeros = []
    for i in listado:
        x = i.find('log')
        if x !=0:
            continue
        y = i.find('.csv')
        numero = int(i[(x+3):y])
        numeros.append(numero)
    
    if numeros == []:
        l = open('log0.csv', 'w')
        l.write('Hora,Temperatura,Humedad\n')
        l.close()
    else:
        max_value = max (numeros)
        archivo = 'log'+str(max_value+1)+'.csv'
        print(archivo)
        l = open(archivo, 'w')
        l.write ('Hora,Temperatura,Humedad\n')
        l.close()

    
# Variables
graba = False
sampling = True
temp = 0
hum = 0

# Introducimos como variables el
# id de la red WIFI y la password
id_red = "ssdi"
pass_red = "password"

# Creamos un objeto RTC y un objeto
# del tipo MyRTC para la sincronizacion
reloj = RTC()
sincro_reloj = MyRTC(id_red, pass_red)

# Sincronizamos el RTC e imprimimos
# por consola
sincro_reloj.sincro()

# Asignamos los pines I2C para el ESP32 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Definimos dimensiones del la pantalla
# y creamos el objeto correspondiente
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

# Indicamos los pines para el bus SPI del 
# lector de SD y lo iniciamos.
spi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
spi.init()
cs = Pin(5)

# Creamos un objeto del tipo SDCard
sd = SDCard(spi, cs)
# Creamos un objeto de sistema de archivos Fat
vfs = os.VfsFat(sd)
# Monatamos el sistema de archivos  como /sd
os.mount(vfs, '/sd')
os.chdir('sd')

# Creamos un objeto DHT11 y le asignamos un Pin
d = dht.DHT11(Pin(14))

# Variable que nos indicará si acabamos de
# sincronizar el reloj
sinc_act = False

# Creamos un log
new_log()
print ('Terminada configuración')

# Creamos un bucle para el programa
while True:
    # Leemos la hora local
    date = time.localtime()
    # Si es domingo y son las 4 de la mañana sincronizamos
    # el RTC y activamos la variable que indica que hemos
    # sincronizado el reloj
    if date[6] == 6 and date[3] == 4 and sinc_act == False:
        sincro_reloj.sincro()
        sinc_act = True
    # El domingo a las 6 de la mañana restablecemos la
    # variable que indica que hemos sincronizado
    if date[6] == 6 and date[3] == 5:
        sin_act = False
    
    # Volvemos a leer la hora local
    date = time.localtime()
    
    # Borramos la pantalla OLED
    oled.fill(0)
    
    # Pasamos la informacion a mostrar a string
    d_semana = ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes',
                'Sábado', 'Domingo')
    m_ano = ('enero','febrero','marzo','abril','mayo','junio','julio',
             'agosto','septiembre','octubre','noviembre','diciembre')
    dia_semana = d_semana[date[6]]
    dia_mes = str(date[2])
    mes = str(m_ano[date[1]-1])
    ano = str(date[0])
    hora = str(date[3])
    minuto = str(date[4])
    segundo = str(date[5])
    
    # Tomamos las medidas con el sensor DHT11 cada 2 segundos
    if date[5] % 2 == 0 and sampling == True:
        d.measure()
        temp = d.temperature()
        hum = d.humidity()
        sampling = False
    if date[5] % 2 != 0:
        sampling = True
    
    # Comenzamos un nuevo log cada semana
    if date[6] == 0 and nuevo_log == True:
        new_log()
        nuevo_log = False
    if date[6] !=0:
        nuevo_log = True
    
    # Añadimos datos al log cada cinco minutos
    if date[4] % 2 == 0 and graba == True:
        horas = hora+':'+minuto
        logging (horas, str(temp),str(hum))
        graba = False
    if date[4] % 2 !=0:
        graba = True
    
    # Mostramos información  en pantalla OLED
    oled.text(dia_semana,5, 5)
    oled.text(dia_mes+'/'+mes+'/'+ano,5,18)
    oled.text(hora+':'+minuto+':'+segundo, 5, 31)
    oled.text('T : '+str(temp), 5, 44)
    oled.text('H : '+str(hum), 5, 57)
    oled.show()
    time.sleep_ms(50)
    
    
    
    
    
    
    
        