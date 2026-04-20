# Kaggle Data — Job Salary Prediction Pipeline

Проект по построению аналитического пайплайна обработки данных о вакансиях и зарплатах с использованием **Apache Spark**, **Data Build Tools**, **Airflow** и **MinIO**.

Цель проекта — загрузить сырые данные с Kaggle, очистить и сохранить их в Silver-слое, а затем построить готовые аналитические витрины (Gold layer) для бизнес-аналитики.

---

## О проекте

Этот репозиторий содержит полный **ETL/ELT пайплайн** для датасета **Job Salary Prediction** (https://www.kaggle.com/datasets/nalisha/job-salary-prediction-dataset):
- Ингест данных из Kaggle → Bronze
- Очистка, валидация и трансформация → Silver
- Построение аналитических витрин (агрегации) → Gold

Используется современный **Data Lakehouse** подход на базе Delta Lake.

## Поток данных

```
Источники данных
          ↓
Airflow DAG (Ingestion)
          ↓
MinIO → Bronze (сырые данные)
          ↓
PySpark Job (очистка, дедупликация, обогащение)
          ↓
MinIO → Silver (Apache Iceberg tables)
(Nessie as REST Catalog)
          ↓
dbt читает данные напрямую из Silver Iceberg. 
Trino выступает как query engine, который умеет читать Iceberg таблицы по SQL.
          ↓
dbt материализует модели в ClickHouse (Gold layer).
          ↓
dbt (на ClickHouse) + Cosmos
   ├── Silver models → materialization: view / ephemeral
   └── Gold / Data Marts → materialization: table / incremental (MergeTree)
          ↓
BI-инструменты (Metabase / Superset)
```

---

## Стек технологий

- **Python 3.11**
- **Apache Spark** + **Iceberg**
- **Apache Airflow**
- **Trino** + **Polaris**
- **Data Build Tools (dbt)**
- **MinIO** (S3-совместимое хранилище)
- **Docker**

---

## Как запустить проект

### 1. Клонирование репозитория

```bash
git clone https://github.com/fvrsvv/kaggle-data.git
cd kaggle-data
```

### 2. Запуск окружения через Docker Compose
```bash
docker-compose up -d
```

### 3. Настройка
Создайте .env в корне проект и укажите свои параметры (пример .env.example).

### 4. Запуск пайплайна
Зайдите в Airflow UI (http://localhost:8080) и запустите DAG.

https://github.com/fvrsvv/kaggle-data
