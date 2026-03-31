FROM apache/airflow:2.11.2-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jdk-headless \
        nano iputils-ping git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

USER airflow

COPY requirements.txt .

RUN pip uninstall -y dbt-core dbt-clickhouse dbt-adapters dbt-common || true && \
    pip install --no-cache-dir --force-reinstall \
        -r requirements.txt && \
    pip cache purge

RUN dbt --version