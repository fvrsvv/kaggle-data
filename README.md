# Kaggle Data — Job Salary Prediction Pipeline

Проект по построению аналитического пайплайна обработки данных о вакансиях и зарплатах с использованием **Apache Spark**, **Data Build Tools**, **Airflow** и **MinIO**.

Цель проекта — загрузить сырые данные с Kaggle, очистить, трансформировать, обогатить их, а затем построить готовые аналитические витрины для бизнес-аналитики.

---

## О проекте

Этот репозиторий содержит полный **ETL/ELT пайплайн** для датасета **Job Salary Prediction** (https://www.kaggle.com/datasets/nalisha/job-salary-prediction-dataset):

- Ингест данных из Kaggle → Bronze
- Очистка, валидация и трансформация → Silver
- Построение аналитических витрин (агрегации) → Gold

Используется современный **Data Lakehouse** подход на базе **Iceberg**.

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
Analytics / BI / Data Marts используют ClickHouse Gold
```

---

## Data marts

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
Создайте .env в корне проект и укажите свои параметры (.env.example)

### 3. Запуск окружения через Docker Compose
```bash
docker-compose up -d
```

### 4. Запуск пайплайна
Зайдите в Airflow UI (http://localhost:8080) и запустите DAG.

https://github.com/fvrsvv/kaggle-data
