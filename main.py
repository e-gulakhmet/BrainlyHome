import logging

import connection



def main():
    logging.basicConfig(filename="brainlyhome.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    mqtt = connection.Mqtt("192.168.1.112", "base")
    mqtt.connect()
    mqtt.publish("base/test", "hello world")
    mqtt.disconnect()
    
    mqtt_helper = connection.MqttHelper(mqtt)
    mqtt_helper.update()
    clients = mqtt_helper.get_devices()
    print(clients[0].get_name())



if __name__ == "__main__":
    main()
