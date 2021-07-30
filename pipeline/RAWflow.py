from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.dates import days_ago

# define arguments and dag
args = {
      'owner' : 'Songhyun',
      'start_date' : days_ago(2),
      'retries' : 2,
      'retry_delay' : timedelta(minutes=1),
}

dag = DAG('ETL_Whole_Once', schedule_interval = '@once', default_args = args, max_active_runs=1)
homepath = "/usr/local/airflow/"
settings = "export SPARK_HOME=/usr/local/airflow/spark && export PATH=$PATH:$SPARK_HOME/bin && "

task0 = BashOperator(task_id="ETL_Whole_Chart", bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + "source/chart-etl.py", dag=dag)
task1 = BashOperator(task_id="ETL_Whole_Patient", bash_command=settings + homepath + "spark/bin/submit.sh " + homepath + "source/patient-etl.py", dag=dag)
task2 = TriggerDagRunOperator(task_id='trigger_dagrun', trigger_dag_id="ETL_workflow_daily", dag=dag)

# schedule
task0 >> task1 >> task2

# task0 >> task2
# task1 >> task2