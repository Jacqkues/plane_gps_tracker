from kafka import KafkaConsumer
import psycopg2
import os
import json  # Assuming the Kafka message payload is JSON formatted

# Environment variables
BROKER_IP = os.getenv("BROKER_IP", "127.0.0.1")

KAFKA_BROKERS = [f'{BROKER_IP}:9092', f'{BROKER_IP}:9094', f'{BROKER_IP}:9096']
KAFKA_TOPICS = 'event'
KAFKA_GROUP_ID = "gps_group_event"

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

print("Kafka Brokers:", KAFKA_BROKERS)

# Database connection

# Table schema (for reference):
#CREATE TABLE IF NOT EXISTS event (
#    id SERIAL PRIMARY KEY,
#    plane_id TEXT NOT NULL,
#    message TEXT NOT NULL,
#    timestamp TIMESTAMP NOT NULL
#)

def start():
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

# Process each message
    for message in consumer:
        try:
            # Print message details
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
            # Decode the message value (assuming JSON format)
            data = json.loads(message.value.decode('utf-8'))
            plane_id = data.get('plane_id')
            message = data.get('message')
            timestamp = data.get('timestamp')
                # Validate that all required fields are present
            if not all([plane_id, message, timestamp]):
                print("Missing required fields in message:", data)
                continue

                # Insert data into the PostgreSQL database
            insert_query = """
                INSERT INTO event (plane_id, message, timestamp)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (plane_id,message, timestamp))

                # Commit the transaction
            db_connection.commit()
            print("Data inserted successfully:", data)
        except Exception as e:
            print("Error processing message:", e)
            db_connection.rollback()

    # Close database connection (if exiting the loop)
    cursor.close()
    db_connection.close()


