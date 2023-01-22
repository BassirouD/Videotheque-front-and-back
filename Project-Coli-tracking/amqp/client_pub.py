# !/usr/bin/env python
import pika
import time
import json

def sendInfo():
    credentials = pika.PlainCredentials('diallo', 'toor')
    parameters = pika.ConnectionParameters('10.0.3.207', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print(' [*] Sending positions. To exit press CTRL+C')
    i = 0
    data = {'id': 1, 'rue': '', 'angle': ''}
    while i < 10:
        data['rue'] = 'rue ' + str(i)
        data['angle'] = 'angle ' + str(i)
        json_data = json.dumps(data)
        # channel.queue_declare(queue='mobile')
        channel.basic_publish(exchange='',
                              routing_key='mobile',
                              body=json_data)
        time.sleep(5)
        i += 1
    connection.close()


def conSrv():
    sendInfo()
    # channel.queue_declare(queue='mobile')

    print(" [x] Process end...!'")
    # connection.close()


if __name__ == '__main__':
    conSrv()