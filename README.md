# Kaggle Data — Job Salary Prediction Pipeline

Проект по построению аналитического пайплайна обработки данных о вакансиях и зарплатах с использованием **Apache Spark**, **Delta Lake**, **Airflow** и **MinIO**.

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
Источники данных (Kaggle, API, базы и т.д.)
          ↓
     Airflow DAG (Ingestion)
          ↓
   MinIO → Bronze (сырые данные)
          ↓
   PySpark Job (очистка, дедупликация, обогащение)
          ↓
   MinIO → Silver (Apache Iceberg tables)
          ↓
   ClickHouse (читает Silver напрямую через IcebergS3)
          ↓
          dbt (на ClickHouse) + Cosmos
   ├── Silver models → materialization: view / ephemeral
   └── Gold / Data Marts → materialization: table / incremental (MergeTree)
          ↓
   BI-инструменты (Metabase / Superset / Lightdash и т.д.)
```

### Основные витрины (Gold layer)

- **salary_by_industry** — статистика зарплат по отраслям (средняя, медиана, мин/макс, стандартное отклонение)
- **salary_by_experience_edu** — статистика зарплат по категориям опыта и уровню образования
- **salary_summary** — сводная статистика по remote work и размеру компании

---

## Стек технологий

- **Python 3.11**
- **Apache Spark** + **Delta Lake**
- **Apache Airflow** (оркестрация DAG'ов)
- **MinIO** (S3-совместимое хранилище)
- **Docker** + **docker-compose**
- PySpark, Delta-spark, Hadoop AWS

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
### Сервисы, которые запустятся:

- Airflow (webserver + scheduler)
- Spark (в режиме local[*])
- MinIO (S3-совместимое хранилище)

### 3. Настройка
Создайте .env в корне проект и укажите свои параметры (пример .env.example).

### 4. Запуск пайплайна
Зайдите в Airflow UI (http://localhost:8080) и запустите DAG.

https://github.com/fvrsvv/kaggle-data