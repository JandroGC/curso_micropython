# Ejemplo 10 , uso de encoder mecánico KY-040
# para el control de un motor DC mediante PWM
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
# de encoder. Importamos también la librería para
# gestionar la pantalla OLED.
import time
from rotary_irq_esp import RotaryIRQ
from machine import Pin, PWM, SoftI2C
import ssd1306


# Asignamos los pines I2C para el ESP32
# en los que conectaremos la pantalla OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Definimos dimensiones del la pantalla OLED
# y creamos el objeto correspondiente.
# Borramos la pantalla
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0) 

# Este es le constructor de la clase RotaryIRQ
# para el encoder
r = RotaryIRQ(pin_num_clk=35, 
              pin_num_dt=32, 
              min_val=0, 
              max_val=10, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_BOUNDED)
            
val_old = r.value()

# Definimos los pines para control del motor
pwm12 = PWM(Pin(12), freq=100, duty=0)
cw = Pin(14, Pin.OUT)
ccw = Pin(27, Pin.OUT)
ciclo = 0

# Bucle de repetición del programa
while True:
    
    # Consultamos el encoder
    val_new = r.value()
    
    if val_old != val_new and val_new !=0:
        val_old = val_new
        ciclo = val_new * 100
        velocidad = val_new * 10
        oled.fill(0)
        oled.text('Velocidad :', 5, 5)
        oled.text(str(velocidad), 5, 15)
        oled.show()
        cw.on()
        ccw.off()
        
    elif val_new == 0:
        oled.fill(0)
        oled.text('MOTOR PARADO', 5, 5)
        oled.show()
        pwm12.duty(0)
        cw.off()
        ccw.off()
        
    pwm12.duty(ciclo)
        
    time.sleep_ms(50)