from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "woojeong",
    "depends_on_past": False,
    "start_date": datetime(2021, 7, 21, 7, 0 ,0),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'end_date': datetime(2016, 1, 1),
}

dag= DAG('test',default_args=default_args,schedule_interval=timedelta(minutes=1))

def record_now():
    now=datetime.now()
    nowDatetime=now.strftime('%Y-%m-%d_%H:%M:%S')
    f=open("/usr/local/airflow/test/"+str(nowDatetime)+".txt", 'w')
    f.write(str(nowDatetime))
    f.close()
    print('recorded the datetime => '+str(nowDatetime))
    return 'hello airflow'

t1 = PythonOperator(task_id='record_now', python_callable=record_now, dag=dag)

t2 = BashOperator(task_id='print_now',bash_command='date', dag=dag)

t1>>t2