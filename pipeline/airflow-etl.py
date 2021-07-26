from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# define arguments and dag
args = {
  'owner' : 'Songhyun',
  'start_date' : days_ago(2),
  'retries' : 2,
  'retry_delay': timedelta(minutes=5)
}

dag = DAG('workflow', schedule_interval = '@daily', default_args = args)
homepath = "/usr/local/airflow"
# save raw data to data lake
task1 = BashOperator(task_id='Fetch', bash_command=homepath + "spark/bin/spark-submit " + homepath + "source/fetch.py", dag=dag)
# get raw data from data lake and etl as delta lake
task2 = BashOperator(task_id="ETL", bash_command=homepath + "spark/bin/spark-submit " + homepath + "source/etl.py", dag=dag)
# get etl data and update database
task3 = BashOperator(task_id="update_Database", bash_command=homepath + "spark/bin/spark-submit " + homepath + "source/update-databases.py", dag=dag)

# schedule
task1 >> task2 >> task3
