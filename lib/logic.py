# Archivo logic, contiene las clases necesarias
# para utilizar funciones lógicas similares a las
# de un relé programable
# Autor: Alejandro García Castro
# Febrero de 2022

from machine import Pin
import time


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
        self.__ent_act = 0
        self.__ent_ant = 0
        self.contaje = 0
        self.__inicio = 0
        self.__temp_actual = 0
        print('Creado objeto TON ...')
    
    def temporiza (self, trg):
        '''
        Función que temporiza cuando trg = 1
        
        Args:
            trg: valor de Pin o var que dispara la temporización
        '''
        self.__ent_act = trg
        
        if  self.__ent_act == 1 and self.__ent_act != self.__ent_ant:
            self.__ent_ant = self.__ent_act
            self.__inicio = time.ticks_ms()
        elif  self.__ent_act == 0 and self.__ent_act != self.__ent_ant:
            self.__ent_ant = self.__ent_act
            self.salida = 0
            self.contaje = 0
            self.__inicio = 0
        
        elif self.__ent_act == 1:
            self.__temp_actual = time.ticks_ms()
            self.contaje = time.ticks_diff(self.__temp_actual, self.__inicio)
            if self.contaje >= self.tiempo:
                self.salida = 1

class Toff:
    '''
    Clase que crea un objeto de tipo Toff.
    Temporizador con retardo a la desconexion.
    
    Attributes:
        tiempo: tiempo a temporizar en ms, se inicializa con t
        salida: se activa con el temp. se mantiene activada durante "tiempo"
        contaje: valor actual de contaje en ms
        
    Methods:
        temporiza: activa salida a 1 si trg es 1. Cuando trg pasa de 1 a 0 temporiza.
                    Si activamos r el temporizador se pone a 0
    '''
    def __init__(self, t):
        self.tiempo = t
        self.salida = 0
        self.__ent_act = 0
        self.__ent_ant = 0
        self.contaje = t
        self.__inicio = 0
        self.__temp_actual = 0
        self.__disparo = False
        print('Creado objeto Toff ...')
    
    def temporiza (self, trg, r):
        '''
        Función que temporiza cuando trg pasa de 1 a 0
        
        Args:
            trg: valor de Pin o var que dispara la temporización
            r: valor de Pin o var de reset del temporizador
        '''
        self.__ent_act = trg
        self.__reset = r
        
        if self.__ent_act == 1 and self.__reset  == 0:
            self.__ent_ant = 1
            self.contaje = 0
            self.salida = 1

        elif  self.__ent_act == 0 and self.__ent_act != self.__ent_ant and self.__reset  == 0:
            self.__ent_ant = self.__ent_act
            self.__inicio = time.ticks_ms()
            self.__disparo = True
        
        elif self.__ent_act == 0 and self.__disparo == True and self.__reset  == 0:
            self.__temp_actual = time.ticks_ms()
            self.contaje = time.ticks_diff(self.__temp_actual, self.__inicio)
            if self.contaje <= self.tiempo:
                self.salida = 1
            else:
                self.salida = 0
                self.contaje = 0
                self.__disparo = False
                print ('Temporización terminada')

        elif self.__reset  == 1:
            self.salida = 0
            self.contaje = 0
            self.__disparo = False
            self.__ent_act = 0
            self.__ent_ant = 0

class Telerruptor:
    '''
    Crea un objeto del tipo Telerrutor que  conmuta el 
    estado de salida  con un flanco positivo en la 
    entrada (trg)
  
    Atributos:
        ent_act: valor de la entrada actual se inicializa  con trg
        salida: se activa o desactiva con flanco - en entrada
      
    Métodos:
        conmuta: conmuta salida cuando "trg" cambia de 1 a 0
      
    '''
    def __init__(self, trg):
        self.ent_act = trg
        self.__ent_ant = 0
        self.salida = 0
        print('Creado un telerruptor')
  
    def conmuta(self,trg):
        '''
        Función que conmuta el estado de la 
        salida  del objeto telerruptor cuando se detecta
        un flanco negativo en la variable de entrada "trg"
    
        Args:
            trg: valor del Pin o variable que hace conmutar
        '''
        self.ent_act = trg
        if  self.ent_act == 1 and self.ent_act != self.__ent_ant:
            if self.salida == 0:
                self.salida = 1
                self.__ent_ant = self.ent_act
            elif self.salida == 0:
                self.salida = 1
                self.__ent_ant = self.ent_act
        elif  self.ent_act == 0 and self.ent_act != self.__ent_ant:
                self.__ent_ant = self.ent_act


class Bascula:
    '''
    Crea un objeto del tipo Bascula (RS) que  pone a 1 la "salida"
    con el estado 1 de "activa" y a 0 con el estado 1 de
    "desactiva".
  
    Atributos:
        activa: entrado de activacion o SET
        desactiva: entrada de desactivacion o RESET
        salida: salida del bloque lógico
      
    Métodos:
        evalua: actualiza el valor de "salida " con act y des
      
    '''
    def __init__(self, activa, desactiva):
        self.activa = activa
        self.desactiva = desactiva
        self.salida = 0
        print('Creado un objeto tipo Bascula')
  
    def evalua(self, activa, desactiva):
        '''
        Función que activa la salida con el flanco + en "act"
        y la desactiva con un flanco + en "des"
    
        Args:
            act: valor del Pin o variable de SET o activación
            des: valor del Pin o variable de RESET o desactivacion
        '''
        self.activa = activa
        self.desactiva = desactiva
        if self.desactiva == 1:
            self.salida = 0
        elif self.desactiva == 0 and self.activa == 1:
            self.salida = 1