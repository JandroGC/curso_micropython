# Ejemplo 8, texto  que recorre la pantalla
# de arriba a abajo
# Autor: Alejandro García Castro
# Febrero 2022

# Importamos las clases y librerías 
from machine import Pin, SoftI2C
import ssd1306
from time import sleep_ms

# Asignamos los pines I2C para el ESP32 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Definimos dimensiones del la pantalla
# y creamos el objeto correspondiente
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Borramos la pantalla
oled.fill(0) 
x= 0
while x <= 50:
    oled.text('Viva Juan Bosco', 0, x)
    # Mostramos el texto con show()
    oled.show() 
    sleep_ms(50)
    oled.fill(0)
    x = x + 1

oled.fill(0)
oled.show()