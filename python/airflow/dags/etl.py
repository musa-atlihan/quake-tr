from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from utils.etl import init_etl, insert_quake_data
from utils.etl.queries import *


default_args = {
    "owner": "QuakeTR",
    "start_date": datetime.now() - timedelta(hours=1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "load_examples": False
}

with DAG(
        "insert_historical_quake_data",
        default_args=default_args,
        schedule_interval="@once") as dag:

    task_create_quake_tr_table = PostgresOperator(
        task_id="create_quake_tr_table",
        postgres_conn_id="postgres_quake_tr",
        autocommit=True,
        sql=create_quake_tr_table
    )

    task_init_etl = PythonOperator(
        task_id="init_etl",
        python_callable=init_etl
    )

    task_insert_quake_tr_table = PythonOperator(
        task_id="insert_quake_tr_table",
        python_callable=insert_quake_data
    )

    task_init_etl >> task_create_quake_tr_table >> task_insert_quake_tr_table
