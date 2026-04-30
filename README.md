# Kaggle Data — Job Salary Prediction Pipeline

Проект по построению аналитического пайплайна обработки данных о вакансиях и зарплатах с использованием **Apache Spark**, **Data Build Tools**, **Airflow** и **MinIO**.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Spark](https://img.shields.io/badge/Spark-E25A1C?logo=apachespark&logoColor=white)
![Iceberg](https://img.shields.io/badge/Apache%20Iceberg-1E90FF)
![dbt](https://img.shields.io/badge/dbt-FF694B?logo=dbt&logoColor=white)
![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC00?logo=clickhouse&logoColor=black)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?logo=apacheairflow&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?logo=metabase&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## О проекте

Полноценный **production-grade** Data Lakehouse проект на основе датасета **Job Salary Prediction** (kaggle) (https://www.kaggle.com/datasets/nalisha/job-salary-prediction-dataset):

- Ингест данных из Kaggle → Bronze
- Очистка, валидация и трансформация → Silver
- Построение аналитических витрин (агрегации) → Gold



## Поток данных

```
Источники данных
          ↓
Airflow DAG (Ingestion)
          ↓
MinIO → Bronze (raw files)
          ↓
PySpark Job (очистка, дедупликация, обогащение)
          ↓
MinIO Silver Apache Iceberg tables (Nessie catalog)
          ↓
dbt c помощью Trino читает данные напрямую из Silver Iceberg. 
          ↓
dbt → materializes Gold layer **ClickHouse** with Trino
          ↓
Metabase Dashboards
```

---

## Аналитические витрины (Gold)

1. **fct_salary_by_job_title** - Лучшие и худшие оплачиваемые должности, диапазон зарплат, количество вакансий
2. **fct_salary_by_experience** - Как растёт зарплата в зависимости от опыта (бакеты по годам) (experience_bucket (0-2, 3-5, 6-10, 10+))
3. **fct_salary_by_location** - Зарплаты по странам/регионам + влияние remote work
4. **fct_salary_by_company_size** - Сравнение зарплат в компаниях малого, среднего и крупного размера
5. **fct_salary_by_skills** - Влияние количества навыков и сертификатов на зарплату
6. **fct_remote_work_impact** - Сравнение зарплат remote / hybrid / office по отраслям и должностям
7. **fct_job_market_overview** - Общая сводка рынка труда 

---

## Стек технологий

- **Python 3.11**
- **Apache Spark** + **Iceberg**
- **Apache Airflow**
- **Trino** + **Nessie**
- **Data Build Tools (dbt)**
- **MinIO** (S3-совместимое хранилище)
- **Clickhouse**
- **Docker**

---

## Как запустить проект

### 1. Клонирование репозитория

```bash
git clone https://github.com/fvrsvv/kaggle-data.git
cd kaggle-data
```
### 2. Настройка
Создайте **.env** в корне проект и укажите свои параметры (.env.example)

### 3. Запуск окружения через Docker Compose
```bash
docker-compose up -d
```

### 4. Запуск пайплайна
- Зайдите в Airflow UI (http://localhost:8080) и запустите DAG.
- MinIO (http://localhost:9001) 

- Настройка Metabase (http://localhost:3000)
    1. Database type: ClickHouse
    2. Name: ClickHouse 
    3. Host: clickhouse
    4. Port: 8123
    5. Username: clickhouse.username (.env)
    6. Password: clickhouse.password (.env)

https://github.com/fvrsvv/kaggle-data
