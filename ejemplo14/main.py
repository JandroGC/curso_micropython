# Ejemplo 14, publicacion de valores de un
# sensor en Thinspeak para su análisis
#
# Autor: Alejandro García Castro
# basado en programa de:
# George Bantique 
# TechToTinker Youtube Channel  
# TechToTinker.blogspot.com

# Importamos la librerías necesarias
import machine
import network
from umqtt.simple import MQTTClient
import dht
import time

# Definimos variables para conexión
wifi_ssdi = 'ssid_wifi'
wifi_pass = 'password'

# Función que nos conecta al WIFI
def connect_wifi():
    if not sta.isconnected():
        print('conectando a la red...')
        sta.active(True)
        sta.connect(wifi_ssdi, wifi_pass)
        while not sta.isconnected():
            pass
    print('Configuración de red: ', sta.ifconfig())


# Creamos objetos necesarios
led = machine.Pin(2,machine.Pin.OUT)
d = dht.DHT11(machine.Pin(23))

# Configuramos ESP32 como Station
# y lo conectamos al wifi
sta = network.WLAN(network.STA_IF)
connect_wifi()



# Variables y constantes globales para MQTT
SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)
CHANNEL_ID = "1667---"
WRITE_API_KEY = "KX0VAIBN3UF1R---"
# topic = "channels/1667943/publish/KX0VAIBN3UF1R01E"
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY
UPDATE_TIME_INTERVAL = 10000 # in ms unit
last_update = time.ticks_ms()

# Bucle principal del programa
while True:
    # Si perdemos la conexión intentamos
    # conectar de nuevo
    if not sta.isconnected():
        print('Wifi desconectado ...')
        sta.disconnect()
        connect_wifi()
    # Si estamos conectados tomamos lecturas cada
    # cierto tiempo del sensor DHT11 y las publicamos 
    # en el servidor MQTT
    if sta.isconnected():
        if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
            d.measure()
            t = d.temperature()
            h = d.humidity()
    
            payload = "field1={}&field2={}" .format(str(t), str(h))

            client.connect()
            client.publish(topic, payload)
            client.disconnect()

            print(payload)
            led.value(not led.value())
            last_update = time.ticks_ms()
        
        