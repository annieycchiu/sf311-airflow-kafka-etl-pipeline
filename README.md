# San Francisco 311 Requests - ETL Pipeline

## Project Overview

* Summary

  San Francisco faces the challenge of efficiently managing and addressing the diverse array of incidents reported through its 311 system. With a continuous influx of cases, there is a pressing need to streamline the allocation of resources and enhance response times to improve public service quality.
* Objectives

  * **Streaming Data ETL Pipeline**: Leveraging data streaming and orchestration techniques to construct a
    real-time data pipeline.
  * **Data Visualization**: Mapping 311 cases across the city to identify hotspots and patterns and allowing for interactive user inputs.
  * **Request Resolved Time Prediction**: ?everage machine learning model to predict case closure times, factoring in request types and locations.

## Architecture Diagram

![Alt text](./assets/images/sf_311_architecture.png)

## Dataset

* Open source dataset managed by San Francisco Government
* Dataset Creation:October, 2011
* Update frequency: Daily (multiple times per hour)
* Dataset Size: 2.2 GB
* Number of Records: 6.6 M
* Features:48 ()interpretable: 15)
* Source: [https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/explore](https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/explore)

## Tools & Packages

* **Data Orchestration**:apache-airflow, sodapy
* **Data Streaming**:avro,confluent_kafka, fastavro
* **Database**: pgAdmin, psycopg2, sqlalchemy
* **Modeling & Serving**: fastapi[all], mlflow, scikit-learn
* **Data Visualization**: folium, numpy, pandas, plotly, streamlit
* **Version Control**: git, Github

### Airflow

By leveraging Airflow DAGs, I retrieved data in batches daily to prevent potential API denial resulting from high-frequency requests and to accommodate the inconsistent database updates from the original data source. Once obtained from the source, the data was published to Kafka topic by the producer and then consumed by the consumer in real-time to the database.

Two DAGs are implemented:

* DAG 1 - Fetch data from Socrata API, preprocess data to extract necessary information, and produce data to Confluent Kafka topic
* DAG 2 - Consume data from Confluent Kafka topic and upsert into PostgreSQL database

![Alt text](./assets/images/airflow_1.png)

![Alt text](./assets/images/airflow_2.png)

### Kafka

I set up a Confluent Kafka topic as a designated channel where producers publish messages of 311 request data, and consumers subscribe to receive it, thereby decoupling producers from consumers. This setup facilitates real-time data processing in parallel. Additionally, I serialized the messages using the Avro serializer and register the schema in the schema registry to enhance message delivery efficiency.


![Alt text](./assets/images/kafka.png)

### PostgreSQL DB

I configured a PostgreSQL database using the pgAdmin tool to store the data consumed from the Confluent Kafka topic. This stored data was then utilized for downstream analysis, modeling, and visualizations.

![Alt text](./assets/images/postgresql_db.png)

### Streamlit/ Plotly/ Folium

I implemented a Streamlit application for real-time data visualization. Users can interact with different types of charts, such as a map, bar plot, pie plot, multi-line plot, and various metrics, by providing their inputs. Additionally, the application calls a model served by FastAPI to perform real-time predictions.


![Alt text](./assets/images/streamlit.png)
