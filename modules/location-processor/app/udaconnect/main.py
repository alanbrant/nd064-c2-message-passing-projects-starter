import time
from concurrent import futures

from kafka import KafkaConsumer
from sqlalchemy import create_engine
import json
import os

TOPIC_NAME = 'locations'
consumer = KafkaConsumer(TOPIC_NAME)

def get_messages():
        for message in consumer:
            json_message = json.loads(message)
            print (message)

            DB_USERNAME = os.environ["DB_USERNAME"]
            DB_PASSWORD = os.environ["DB_PASSWORD"]
            DB_HOST = os.environ["DB_HOST"]
            DB_PORT = os.environ["DB_PORT"]
            DB_NAME = os.environ["DB_NAME"]

            engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
            conn = engine.connect()

            person_id = int(json_message["userId"])
            latitude, longitude = int(json_message["latitude"]), int(json_message["longitude"])

            insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)

            conn.execute(insert)

get_messages()