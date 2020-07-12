import logging
import time

import mqtt



def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s : %(message)s")

    print("BrainlyHome")
    client = mqtt.Mqtt("192.168.1.112", "base")
    client.connect()
    client.publish("base/test", "hello world")
    client.disconnect()    



if __name__ == "__main__":
    main()
