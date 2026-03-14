import os
import sys

import cv2
import numpy as np
import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='stream')

    def callback(ch, method, properties, body):
        nparr = np.frombuffer(body, np.uint8)
        newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # processing and streaming
        cv2.imshow("webcam", newFrame)
        cv2.waitKey(1)

    channel.basic_consume(queue='stream', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)