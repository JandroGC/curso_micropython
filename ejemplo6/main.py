# Ejemplo 6, automatización de un husillo
# Autor: Alejandro García Castro
# Febrero 2022

# Importarmos las clases necesarias
from machine import Pin
import time
from logic import Ton, Bascula


def main():
    # Configuramos GPIO como entradas y salidas
    pin12 = Pin(12, Pin.IN, Pin.PULL_UP)
    pin25 = Pin(25, Pin.IN, Pin.PULL_UP)
    pin18 = Pin(18, Pin.IN, Pin.PULL_UP)
    pin19 = Pin(19, Pin.IN, Pin.PULL_UP)

    avance = Pin(2, Pin.OUT)
    retroceso = Pin(4, Pin.OUT)
    # Hasta aquí los GPIO

    # Instanciamos los objetos necesarios
    # Dos básculas y un temporizador
    mov_der = Bascula(0, 0)
    temp1 = Ton(2000)
    mov_izq = Bascula(0, 0)

    # Parte del programa que se repite
    while True:
        # Leemos e invertimos los pines PULL_UP de entrada
        pulsa = not pin18.value()
        termico = not pin19.value()
        fdc_der = not pin25.value()
        fdc_izq = not pin12.value()

        # Actualizamos los objetos con los valores de las variables
        mov_der.evalua(pulsa, fdc_der or termico or mov_izq.salida)
        temp1.temporiza(fdc_der)
        mov_izq.evalua(temp1.salida, fdc_izq or termico or mov_der.salida)
    
        # Actualizamos las salidas con los valores de salida de los objetos
        avance.value(not(mov_der.salida))
        retroceso.value(not(mov_izq.salida))

if __name__=="__main__":
    main()