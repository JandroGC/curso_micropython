# Ejemplo 7 , lectura de valores analógicos
# Autor: Alejandro García Castro
# Febrero 2022

# Importamos las clases necesarias
from machine import ADC, Pin
from time import sleep

# Definimos los GPIO y los ADC a
# emplear para los potenciómetros.
# Indicamos la atenuacion.
pin32 = Pin(32) 
pin33 = Pin(33)
adc32 = ADC(pin32)
adc32.atten(ADC.ATTN_11DB)
adc33 = ADC(pin33)
adc33.atten(ADC.ATTN_11DB)

# Creamos un bucle para leer e imprimir
# los valores que de los potenciómetros
while True:
    valor1 = adc32.read_u16()
    valor2 = adc33.read_u16()
    print(valor1, " - ", valor2)
    # Detenemos el programa durante 1 segundo
    # para poder observar lo valores por consola.
    sleep(1)