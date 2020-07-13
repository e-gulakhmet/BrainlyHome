import paho.mqtt.client as paho_mqtt
import logging
import time



# TODO: Добавить проверку подключения перед исполнением функции



class Mqtt():
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


    
    def connect(self):
        # Подключаемся к брокеру
        self.client.connect(self.broker_adress)
        self.client.loop_start()
        time.sleep(0.1)

    def disconnect(self):
        # Оключаемся от брокера
        if self.client.is_connected():
            self.client.loop_stop()
            self.client.disconnect()
        else:
            self.logger.warning("Connection is broken")

    def publish(self, topic, message):
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
            

    def log(self, client, userdata, level, buf):
        self.logger.info(buf)
