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
        self.S_callback.emit(str(message.topic), str(message.payload))
        self.logger.info("new message came: [" + str(message.topic) + "] " + str(message.payload))
        
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
        self.mqtt.subscribe("home/id")
        self.mqtt.S_callback.connect(self.on_message)
        self.logger = logging.getLogger("MQTTHELPER")



    def get_devices(self): # Получить всех клиентов
        self.logger.info(str(len(self.clients)) + " client connected")
        return self.clients
    
    def on_message(self, topic, message): # Функция нахождения новых клиентов
        new_client = True
        if topic == "home/id":
            # Проходимся по каждому из клиентов
            for client in self.clients:
                # Если нашли одинаковые номера
                # Говорим, что новый пользователь не добаляется
                # и выходим из функции
                if message == client.get_id():
                    self.logger.info("Client is already connected")
                    new_client = False
                    return
            # Если совпадения не были найдены, 
            # то добавляем нового клиента и подключаемся к его топикам
            self.clients.append(home.Client(message, ""))
            self.mqtt.subscribe("home/" + message + "/kind")
            self.mqtt.subscribe("home/" + message + "/tx")
            self.mqtt.subscribe("home/" + message + "/rx")
            self.logger.info("New client was found")
        else:
            new_client = False

        # Если новый клиент был добавлен 
        # и пришло сообщение на топик нового клиента
        if new_client and topic == "home/" + self.clients[len(self.clients) - 1].get_id() + "/kind":
            # Указываем тип для него
            self.clients[len(self.clients) - 1].set_kind(message)
            self.logger.info("The type " + message + " for the new client has been set")
            return

    def delete_device(self, id): # Удалить клиента
        for i in range(0, len(self.clients)):
            if (id == self.clients[i].get_id()):
                self.clients.pop(i)
                self.logger.info("Client was deleted")
