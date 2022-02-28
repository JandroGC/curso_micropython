# Ejemplo 2, telerruptor mediante interrupciones
# Autor: Alejandro García Castro
# Febrero 2022

# Importamos Pin y sleep
from machine import Pin
from time import sleep

# Definimos la rutina de interrupción.
# Esta función es la denominada handler
# contiene el código que se ejecuta en la 
# interrupción.
def rutina_int(pin):
    print('INTERUPPCIÓN!!')
    if led.value() == 0:
        led.on()
    else:
        led.off()

# Definimos el GPIO 2 como salida y el 
# GPIO 3 como entrada PULL_UP.
led = Pin(2, Pin.OUT)
btn = Pin(4, Pin.IN, Pin.PULL_UP)

# Definimos la interrupcón en el pulsador btn que se 
# produce cuando éste pasa de 1 a 0 (IRQ_FALLING)
btn.irq(trigger=Pin.IRQ_FALLING, handler=rutina_int)

# Apagamos el led incialmente.
led.off()

# Creamos un bucle infinito para
# que se ejecute continuamente
while True:
    print ('*')
    sleep(1)