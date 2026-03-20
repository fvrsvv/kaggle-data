import kagglehub
import logging
from kagglehub import KaggleDatasetAdapter
import pandas as pd
# from dotenv import dotenv_values

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def download_kaggle_dataset():
#     dataset = dotenv_values(".env.KAGGLE_DATASET") 
#     path = kagglehub.dataset_download(dataset)
#     print("Путь к файлам:", path)

path="job_salary_prediction_dataset.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "nalisha/job-salary-prediction-dataset",
  path,
)

print(df.head(-5))
print(df.shape)