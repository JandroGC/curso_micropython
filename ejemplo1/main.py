# Ejemplo 1, encendido de un led con pulsador
# Autor: Alejandro García Castro
# Febrero 2022

# Importamos la clase Pin
from machine import Pin

# Definimos el GPIO 2 como salida y el 
# GPIO 3 como entrada PULL_UP
led = Pin(2, Pin.OUT)
btn = Pin(4, Pin.IN, Pin.PULL_UP)

# Creamos un bucle infinito para ejecutar
# continuamente el programa
while True:
    # Si pulsamos se pone a cero y 
    # encendemos el led. En caso contrario
    # el led permanece apagado.
    if btn.value()==0:
        led.on()
    else:
        led.off()