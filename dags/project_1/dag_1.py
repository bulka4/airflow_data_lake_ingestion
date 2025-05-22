from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent / 'common/classes').resolve().as_posix()
sys.path.append(classes_path)

from class_data_ingestion import DataIngestion

from airflow import DAG
from airflow.decorators import task

from datetime import datetime
from dotenv import load_dotenv


@task(task_id = 'data_ingestion')
def data_ingestion():
    # === Task configuration ===
    
    # name of the container and directory in that container where we will be ingesting data.
    container_name = 'source-data'
    directory_name = 'source_data'

    # names of the tables (of the format <db_name>.<schema_name>.<table_name>) to ingest data from using full truncate and load.
    tables_full_load = ['db.fact.table1']

    # tables_inc_load contains information needed for incremental load. It is a table containing following columns:
    # [
    #     ['source_table_name', 'target_table_path', 'changes_table_name', 'change_created_date_column', 'pk_name', 'deleted_col']
    # ]
    # - source_table_name:  name of the source table in SQL db (of the format <db_name>.<schema_name>.<table_name>) from which we will 
    #                       be ingesting data into the Data Lake.
    # - target_table_path: path of the target table in the container which will be updated.
    # - pk_name: name of the primary key of that table.
    # - changes_table_name: name of the changes table (of the format <db_name>.<schema_name>.<table_name>) which contains information 
    #                       about changes done to the source table.
    # - change_created_date_column: name of the column in the changes table which indicates when the record has been created (when the 
    #   change happened to the source table).
    # - deleted_col: name of the column indicating if given record has been deleted in the source table.
    tables_inc_load = [
        ['db.fact.table2', f'{directory_name}/table2', 'db.fact.table2_changes', 'date_created', 'ID', 'deleted']
    ]


    # === Task execution ===

    # Load environment variables from .env file
    load_dotenv()

    account_name = os.getenv('ACCOUNT_NAME')
    access_key = os.getenv('ACCESS_KEY')

    server_name = os.getenv('SQL_SERVER_NAME')
    database = os.getenv('SQL_DB_NAME')
    sql_username = os.getenv('SQL_USERNAME')
    sql_password = os.getenv('SQL_PASSWORD')

    # Initialize class for performing data ingestion
    di = DataIngestion(
        sql_server = server_name
        ,sql_database = database
        ,sql_username = sql_username
        ,sql_password = sql_password
        ,dl_account_name = account_name
        ,dl_access_key = access_key
        ,extract_logs_container_name = 'extract-logs'
        ,extract_logs_path = 'extract_logs'
    )

    # full load
    for table_name in tables_full_load:
        di.full_load(
            source_table_name = table_name
            ,container_name = container_name
            ,target_table_path = f"{directory_name}/{table_name.split('.')[-1]}"
            ,if_exists = 'overwrite'
        )

    # incremental load
    for (
        source_table_name
        ,target_table_path
        ,changes_table_name
        ,change_created_date_column
        ,pk
        ,deleted_col
    ) in (
        tables_inc_load
    ):
        di.incr_load(
            source_table_name
            ,container_name
            ,target_table_path
            ,changes_table_name
            ,change_created_date_column
            ,pk
            ,deleted_col
        )


with DAG(
    dag_id = 'data_lake_ingestion',
    start_date = datetime.now(),
    schedule_interval = '@hourly',
    catchup = False
) as dag:
    data_ingestion()



# client = Client(None, None)
# client.trigger_dag(dag_id = 'dag')