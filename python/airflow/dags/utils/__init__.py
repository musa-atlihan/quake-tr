from scrape import KOERI
from datetime import datetime
from airflow.hooks.postgres_hook import PostgresHook

from etl_queries import *


def insert_quake_data():
    koeri = KOERI()
    hook = PostgresHook(postgres_conn_id="postgres_quake_tr")
    for year in range(2007, datetime.now().year):
        for params in koeri.read_data(year, year+1):
            hook.run(create_quake_tr_table, autocommit=True, parameters=params)
