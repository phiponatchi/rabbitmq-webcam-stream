#!/usr/bin/env python
import time

import cv2
import pika


def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='webcam', exchange_type='fanout')
    return connection, channel

def stream_webcam(channel, fps=30, quality=70):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    frame_interval = 1 / fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

            channel.basic_publish(
                exchange='webcam',
                routing_key='',
                body=buffer.tobytes(),
                properties=pika.BasicProperties(
                    content_type='application/octet-stream',
                    delivery_mode=1  # non-persistent, no disk write
                )
            )

            time.sleep(frame_interval)
    finally:
        cap.release()

if __name__ == '__main__':
    connection, channel = create_connection()
    try:
        stream_webcam(channel)
    finally:
        connection.close()