from datetime import timedelta
from airflow import DAG
from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

args = {
    'owner' : 'gmlrhks95',
    'start_date' : days_ago(2),
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='elastic_faker_example', 
    schedule_interval=None,
    default_args=args,
    tags=['faker'],
    ) as dag:

    test_elastic_faker = KubernetesPodOperator(
        namespace='elasticsearch',
        image='gmlrhks95/elastic-faker',
        name='elastic-faker-pods',
        is_delete_operator_pod=True,
        in_cluster=True,
        task_id="elastic-faker",
        get_logs=True,
    )

    test_echo = KubernetesPodOperator(
        namespace='elasticsearch',
        image='busybox',
        name='echoing',
        is_delete_operator_pod=True,
        in_cluster=True,
        task_id="echoing",
        cmds=['echo'],
        arguments=['Hello World!'],
        get_logs=True,
    )

    test_elastic_faker >> test_echo