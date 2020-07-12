import paho.mqtt.client as paho_mqtt
import logging
import time



# TODO: Добавить проверку подключения перед исполнением функции



class Mqtt():
    def __init__(self, broker_adress, client_id):
        self.broker_adress = broker_adress # Адресс брокера в сети
        self.client_id = client_id

        self.logger = logging.getLogger('CLIENT')
        # Инициализируем клиент
        self.client = paho_mqtt.Client(self.client_id)

        # Подключаемся к событиям клиента для отладки
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish


    
    def connect(self):
        # Подключаемся к брокеру
        self.logger.info("Connecting...")
        self.client.connect(self.broker_adress)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected")



    def disconnect(self):
        # Оключаемся от брокера
        if self.client.is_connected() is True:
            self.logger.info("Disconnecting...")
            self.client.loop_stop()
            self.client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        self.logger.info("Disconnected")

    

    def publish(self, topic, message):
        # Отправляем сообщение
        if self.client.is_connected():
            self.logger.info("Publishing{Topic: " + topic + ", Message: " + message + "}...")
            self.client.publish(topic, message)

    def on_publish(self, client, userdata, mid):
        self.logger.info("Published")