# curso_micropython
Breve curso de Micropython, ejemplos de programación con ESP32 MicroPython. 

Los ejemplos están publicados en  "Cuadernos de Automatización. Microcontrolador ESP32". Todos ellos han sido probados en una placa ESP32-WROOM32.
La lista de ejemplos es la siguiente:

- Ejemplo 1, encendido de un LED con pulsador
- Ejemplo 2, telerruptor mediante interrupciones
- Ejemplo 3, telerruptor y báscula RS
- Ejemplo 4, temporizador con retardo a la conexión
- Ejemplo 5, temporizador con retardo a la desconexión
- Ejemplo 6, automatización de un husillo
- Ejemplo 7, lectura de valores analógicos
- Ejemplo 8, texto que recorre la pantalla
- Ejemplo 9, uso de un encoder mecánico KY-040
- Ejemplo 10, control de un motor DC mediante PWM
- Ejemplo 11, mantemos sincronizado el RTC y los mostramos en pantalla
- Ejemplo 12, log de un sensor DHT11 en una tarjeta SD
- Ejemplo 13, encendido de iluminación por Bluetooth
- Ejemmplo 14, envío de datos a un servidor IoT (Internet of Things)

En la carpeta ***/lib*** se encuentran  las librería empleadas en los ejemplos. Las librerías *logic.py* y *mi_RTC.py* son propias del autor. Deberán cargarse en la memoria del microcontrolador ESP32 las librerias necesarias en cada caso. Se incluyen librerías de otros autores, también. Los enlaces son los siguientes:

- GitHub de Damien George con drivers para utilizar en la ESP32 con diferentes componentes. Entre ellos está el de la pantalla OLED, la tarjeta SD o el DHT11: [https://github.com/micropython/micropython-esp32](https://github.com/micropython/micropython-esp32) 

- GitHub de Mike Teachman que contiene las librerías para trabajar con el encoder mecánico: [https://github.com/miketeachman/micropython-rotary](https://github.com/miketeachman/micropython-rotary)

- GitHub de Robert Hammelrath  que contine la librería para trabajar con la tarjeta SD: [https://github.com/micropython/micropython/blob/master/drivers/sdcard/sdcard.py](https://github.com/micropython/micropython/blob/master/drivers/sdcard/sdcard.py)
