#!/usr/bin/env python
import pika, os, time

def pdf_process_function(msg):
  print(" PDF processing")
  print(" [x] Received " + str(msg))

  time.sleep(5) # delays for 5 seconds
  print(" PDF process finish");
  return;

credentials = pika.PlainCredentials('diallo', 'toor')
parameters = pika.ConnectionParameters('10.0.3.207', 5672, '/',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel() # start a channel
channel.queue_declare(queue='mobile') # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  pdf_process_function(body)

# set up subscription on the queue
channel.basic_consume('mobile',
  callback,
  auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
