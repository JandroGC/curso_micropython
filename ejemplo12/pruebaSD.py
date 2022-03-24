# Importamos las librerías necesarias
from sdcard import SDCard
from machine import SPI, Pin
import os

# Indicamos los pines para el bus SPI
# y lo iniciamos.
spi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
spi.init()
cs = Pin(5)

# Creamos un objeto del tipo SDCard
sd = SDCard(spi, cs)

# Creamos un objeto de sistema de archivos Fat
vfs = os.VfsFat(sd)
# Monatamos el sistema de archivos  como /sd
os.mount(vfs, '/sd')

# Imprimimos listado del directorio raiz
print('Root directory:{}'.format(os.listdir()))

# Cambiamos a la SD e imprimos contenido
os.chdir('sd')
print('SD Card contains:{}'.format(os.listdir()))

# Creamos un archivo csv y escribimos
f = open ('prueba2.csv','w')
f.write("Hora,Temperatura,Presión")
f.close()

g = open('prueba2.csv', 'r')
contenido = g.read()
print (contenido)
g.close()

t = open('prueba2.csv', 'a')
hora = '20:00:00'
temp = 22
pre = 75
t.write('\n'+hora+','+str(temp)+','+str(pre))
t.close()

g2 = open('prueba2.csv', 'r')
contenido = g2.read()
print (contenido)
g2.close()