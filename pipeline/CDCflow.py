from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# define arguments and dag
args = {
      'owner' : 'Songhyun',
      'start_date' : days_ago(2),
      'retries' : 2,
      'retry_delay' : timedelta(minutes=3),
}

dag = DAG('ETL_workflow_daily', schedule_interval = '@daily', default_args = args, max_active_runs=2)
homepath = "/usr/local/airflow/"
settings = "export SPARK_HOME=/usr/local/airflow/spark && export PATH=$PATH:$SPARK_HOME/bin && "

task0 = BashOperator(task_id="Dummy_Task", bash_command="echo {{ ds }}", dag=dag)
task1 = BashOperator(task_id='Chart_ETL',
        bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + """source/chart-etl.py -y {{ execution_date.strftime("%Y") }} -m {{ execution_date.strftime("%m") }} -d {{ execution_date.strftime("%d") }}""",
        dag=dag)
task2 = BashOperator(task_id="Patient_ETL",
        bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + """source/patient-etl.py -y {{ execution_date.strftime("%Y") }} -m {{ execution_date.strftime("%m") }} -d {{ execution_date.strftime("%d") }}""",
        dag=dag)
task3 = BashOperator(task_id="Done", bash_command="echo Done!", dag=dag)

# schedule
task0 >> task1 >> task2 >> task3

# task0 >> task1 >> task3 << task2 << task0
