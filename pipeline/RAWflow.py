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
      'retry_delay' : timedelta(minutes=3),
}

dag = DAG('ETL_Mongo_Once', schedule_interval = '@once', default_args = args)
homepath = "/usr/local/airflow/"
settings = "export SPARK_HOME=/usr/local/airflow/spark && export PATH=$PATH:$SPARK_HOME/bin && "

task0 = BashOperator(task_id="Test_task", bash_command="echo Started!", dag=dag)
task1 = TriggerDagRunOperator(task_id='test_trigger_dagrun', trigger_dag_id="ETL_workflow_daily", dag=dag)

# schedule
task0 >> task1 

