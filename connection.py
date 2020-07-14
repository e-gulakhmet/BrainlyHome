import PyQt5.QtCore
import paho.mqtt.client as paho_mqtt
import logging
import time



class Mqtt():

    S_callback = PyQt5.QtCore.pyqtSignal(str, str, name="callBack")

    def __init__(self, broker_adress, client_id):
        self.broker_adress = broker_adress # Адресс брокера в сети
        self.client_id = client_id

        self.logger = logging.getLogger("MQTT")

        if broker_adress == "":
            self.logger.error("Broker adress is empty!")
        if client_id == "":
            self.logger.error("Client id is empty!")
        self.logger = logging.getLogger("MQTT")
        # Инициализируем клиент
        self.client = paho_mqtt.Client(self.client_id)

        # Подключаемся к событиям клиента для отладки
        self.client.on_log = self.log

        # Подключаемся к сообщенияем, которые пришли от топиков, на которые мы подписаны
        self.client.on_message = self.callback


    
    def connect(self): # Подключение к брокеру
        # Подключаемся к брокеру
        self.client.connect(self.broker_adress)
        self.client.loop_start()
        time.sleep(0.1)

    def disconnect(self): # Отключение от брокера
        # Оключаемся от брокера
        if self.client.is_connected():
            self.client.loop_stop()
            self.client.disconnect()
        else:
            self.logger.warning("Connection is broken")

    def publish(self, topic, message): # Отправка сообщения
        # Отправляем сообщение
        if (topic == ""):
            self.logger.error("Topic is empty!")
        if (message == ""):
            self.logger.error("Message is empty!")

        # Если мы подключены, то отправляем сообщение
        if self.client.is_connected():
            self.client.publish(topic, message)
        else:
            self.logger.warning("Connection is broken")

    def subscribe(self, topic): # Подписка на топик
        if self.client.is_connected():
            self.client.subscribe(topic)
        else:
            self.logger.warning("Connection is broken")

    def callback(self, client, userdata, message):
        self.S_callback.emit(str(message.topic), str(message.payload))
        
    def log(self, client, userdata, level, buf):
        self.logger.info(buf)



class Client():
    def __init__(self, id, kind, name):
        self.id = id
        self.kind = kind
        self.name = name

        self.logger = logging.getLogger("CLIENT")
    
    def get_id(self):
        return self.id

    def set_kind(seld, kind):
        if (kind == ""):
            self.logger.error("Kind is empty")
        else:
            self.kind = kind

    def get_kind(self):
        return self.kind

    def set_name(self, name):
        if (name == ""):
            self.logger.error("Name is empty")
        else:
            self.name = name
        
    def get_name(self):
        return self.name




class MqttHelper():
    def __init__(self, mqtt_service):
        self.mqtt = mqtt_service
        self.clients = []
        self.is_searching = True
        self.mqtt.subscribe()
        self.mqtt.S_callback.connect(self.on_message)
        
    def update(self):
        # TODO: Добавить команду по которой будет производится поиск новых подключений
        pass

    def get_devices(self):
        return self.clients
    
    def on_message(self, topic, message):
        if topic == "home/id":
            if message not in self.clients:
                self.clients.append(Client(message, "", ""))
                self.mqtt.subscribe("home/" + message + "/kind")
                self.mqtt.subscribe("home/" + message + "/tx")
                self.mqtt.subscribe("home/" + message + "/rx")

        for i in rande(0, len(self.clients):
            if topic == "home/" + self.clients[i].get_id() + "/kind":
                self.clients.set_kind(message)
