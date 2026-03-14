#!/usr/bin/env python

import cv2
import numpy as np
import pika


def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='webcam', exchange_type='fanout')
    return connection, channel

def on_frame(ch, method, properties, body):
    nparr = np.frombuffer(body, np.uint8)
    newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # processing and streaming
    cv2.imshow("webcam", newFrame)
    cv2.waitKey(1)

def start_consumer(channel):
    # exclusive=True — queue is deleted when consumer disconnects
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='webcam', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=on_frame, auto_ack=True)

    print("Waiting for frames...")
    channel.start_consuming()

if __name__ == '__main__':
    connection, channel = create_connection()
    try:
        start_consumer(channel)
    except KeyboardInterrupt:
        connection.close()