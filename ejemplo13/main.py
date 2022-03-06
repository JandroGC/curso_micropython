# Ejemplo 13, encendido de iluminacion con
# Bluetooth de baja energía (BLE)
# Bluetooth Low Energy
# Autor: Alejandro García Castro
# Marzo 2022

# Importamos las librerías necesarias
from machine import Pin, Timer
from time import sleep_ms, sleep
import ubluetooth

# Creamos una clase BLE que es la que
# gestionará la comunicacion bluetooth
# serie con el disposivo móvil, enviando
# y recibiendo mensajes.
class BLE():
    '''
        Clase BLE que conecta por BLE  la placa ESP32
        con un dispositivo móvil.
        Atributos:
            ble = objeto de tipo BLE de la librería
                  bluetooth
            led = diodo led que parpadea cuando no se
                  ha establecido conexion y pasa a
                  encendido fijo cuando está conectado
        Métodos:
            ble_irq = contiene los eventos que utilizamos
                      en el programa. Son los cuatro mensajes
                      que al ser recibidos producen cambios en
                      las salidas.
            connected = encendido fijo en led de señalizacion
                        cuando BLE está conectado
            disconnected = parpadeo en led cuando BLE desconectado
            send = envia datos a través del blutooth
            advertiser = Hace visible el nombre del dispositivo para
                         poder ser identificado.
            register =  maneja los registros necesarios para la
                        comunicación
    '''

    def __init__(self, name):
        print('se ha creado objeto BLE')
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
       
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''Nuevo mensaje recibido'''            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)            
            if message == 'luz1':
                luz1.value(not luz1.value())
                print('Luz 1...', luz1.value())
                ble.send('Luz 1...' + str(luz1.value()))
            if message == 'luz2':
                luz2.value(not luz2.value())
                print('Luz 2...', luz2.value())
                ble.send('Luz 2...' + str(luz2.value()))
            if message == 'luz3':
                luz3.value(not luz3.value())
                print('Luz 3...', luz3.value())
                ble.send('Luz 3...' + str(luz3.value()))
            if message == 'luz4':
                luz4.value(not luz4.value())
                print('Luz 4...', luz4.value())
                ble.send('Luz 4...' + str(luz4.value()))
                
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        
# Prueba

# Definimos los pines para las salidas
# en las que están conectados los relés
luz1 = Pin(12, Pin.OUT)
luz2 = Pin(14, Pin.OUT)
luz3 = Pin(27, Pin.OUT)
luz4 = Pin(26, Pin.OUT)

# Creamos el objeto de tipo BLE
# que al funcionar por interrupciones
# estará continuamente escuchando
ble = BLE("ESP32")

while True:
    print ('Bluetooth')
    sleep(5)