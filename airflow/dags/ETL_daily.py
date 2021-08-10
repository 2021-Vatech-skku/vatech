from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
#from kubernetes.client import models as k8s

args = {
      'owner' : 'Sanhak',
      'start_date' : days_ago(1),    #'start_date': datetime(2021, 8, 8),
      'retries' : 2,
      'retry_delay' : timedelta(minutes=3),
}

dag = DAG('ETL_daily', schedule_interval = '0 0 * * *', default_args = args, max_active_runs=1)

t1 = KubernetesPodOperator(
    task_id="insert_chart",
    name="insert_chart",
    namespace="spark",
    image="cmcm0012/spark:latest",
    cmds=["./submit.sh"],
    arguments=["clever-fetch.py -d 0"],
    image_pull_policy="Always",
    env_vars={'SPARK_HOME' : '/opt/spark', 'JAVA_HOME' : '/usr/lib/jvm/java-11-openjdk-amd64', "SPARK_LOCAL_HOSTNAME" : "localhost"},
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)
t2 = KubernetesPodOperator(
    task_id="update_chart",
    name="update_chart",
    namespace="spark",
    image="cmcm0012/spark:latest",
    cmds=["./submit.sh"],
    arguments=["clever-fetch.py -t update -d 0"],
    image_pull_policy="Always",
    env_vars={'SPARK_HOME' : '/opt/spark', 'JAVA_HOME' : '/usr/lib/jvm/java-11-openjdk-amd64', "SPARK_LOCAL_HOSTNAME" : "localhost"},
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)
t3 = KubernetesPodOperator(
    task_id="insert_patient",
    name="insert_patient",
    namespace="spark",
    image="cmcm0012/spark:latest",
    cmds=["./submit.sh"],
    arguments=["clever-fetch.py -c jee.clever.dev0-patient.filtered.test -d 0"],
    image_pull_policy="Always",
    env_vars={'SPARK_HOME' : '/opt/spark', 'JAVA_HOME' : '/usr/lib/jvm/java-11-openjdk-amd64', "SPARK_LOCAL_HOSTNAME" : "localhost"},
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)
t4 = KubernetesPodOperator(
    task_id="update_patient",
    name="update_patient",
    namespace="spark",
    image="cmcm0012/spark:latest",
    cmds=["./submit.sh"],
    arguments=["clever-fetch.py -c jee.clever.dev0-patient.filtered.test -t update -d 0"],
    image_pull_policy="Always",
    env_vars={'SPARK_HOME' : '/opt/spark', 'JAVA_HOME' : '/usr/lib/jvm/java-11-openjdk-amd64', "SPARK_LOCAL_HOSTNAME" : "localhost"},
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

# schedule
t1 >> t2 
t3 >> t4     