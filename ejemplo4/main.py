# Ejemplo 4, temporizador con retardo a la conexión
# Autor: Alejandro García Castro
# Febrero 2021

# Importamos las librerías necearias
from machine import Pin
import time

# Definición de una clase para crear
# objetos de tipo temporizador
class Ton:
    '''
    Clase que crea un objeto de tipo Ton, temporizador con
    retardo a la conexion de entrada mantenida.
    
    Atributos:
        tiempo: tiempo a temporizar en ms, se inicializa con t
        salida: se activa cuando transcurre el tiempo
        contaje: valor actual de contaje en ms
        
    Métodos:
        temporiza: lanza la temporización
    '''
    def __init__(self, t):
        self.tiempo = t
        self.salida = 0
        self.__ent_act = 1
        self.__ent_ant = 1
        self.contaje = 0
        self.__inicio = 0
        self.__temp_actual = 0
        print('Creado objeto TON ...')
    
    def temporiza (self, trg):
        '''
        Función que temporiza cuando trg = 0
        
        Args:
            trg: valor de Pin o var que dispara la temporización
        '''
        self.__ent_act = trg
        
        if  self.__ent_act == 0 and self.__ent_act != self.__ent_ant:
            self.__ent_ant = self.__ent_act
            self.__inicio = time.ticks_ms()
        elif  self.__ent_act == 1 and self.__ent_act != self.__ent_ant:
            self.__ent_ant = self.__ent_act
            self.salida = 0
            self.contaje = 0
            self.__inicio = 0
        
        elif self.__ent_act == 0:
            self.__temp_actual = time.ticks_ms()
            self.contaje = time.ticks_diff(self.__temp_actual, self.__inicio)
            if self.contaje >= self.tiempo:
                self.salida = 1

# Hasta aquí llega la definición de la clase

# Definimos el GPIO 2 como salida y el 
# GPIO 3 como entrada PULL_UP.
led = Pin(2, Pin.OUT)
btn = Pin(18, Pin.IN, Pin.PULL_UP)

# Creamos un objeto de tipo Ton con un 
# valor de 2 segundos (2000 ms)
temp1 = Ton(2000)

# Creamos un bucle infinito para ejecutar
# continuamente el programa
while True:
    # Actualizamos continuamente la función
    # temporiza del objeto Ton
    temp1.temporiza(btn.value())

    # Actualizamos la salida con la propiedad
    # salida del objeto Ton 
    led.value(temp1.salida)