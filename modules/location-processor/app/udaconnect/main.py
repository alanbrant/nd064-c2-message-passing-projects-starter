import time
from concurrent import futures

from kafka import KafkaConsumer


TOPIC_NAME = 'items'

consumer = KafkaConsumer(TOPIC_NAME)


def get_messages():
        for message in consumer:
            print (message)




get_messages()