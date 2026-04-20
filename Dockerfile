FROM apache/airflow:2.11.2-python3.10

USER root

# Устанавливаем Java и необходимые утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    procps \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Находим реальный путь к Java и устанавливаем переменные
RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java)))) \
    && echo "JAVA_HOME is $JAVA_HOME" \
    && ln -s $JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH="${JAVA_HOME}/bin:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

# Распаковываем Spark из локального файла
COPY spark-3.5.8-bin-hadoop3.tgz /tmp/spark.tgz

RUN tar -xzf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-3.5.8-bin-hadoop3 ${SPARK_HOME} \
    && rm /tmp/spark.tgz \
    && chown -R airflow: ${SPARK_HOME} ${JAVA_HOME}

# Добавляем JARы для MinIO/Iceberg
RUN mkdir -p ${SPARK_HOME}/jars && \
    curl -sL -o ${SPARK_HOME}/jars/hadoop-aws-3.3.4.jar \
        https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -sL -o ${SPARK_HOME}/jars/aws-java-sdk-bundle-1.12.777.jar \
        https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.777/aws-java-sdk-bundle-1.12.777.jar && \
    curl -sL -o ${SPARK_HOME}/jars/iceberg-spark-runtime-3.5_2.12-1.5.2.jar \
        https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.2/iceberg-spark-runtime-3.5_2.12-1.5.2.jar

# Устанавливаем права
RUN chown -R airflow: ${SPARK_HOME}/jars
USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# ==================== dbt ====================
RUN python -m venv /home/airflow/dbt_venv

RUN /home/airflow/dbt_venv/bin/pip install --no-cache-dir \
    dbt-core==1.8.0 \
    dbt-trino==1.8.5 \
    dbt-clickhouse==1.8.0 \
    && /home/airflow/dbt_venv/bin/pip cache purge

USER root
RUN ln -s /home/airflow/dbt_venv/bin/dbt /usr/local/bin/dbt
USER airflow