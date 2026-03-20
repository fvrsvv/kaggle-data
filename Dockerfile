FROM apache/airflow:2.11.2-python3.11

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nano iputils-ping git \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir \
        apache-airflow==2.11.2\
        -r requirements.txt \
    && pip cache purge