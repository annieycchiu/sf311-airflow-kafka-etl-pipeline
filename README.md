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

![Alt text](./assets/images/airflow_1.png)

![Alt text](./assets/images/airflow_2.png)

### Kafka

![Alt text](./assets/images/kafka.png)

### PostgreSQL DB

![Alt text](./assets/images/postgresql_db.png)

### Streamlit/ Plotly/ Folium

![Alt text](./assets/images/streamlit.png)

<video width="320" height="240" controls>
  <source src="./assets/videos/streamlit_dashboard.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
