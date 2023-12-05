# standard library imports
import os

# third-party library imports
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Confluent Kafka client libraries for consuming messages and managing Kafka topics
from confluent_kafka import KafkaException, DeserializingConsumer, OFFSET_BEGINNING
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# local application/module imports
from .schemas import request_stream_schema


# load secrets to connect confluent kafka
load_dotenv(verbose=True)


def get_kafka_config():
    """
    Load Kafka configuration from environment variables.
    """
    return {
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
        'security.protocol': os.getenv('SECURITY_PROTOCOL'),
        'sasl.mechanisms': os.getenv('SASL_MECHANISMS'),
        'sasl.username': os.getenv('SASL_USERNAME'),
        'sasl.password': os.getenv('SASL_PASSWORD'),
    }

def get_postgres_config():
    """
    Load Postgres configuration from environment variables.
    """
    return {
        'host': os.getenv('POSTGRE_HOST'),
        'port': os.getenv('POSTGRE_PORT'),
        'database': os.getenv('POSTGRE_DATABASE'),
        'user': os.getenv('POSTGRE_USER'),
        'password': os.getenv('POSTGRE_PASSWORD'),
    }

def upsert_query():
    """Upsert query for PostgreSQL database"""
    return f'''
        INSERT INTO kafka_311_request (
            request_id, requested_datetime, updated_datetime, 
            status_description, agency_responsible, service_type, 
            service_subtype, address, street, supervisor_district, 
            neighborhood, police_district, latitude, longitude, source) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (request_id)
        DO UPDATE SET
        requested_datetime = EXCLUDED.requested_datetime, 
        updated_datetime = EXCLUDED.updated_datetime, 
        status_description = EXCLUDED.status_description, 
        agency_responsible = EXCLUDED.agency_responsible, 
        service_type = EXCLUDED.service_type, 
        service_subtype = EXCLUDED.service_subtype, 
        address = EXCLUDED.address, 
        street = EXCLUDED.street, 
        supervisor_district = EXCLUDED.supervisor_district, 
        neighborhood = EXCLUDED.neighborhood, 
        police_district = EXCLUDED.police_district, 
        latitude = EXCLUDED.latitude, 
        longitude = EXCLUDED.longitude, 
        source = EXCLUDED.source
        '''


def make_consumer():
    """
    Create and return a Kafka consumer with Avro deserialization.
    """
    schema_registry_client = SchemaRegistryClient({
        'url': os.getenv('SCHEMA_REGISTRY_URL'),
        'basic.auth.user.info': os.getenv('BASIC_AUTH_USER_INFO')
        })
    
    value_deserializer = AvroDeserializer( 
        schema_registry_client=schema_registry_client,
        schema_str=request_stream_schema)
    
    return DeserializingConsumer({
        **get_kafka_config(),
        'group.id': os.getenv('CONSUMER_GROUP_ID', ),
        'auto.offset.reset': 'latest',
        'key.deserializer': StringDeserializer("utf_8"),
        'value.deserializer': value_deserializer,
    })

def on_assign(consumer, partitions):
    """
    Callback executed when partitions are assigned. Sets partition offset to beginning.
    """
    for partition in partitions:
        partition.offset = OFFSET_BEGINNING
    consumer.assign(partitions)

def consume_messages_to_postgres(thresh):
    """
    Consume messgaes from Kafka topic and upsert into PostgreSQL database.
    """
    # subscribe to Kafka topic
    topic_name = os.getenv('TOPIC_NAME')
    consumer = make_consumer()
    consumer.subscribe([topic_name], on_assign=on_assign)

    try:
        # set up database connection
        conn = psycopg2.connect(**get_postgres_config())
        cursor = conn.cursor()

        # set up a threshold to terminate the consumer
        condition = True
        no_message_count = 0

        while condition:
            msg = consumer.poll(0.1)

            if msg is None:
                print(f'Consumer receive no message from {topic_name}')
                no_message_count += 1

                # stop the consumer if it reaches a threshold of not receiving message from the topic
                if no_message_count >= thresh:
                    print(f'Consumer receive no message from {topic_name} for {thresh} times consecutively. Stop consuming.')
                    condition = False

            elif msg.error():
                print(f'error from consumer {msg.error()}')
            else:
                key = msg.key()
                val = msg.value()
                print(f'Consumed message from {topic_name} - Key: {key}')

                # get upsert data
                data = list(val.values())

                # get upsert query
                upsert_query = upsert_query()

                try:
                    # upsert data into database
                    cursor.execute(upsert_query, data)
                    print(f'Record with id {val["request_id"]} upserted into PostgreSQL')
                except Error as e:
                    conn.rollback()
                    print(f'Error upserting record: {e}')
                finally:
                    conn.commit()

    except KafkaException as kafka_exception:
        print(f'Kafka Exception: {kafka_exception}')
    except psycopg2.Error as psycopg_error:
        print(f'PostgreSQL Error: {psycopg_error}')
    finally:
        consumer.close()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    thresh = 50
    consume_messages_to_postgres(thresh)