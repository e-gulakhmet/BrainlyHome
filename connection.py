import PyQt5.QtCore
import paho.mqtt.client as paho_mqtt
import logging
import time

import home



class Mqtt(PyQt5.QtCore.QObject):

    S_callback = PyQt5.QtCore.pyqtSignal(str, str, name="callBack")

    def __init__(self, broker_adress, client_id):
        super().__init__()
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
        self.client.on_message = self.on_message


    
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
        
    def unsubscribe(self, topic):
        if self.client.is_connected():
            self.client.unsubscribe(topic)
        else:
            self.logger.warning("Connection is broken")


    def on_message(self, client, userdata, message): # Функция, которая переотправляет сообщения в сигна
        payload = message.payload.decode("utf-8")
        self.S_callback.emit(str(message.topic), payload)
        self.logger.info("new message came: [" + str(message.topic) + "] " + payload)
        
    def log(self, client, userdata, level, buf):
        self.logger.info(buf)



class MqttHelper(PyQt5.QtCore.QObject):
    """

    Класс вспомогательных функций для MQTT.
    Здесь происходит поиск и инициализация новых клиентов.

    При нахождении новых клиетов, задаем им номер и тип,
    исходя из данный, которые они прислали.

    """

    def __init__(self, mqtt_service):
        super().__init__()
        self.mqtt = mqtt_service
        self.clients = []
        self.mqtt.subscribe("home/client")
        self.mqtt.S_callback.connect(self.on_message)
        self.logger = logging.getLogger("MQTTHELPER")



    def get_devices(self): # Получить всех клиентов
        self.logger.info(str(len(self.clients)) + " client connected")
        return self.clients
    
    def on_message(self, topic, message: str): # Функция нахождения новых клиентов
        if topic == "home/client":
            # Проходимся по каждому из клиентов
            for client in self.clients:
                # Если нашли одинаковые номера
                # Говорим, что новый пользователь не добаляется
                # и выходим из функции
                if message == client.get_id():
                    self.logger.info("Client is already connected")
                    return
            # Если совпадения не были найдены, 
            # то добавляем нового клиента и подключаемся к его топикам
            # Разделяем сообщение по знаку ';',
            # первым элементом будет id,
            # вторым будет type(kind)
            client_info = message.split(';')
            self.clients.append(home.Client(client_info[0], client_info[1]))
            self.mqtt.subscribe("home/" + client_info[0] + "/tx")
            self.mqtt.subscribe("home/" + client_info[0] + "/rx")
            self.logger.info("New client [" + client_info[0] + "] - " + client_info[1] + " was found")

    def delete_device(self, id): # Удалить клиента
        for i in range(0, len(self.clients)):
            if (id == self.clients[i].get_id()):
                self.clients.pop(i)
                self.logger.info("Client was deleted")
