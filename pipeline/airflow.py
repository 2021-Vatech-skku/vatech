from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# define arguments and dag
args = {
      'owner' : 'Songhyun',
      'start_date' : days_ago(2),
      'retries' : 2,
      'retry_delay' : timedelta(seconds=10),
}

dag = DAG('ETL_workflow', schedule_interval = '@daily', default_args = args)
homepath = "/usr/local/airflow/"
settings = "export SPARK_HOME=/usr/local/airflow/spark && export PATH=$PATH:$SPARK_HOME/bin && "

task0 = BashOperator(task_id="Remove_data", bash_command="rm -rf /usr/local/airflow/Clever", dag=dag)
task1 = BashOperator(task_id='Chart_ETL', bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + "source/chart-etl.py", dag=dag)
task2 = BashOperator(task_id="Patient_ETL", bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + "source/patient-etl.py", dag=dag)
task3 = BashOperator(task_id="Done", bash_command="echo Done!", dag=dag)

# schedule
task0 >> task1 >> task2 >> task3

