from airflow import DAG
from airflow.decorators import task
# from airflow.api.client.local_client import Client

from datetime import datetime
from time import time
import pandas as pd
import os, sys

cur_dir = os.getcwd()

@task(task_id = 'load')
def load_data():
    return pd.read_excel(os.path.join(cur_dir, 'dags/data/source_data.xlsx'))

@task(task_id = 'save')
def save_data(df):
    df.to_excel(os.path.join(cur_dir, 'dags/data/saved_data.xlsx'))

with DAG(dag_id = 'dag',
         start_date = datetime(2023, 5, 3),
         schedule_interval = '@hourly',
         catchup = False
         ) as dag:
    loaded_data = load_data()
    saved_data = save_data(loaded_data)
    
    loaded_data >> saved_data

# client = Client(None, None)
# client.trigger_dag(dag_id = 'dag')