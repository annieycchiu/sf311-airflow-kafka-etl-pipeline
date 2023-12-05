# standard library imports
import os
import csv 

# third-party library imports
from dotenv import load_dotenv

# Confluent Kafka client libraries for producing messages and managing Kafka topics
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

# local application/module imports
from .schemas import request_stream_schema
from .entities import RequestStreamModel    

# load secrets to connect to confluent kafka
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

def create_topic(admin_client, topic_name, partitions=3, replication_factor=3):
    """
    Verify Kafka topic creation.
    """
    # initialize Kafka client
    admin_client = AdminClient(get_kafka_config())

    # define topic to be connected
    topic = [NewTopic(topic=topic_name, 
                      num_partitions=partitions, 
                      replication_factor=replication_factor)]
    
    # handle topic creation failure
    try:
        futures = admin_client.create_topics(topic)
        for topic_name, future in futures.items():
            future.result()
            print(f'Topic {topic_name} is created')
    except Exception as e:
            print(f'Failed to create topic {topic_name} - {e}')

def delivery_report(err, msg):
    """
    Callback to report the result of the produce operation.
    """
    if err is not None:
        print(f'Message delivery failed - {err}')
    else:
        # Retrieve the topic name
        topic = msg.topic()
        # Retrieve the partition to which the message was sent
        partition = msg.partition()
        # Retrieve the message offset
        offset = msg.offset()
        # Retrieve the message key
        key = msg.key().decode('utf_8')
        # # Retrieve the message value
        # value = msg.value()

        print(f'Message delivery successful - Topic: {topic}, Partition: {partition}, Offset: {offset}, Key: {key}')

def make_producer():
    """
    Create and return a Kafka producer with Avro serialization.
    """
    # set up Confluent schema registry client
    schema_registry_client = SchemaRegistryClient({
        'url': os.getenv('SCHEMA_REGISTRY_URL'),
        'basic.auth.user.info': os.getenv('BASIC_AUTH_USER_INFO')
        })
    
    # set up value serializer using Avro
    value_serializer = AvroSerializer( 
        schema_registry_client=schema_registry_client,
        schema_str=request_stream_schema,
        to_dict=lambda x, ctx: x.dict(by_alias=True))
    
    return SerializingProducer({
        **get_kafka_config(),
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': value_serializer,
    })


def produce_csv_to_kafka(csv_path):
    """Produce messages from csv file to Kafka topic."""
    # set up connection to Kafka topic
    config = get_kafka_config()
    admin_client = AdminClient(config)
    topic_name = os.getenv('TOPIC_NAME')
    create_topic(admin_client, topic_name)

    # initialize serializing producer
    producer = make_producer()

    # produce data in csv file to topic line by line
    with open(csv_path) as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip the header row
        next(csv_reader)
        for row in csv_reader:
            # message key
            request_id = row[0]
            # message value
            request_data = RequestStreamModel(
                request_id = row[0],
                requested_datetime = row[1],
                updated_datetime = row[2],
                status_description = row[3],
                agency_responsible = row[4],
                service_type = row[5],
                service_subtype = row[6],
                address = row[7],
                street = row[8],
                supervisor_district = row[9],
                neighborhood = row[10],
                police_district = row[11],
                latitude = float(row[12]),
                longitude = float(row[13]),
                source = row[14])
            
            # produce the data to the Kafka topic
            producer.produce(
                topic=topic_name,
                key=str(request_id),
                value=request_data,
                on_delivery=delivery_report
            )

            producer.flush() # Ensure all messages are sent


if __name__ == '__main__':
    csv_path = '../data/processed_data/2023-11-28/sf_311.csv'
    produce_csv_to_kafka(csv_path)