from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from utils.analysis.cluster import insert_cluster_labels, drop_cluster_table
from utils.analysis.queries import *


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
        "analyze_quakes",
        default_args=default_args,
        schedule_interval="@once") as dag:

    task_drop_clustering_table = PythonOperator(
        task_id="drop_clustering_table",
        python_callable=drop_cluster_table
    )

    task_create_clustering_table = PostgresOperator(
        task_id="create_clustering_table",
        postgres_conn_id="postgres_quake_tr",
        sql=create_clustering_table
    )

    task_insert_clustering_table = PythonOperator(
        task_id="insert_clustering_table",
        python_callable=insert_cluster_labels
    )

    task_drop_clustering_table >> task_create_clustering_table >> task_insert_clustering_table
