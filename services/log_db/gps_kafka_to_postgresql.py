from kafka import KafkaConsumer
import psycopg2
import os
import json  # Assuming the Kafka message payload is JSON formatted

# Environment variables
#BROKER_IP = os.getenv("BROKER_IP", "127.0.0.1")

#KAFKA_BROKERS = [f'{BROKER_IP}:9092', f'{BROKER_IP}:9094', f'{BROKER_IP}:9096']

KAFKA_BROKERS = os.getenv("BROKER", "").split(",")
KAFKA_TOPICS = 'gps_raw'
KAFKA_GROUP_ID = "gps_group_gps_raw"

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

print("Kafka Brokers:", KAFKA_BROKERS)


# Table schema (for reference):
# CREATE TABLE IF NOT EXISTS plane_data (
#     id SERIAL PRIMARY KEY,
#     plane_id TEXT NOT NULL,
#     latitude DOUBLE PRECISION NOT NULL,
#     longitude DOUBLE PRECISION NOT NULL,
#     speed_kmh DOUBLE PRECISION NOT NULL,
#     timestamp TIMESTAMP NOT NULL
# );

db_connection = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = db_connection.cursor()
# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPICS,
    group_id=KAFKA_GROUP_ID,
    bootstrap_servers=KAFKA_BROKERS
)
# Pocess each message
for message in consumer:
    try:
        # Print message details
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
        # Decode the message value (assuming JSON format)
        data = json.loads(message.value.decode('utf-8'))
       
        # Extract fields from the message
        plane_id = data.get('plane_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        speed_kmh = data.get('speed_kmh')
        timestamp = data.get('timestamp')
        # Validate that all required fields are present
        if not all([plane_id, latitude, longitude, speed_kmh, timestamp]):
            print("Missing required fields in message:", data)
            continue
            # Insert data into the PostgreSQL database
        insert_query = """
                INSERT INTO plane_data (plane_id, latitude, longitude, speed_kmh, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(insert_query, (plane_id, latitude, longitude, speed_kmh, timestamp))
            # Commit the transaction
        db_connection.commit()
        print("Data inserted successfully:", data)
    except Exception as e:
        print("Error processing message:", e)
        db_connection.rollback()
# Close database connection (if exiting the loop)
cursor.close()
db_connection.close()


