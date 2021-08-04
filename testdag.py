from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

# define arguments and dag
args = {
      'owner' : 'SKKU-Sanahk',
      'start_date' : days_ago(2),
      'retries' : 2,
      'retry_delay' : timedelta(minutes=3),
}

dag = DAG('ETL_workflow_daily', schedule_interval = '@daily', default_args = args, max_active_runs=2)

t1 = KubernetesPodOperator(
    namespace='spark',
    image="cmcm0012/tespark:v1",
    cmds=["./submit.sh"],
    arguments=["chart-etl.py"],
    labels={"foo": "bar"},
    image_pull_policy="Always",
    name="chart-cdc",
    task_id="Chart-etl",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

t2 = KubernetesPodOperator(
    namespace='spark',
    image="cmcm0012/tespark:v1",
    cmds=["./submit.sh"],
    arguments=["patient-etl.py"],
    labels={"foo": "bar"},
    image_pull_policy="Always",
    name="patient-cdc",
    task_id="Patient-etl",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

t1 >> t2