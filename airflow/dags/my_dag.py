from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pytz import timezone
import random
import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path="/opt/airflow/dags/.env")

def insert_loop():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    jakarta = timezone('Asia/Jakarta')

    for _ in range(12):
        value = round(random.uniform(10.0, 100.0), 2)
        now = datetime.now(jakarta).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO sensor_data (value, timestamp) VALUES (%s, %s);", (value, now))
        conn.commit()
        time.sleep(5)

    cur.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

with DAG(
    dag_id='insert_sensor_data_every_5s',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/1 * * * *',
    catchup=False,
    tags=["sensor", "realtime"]
) as dag:

    task_insert_loop = PythonOperator(
        task_id='insert_sensor_data_looped',
        python_callable=insert_loop
    )

    task_insert_loop