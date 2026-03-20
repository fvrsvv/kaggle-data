import kagglehub
import logging
from kagglehub import KaggleDatasetAdapter
import pandas as pd
# from dotenv import dotenv_values

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_kaggle():
    df = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS, "nalisha/job-salary-prediction-dataset", "job_salary_prediction_dataset.csv")
    return df

# path = "job_salary_prediction_dataset.csv"
# df = download_kaggle(path)
# print(df.head(-5))
# print(df.shape)