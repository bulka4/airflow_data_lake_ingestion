from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent / 'common/classes').resolve().as_posix()
sys.path.append(classes_path)

from class_data_ingestion import DataIngestion

from airflow import DAG
from airflow.decorators import task

from datetime import datetime


@task(task_id = '1')
def task1():
    print('task 1 executing...')
    return 10


@task(task_id = '2')
def task2(x):
    print(f'value returned by the first task: {x}')

with DAG(
    dag_id = 'dag',
    start_date = datetime.now(),
    schedule_interval = '@hourly',
    catchup = False
) as dag:
    x = task1()
    task2(x)
    
    task1() >> task2(x)



# client = Client(None, None)
# client.trigger_dag(dag_id = 'dag')