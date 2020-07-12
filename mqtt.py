import paho.mqtt.client as paho_mqtt
import logging



class Mqtt():
    def __init__(self, broker_adress, client_id):
        self.broker_adress = broker_adress # Адресс брокера в сети
        self.client_id = client_id
        self.logger = logging.getLogger('CLIENT')
        # Инициализируем клиент
        self.client = paho_mqtt.Client(self.client_id)
        self.logger.info("Initialized")
    
    def connect(self):
        # Подключаемся к брокеру
        self.client.connect(self.broker_adress)
        self.client.loop_start()
        self.logger.info("Connected")

    def disconnect(self):
        # Оключаемся от брокера
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Disconnected")
    
    def publish(self, topic, message):
        # Отправляем сообщение
        self.client.publish(topic, message)