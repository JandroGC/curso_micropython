# Ejemplo 5, temporizador con retardo a la desconexión
# Autor: Alejandro García Castro
# Febrero 2022

# Importamos las librerías necearias
from machine import Pin
import time

# Definición de una clase para crear
# objetos de tipo temporizador Toff
class Toff:
    '''
    Clase que crea un objeto de tipo Toff.
    Temporizador con retardo a la desconexion.
    
    Attributes:
        tiempo: tiempo a temporizar en ms, se inicializa con t
        salida: se activa con el temp. se mantiene activada durante "tiempo"
        contaje: valor actual de contaje en ms
        
    Methods:
        temporiza: activa salida a 1 si trg es 0. Cuando trg pasa de 0 a 1 temporiza.
                    Si activamos r el temporizador se pone a 0
    '''
    def __init__(self, t):
        self.tiempo = t
        self.salida = 0
        self.__ent_act = 1
        self.__ent_ant = 1
        self.contaje = t
        self.__inicio = 0
        self.__temp_actual = 0
        self.__disparo = False
        print('Creado objeto Toff ...')
    
    def temporiza (self, trg, r):
        '''
        Función que temporiza cuando trg = 1. Entradas con resistencias
        PULL_UP, cuando pulso pasa de 1 a 0
        
        Args:
            trg: valor de Pin o var que dispara la temporización
            r: valor de Pin o var de reset del temporizador
        '''
        self.__ent_act = trg
        self.__reset = r
        
        if self.__ent_act == 0 and self.__reset  == 1:
            self.__ent_ant = 0
            self.contaje = 0
            self.salida = 1

        elif  self.__ent_act == 1 and self.__ent_act != self.__ent_ant and self.__reset  == 1:
            self.__ent_ant = self.__ent_act
            self.__inicio = time.ticks_ms()
            self.__disparo = True
        
        elif self.__ent_act == 1 and self.__disparo == True and self.__reset  == 1:
            self.__temp_actual = time.ticks_ms()
            self.contaje = time.ticks_diff(self.__temp_actual, self.__inicio)
            #print(self.contaje)
            if self.contaje <= self.tiempo:
                self.salida = 1
            else:
                self.salida = 0
                self.contaje = 0
                self.__disparo = False
                print ('Temporización terminada')

        elif self.__reset  == 0:
            self.salida = 0
            self.contaje = 0
            self.__disparo = False
            self.__ent_act = 1
            self.__ent_ant = 1

# Hasta aquí llega la definición de la clase

# Definimos el GPIO 2 como salida y el 
# GPIO 3 como entrada PULL_UP.
led = Pin(2, Pin.OUT)
btn = Pin(18, Pin.IN, Pin.PULL_UP)
btn_r = Pin(19, Pin.IN, Pin.PULL_UP)

# Creamos un objeto de tipo Ton con un 
# valor de 2 segundos (2000 ms)
temp1 = Toff(2000)

# Creamos un bucle infinito para ejecutar
# continuamente el programa
while True:
   
    # Actualizamos continuamente la función
    # temporiza del objeto Ton
    temp1.temporiza(btn.value(), btn_r.value())

    # Actualizamos la salida con la propiedad
    # salida del objeto Ton 
    led.value(temp1.salida)