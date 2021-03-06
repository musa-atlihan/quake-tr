from .scrape import KOERI
from datetime import datetime
from airflow.models import Connection
from airflow.settings import Session
from airflow.hooks.postgres_hook import PostgresHook

from .conf import CONF
from .queries import *


def init_etl():
    session = Session()
    for connection in CONF.get('connections', []):
        conn = Connection(**connection)
        if not session.query(Connection.conn_id == conn.conn_id).first()[0]:
            session.add(conn)
            session.commit()
    session.close()


def insert_quake_data():
    koeri = KOERI()
    hook = PostgresHook(postgres_conn_id="postgres_quake_tr")
    for year in range(2007, datetime.now().year+1):
        for params in koeri.read_data(year):
            hook.run(insert_quake_tr_table, autocommit=True, parameters=params)
