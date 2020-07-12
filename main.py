import connection
import logging


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] : %(message)s")

    print("BrainlyHome")
    mqtt = connection.Mqtt("192.168.1.112", "base")

    mqtt.connect()
    mqtt.publish("base/test", "hello world")
    mqtt.disconnect()
    



if __name__ == "__main__":
    main()
