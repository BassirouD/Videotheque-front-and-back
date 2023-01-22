import paho.mqtt.client as paho
import sys
import time
import json

client = paho.Client()

def sendInfo():
    i = 0
    while i < 5:
        if i < 4:
            if i == 0:
                data = {'id': 2, 'location': 'UProd'}
                json_data = json.dumps(data)
                client.publish('UProd', payload=json_data)
                i += 1
                time.sleep(5)
            if i >= 1 & i <= 3:
                data = {'id': 2, 'location': 'en0' + str(i)}
                json_data = json.dumps(data)
                client.publish('en0' + str(i), payload=json_data)
                time.sleep(5)
                i += 1

        if i == 4:
            client.publish('endSession', '2')
            i += 1


def conSrvMQTT():
    if client.connect('localhost', 6000, 60) != 0:
        print('Could no connect to MQTT Borker')
        sys.exit(-1)

    sendInfo()
    client.disconnect()


if __name__ == '__main__':
    conSrvMQTT()
