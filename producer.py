#!/usr/bin/env python
import cv2
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='stream')

vc = cv2.VideoCapture(0)
while True:
    ret, frame = vc.read()
    if not ret:
        print("failed to grab frame")
        break
    im = cv2.imencode('.jpg', frame)[1].tobytes()
    channel.basic_publish(
        exchange = '', routing_key = 'stream', body = im)

connection.close()

