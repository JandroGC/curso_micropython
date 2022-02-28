# Clase que sincroniza el reloj RTC del ESP32
# a la hora de España conectándose al servidor
# de la Marina Española: "hora.roa.es".
# La hora se corrige al horario de invierno_verano.
# 
# Autor: Alejandro García Castro
# Fecha: Febrero 2022

import network, ntptime # importamos las librerías necesarios
from machine import RTC # import RTC desde machine
import time             # Para usar localtime

class MyRTC:
    '''
     Esta es la versión 2 de la libreria MyRTC. En esta
     version se sincroniza realmente el RTC
     
     Atributos:
        corrector: horas de desfase respecto a UTC
        
     Métodos:
        sincro: sincroniza RTC con hora.es y lo corrige
                automáticamente a hora local española
                según horario invierno-verano
    '''
    
    def __init__(self, ssid_user, password_user):
        self.__ssid = ssid_user
        self.__passw = password_user
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.corrector = 0
        self.__datetime = []
        print('Se ha creado objeto MyRTC')
        
    def connect_to_wifi(self):
        if not self.wlan.isconnected():
            print("Conectando a la red ...")
            self.wlan.connect(self.__ssid, self.__passw)
            while not self.wlan.isconnected():
                pass
            
    def sincro(self):
        self.connect_to_wifi()
        # Inicilizamos el RTC
        rtc = RTC()
        # Indicamos el nombre del servidor: Marina Española
        ntptime.localhost = "hora.roa.es"
        # Hacemos un set del RTC con el valor del servidor
        ntptime.settime()
        print ('RTC sincronizado roa: ', rtc.datetime())
        
        self.mi_fecha = time.localtime()
        
        # El mes es anterior a MARZO o posterior a OCTUBRE
        # estamos dentro del horario de invierno sumaremos
        # una hora , o 1 segundos
        if self.mi_fecha[1] < 3 or self.mi_fecha[1] > 10:
            self.corrector = 1
        
        # Mes de MARZO y día anterior al 25
        # estamos dentro del horario de invierno sumaremos
        # una hora , o 1 segundos
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] < 25:
            self.corrector = 1
    
        # Mes de MARZO , día 25
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 25:
            # Día de la semana no es domingo
            # estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5: 
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
    
        # Mes de MARZO , día 26
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 26:
            # Día de la semana no es domingo ni lunes
            # estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 0:
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes y deberíamos 
            # sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
    
        # Mes de MARZO, día    27
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 27:
            # El día de la semana no es  lunes, martes ni domingo
            # estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 1:
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes o martes, y deberíamos
            # sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
    
        # Mes de MARZO, día    28
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 28:
            # El día de la semana no es  lunes, martes, miércoles
            # ni domingo, estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 2:
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes, martes o miercoles,
            # y deberíamos sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
   
        # Mes de MARZO, día    29
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 29:
            # El día de la semana no es  lunes, martes, miércoles
            # jueves, ni domingo, estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 3:
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes, martes, miercoles o
            # o jueves y deberíamos sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
    
        # Mes de MARZO, día    30
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 30:
            # El día de la semana es sábado
            # estamos todavía en horario de invierno
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 4:
                self.corrector = 1
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes, martes, miercoles, jueves
            # o viernes y deberíamos sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
    
        # Mes de MARZO, día 31
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 31:
            # Si es domingo y la hora está por debajo
            # de la una , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de verano, y sumamos 2 segundos (2 horas).
            if self.mi_fecha[6] == 6:
                if self.mi_fecha[3] == 0:
                    self.corrector = 1
                else:
                    self.corrector = 2
            # En otro caso sería lunes, martes, miercoles, jueves
            # viernes o sábado y deberíamos sumar 2 segundos (2 horas)
            else:
                self.corrector = 2
    
        # ***** Cambio de hora en octubre
        # Mes de OCTUBRE y día anterior al 25
        # estamos dentro del horario de VERANO sumaremos
        # dos horas , o 2 segundos
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] < 25:
            self.corrector = 2
    
        # Mes de OCTUBRE , día 25
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 25:
            # Día de la semana no es domingo
            # estamos todavía en horario de VERANO
            if self.mi_fecha[6] <=5: 
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos, estamos en horario de verano
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
    
        # Mes de OCTUBRE , día 26
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 26:
            # Día de la semana no es domingo ni lunes
            # estamos todavía en horario de VERANO
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 0:
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos , estamos en horario de VERANO
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes y deberíamos 
            # sumar 1 segundos (1 hora)
            else:
                self.corrector = 1
    
        # Mes de OCTUBRE, día    27
        elif self.mi_fecha[1] == 3 and self.mi_fecha[2] == 27:
            # El día de la semana no es  lunes, martes ni domingo
             # estamos todavía en horario de VERANO
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 1:
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos, estamos en horario de verano
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes o martes, y deberíamos
            # sumar 1 segundos (1 hora)
            else:
                self.corrector = 1
    
        # Mes de OCTUBRE, día    28
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 28:
            # El día de la semana no es  lunes, martes, miércoles
            # ni domingo, estamos todavía en horario de VERANO
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 2:
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos , estamos en horario de verano
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes, martes o miercoles,
            # y deberíamos sumar 2 segundos (2 horas)
            else:
                self.corrector = 1
            
        # Mes de OCTUBRE, día    29
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 29:
            # El día de la semana no es  lunes, martes, miércoles
            # jueves, ni domingo, estamos todavía en horario de VERABI
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 3:
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos , estamos en horario de verano
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes, martes, miercoles o
            # o jueves y deberíamos sumar 1 segundos (1 hora)
            else:
                self.corrector = 1
    
        # Mes de OCTUBRE, día    30
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 30:
            # El día de la semana es sábado
            # estamos todavía en horario de VERANO
            if self.mi_fecha[6] <=5 and self.mi_fecha[6] > 4:
                self.corrector = 2
            # Si es domingo y la hora está por debajo
            # de las dos , estamos en horario de invierno
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            elif self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes, martes, miercoles, jueves
            # o viernes y deberíamos sumar 1 segundos (1 hora)
            else:
                self.corrector = 1
   
       # Mes de OCTUBRE, día 31
        elif self.mi_fecha[1] == 10 and self.mi_fecha[2] == 31:
            # Si es domingo y la hora está por debajo
            # de las dos , estamos en horario de VERANO
            # en caso contrario ya estaremos en horario
            # de invierno, y sumamos 1 segundos (1 hora).
            if self.mi_fecha[6] == 6:
                if self.mi_fecha[3] <= 1:
                    self.corrector = 2
                else:
                    self.corrector = 1
            # En otro caso sería lunes, martes, miercoles, jueves
            # viernes o sábado y deberíamos sumar 1 segundos (1 hora)
            else:
                self.corrector = 1
        else:
            self.corrector = 2
        
        
        # Pasamos RTC a lista
        self.__datetime = list(rtc.datetime())
        # Sumamos las horas por zona a la hora de la lista RTC
        self.__datetime[4]=self.__datetime[4]+self.corrector
        # Pasamos la lista a tupla
        self.__datetime = tuple(self.__datetime)
        # Actualizamos el RTC
        rtc.datetime(self.__datetime)
        
     
        
        
        
        
        
    
    