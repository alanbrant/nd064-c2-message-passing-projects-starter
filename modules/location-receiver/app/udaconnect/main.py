import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer




class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Create(self, request, context):
        print("Received a message!")

        location = {
            "person_id": request.person_id,
            "lat": request.lat,
            "long": request.long
        }
        print("send to kafka" + location)

        TOPIC_NAME = 'locations'
        KAFKA_SERVER = 'kafka:9092'

        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        producer.send(TOPIC_NAME, location)
        producer.flush()

        return location_pb2.OrderMessage(**location)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)