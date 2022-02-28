# Ejemplo 9 , uso de encoder mecánico KY-040
# Alejandro García Castro
# con la librería de Mike Teachman
# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

# Primero importamos la libreria time  y la clase
# rotary_irq_esp necesaria para gestionar el encoder.
# Nos ayudará  a evitar los rebotes en la conmutacion
# de encoder.
import time
from rotary_irq_esp import RotaryIRQ

# Este es le constructor de la clase RotaryIRQ
r = RotaryIRQ(pin_num_clk=35, 
              pin_num_dt=32, 
              min_val=0, 
              max_val=10, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_BOUNDED)
              
val_old = r.value()

# Bucle de repetición del programa
while True:
    # Consultamos el objeto encoder creado
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('resultado =', val_new)
        
    time.sleep_ms(50)