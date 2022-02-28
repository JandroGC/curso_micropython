# Ejemplo 3, telerruptor y báscula RS 
# sin emplear interrupciones de hardware

from machine import Pin

# Definición de una clase para crear
# objetos de tipo Telerruptor
class Telerruptor:
  '''
  Crea un objeto del tipo Telerrutor que  conmuta el 
  estado de salida (sal) con un flanco positivo en la 
  entrada (ent)
  '''
  def __init__(self, ent):
    self.ent_act = ent
    self.ent_ant = 1
    self.salida = 0
  
  def conmuta(self,valor):
    '''
    Función que conmuta el estado de la 
    salida (sal) del objeto telerruptor cuando se detecta
    un flanco positivo en la variable de entrada (ent)
    '''
    self.ent_act = valor
    if  self.ent_act == 0 and self.ent_act != self.ent_ant:
      #print('Valor de la entrada ...', self.ent_act)
      if self.salida == 0:
        self.salida = 1
        self.ent_ant = self.ent_act
        #print('Conmuta a valor ...', self.sal)
      elif self.salida == 1:
        self.salida = 0
        self.ent_ant = self.ent_act
        #print('Conmuta a valor ...', self.sal)
    elif  self.ent_act == 1 and self.ent_act != self.ent_ant:
      #print('Valor de la entrada...', self.ent_act)
      self.ent_ant = self.ent_act

# Definición de una clase para crear
# objetos de tipo Bascula
class Bascula:
  def __init__(self, act, des):
    self.activa = act
    self.desactiva = des
    self.salida = 0
  
  def evalua(self, s, r):
    self.activa = s
    self.desactiva = r
    if self.desactiva == 0:
      self.salida = 0
    elif self.desactiva == 1 and self.activa == 0:
      self.salida = 1
    
# Configuramos los GPIO de la placa como 
# salidas o como entradas
p18 = Pin(18, Pin.IN, Pin.PULL_UP)
p19 = Pin(19, Pin.IN, Pin.PULL_UP)
p21 = Pin(21, Pin.IN, Pin.PULL_UP)
p02 = Pin(2, Pin.OUT)
p04 = Pin(4, Pin.OUT)

# Realizamos una instancia a la clase Telerruptor
# creando objeto tele
tele = Telerruptor(p21.value)

# Relizamos una instancia a la  clase Bascula
# creando objeto rs
rs = Bascula(p18.value(),p19.value())


while True:
  # Creamos un bucle para evaluar 
  # continuamente las entradas.
  # Actualizamos los objetos con los 
  # valores de las entradas.
  tele.conmuta(p21.value())
  rs.evalua(p18.value(), p19.value())
 
  # Pasamos el valor de las salidas del
  # correspondiente objeto a cada GPIO 
  # de salida
  p02.value(rs.salida)
  p04.value(tele.salida)