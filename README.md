# Vatech songhyun

## 1. 요구사항
Apache Spark가 설치되어 있어야 하며, 환경 변수 설정(%SPARK_HOME, %JAVA_HOME)이 선행되어 있어야 한다. 

## 2. ETL
etl 폴더 안에 Faker 모듈을 이용한 dummy data 생성 코드와 해당 데이터를 가지고 ETL 과정을 거쳐 저장하는 코드 두개가 있다.

## 3. Thriftserver
Thriftserver는 JDBC를 이용, 쿼리를 스파크에서 처리 가능하도록 변환하여 주는 역할을 한다. SparkSQL에서 이용하는 데이터베이스는 spark-warehouse/, metastore_db/에 저장된다.(보통 루트경로)

먼저 
```
./local_thrift.sh
```
를 통해 서버를 실행하고, 
```
SPARK_HOME/bin/beeline
``` 
을 통해 해당 서버에 접속한다. (혹은 spark-beeline)

기본 포트는 10000이므로, 
```
!connect jdbc:hive2://localhost:10000
```
 을 입력하면 Spark SQL에 접속가능하다.
 
 beeline에서 테이블을 미리 만들어줘야한다. 예시는 다음과 같다.
 ```bash
 create table patients using DELTA location "s3a://bucket/folder"
 ```
## 3-1. mySQL
Thriftserver를 통해 업로드 하는 것에 대한 이해 부족으로진행이 안되어 mysql로 먼저 진행해보았다. mysql.py 파일을 submit 하는 것으로 해결되지만, spark 설치 경로 안의 jars 폴더에 jdbc connector 파일(jar)을 넣어줘야 정상적으로 실행된다. config로써 경로를 지정해주긴 했으나, 폴더에 넣어주거나, 인자를 주는 방법으로만 인식을 제대로 하는 듯 하다.
```
spark-submit --driver-class-path=path/to/mysql-connector-java-8.0.25.jar mysql.py
```
## 3-2. mongoDB
mongoDB는 JDBC를 사용하지 않더라도 스파크에서 기본으로 제공하기 때문에 spark-submit할 때 인자로 package를 다운받도록 하면 된다. 다만 
```
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 mongo.py
```
를 입력하거나, submit.sh를 이용하면 된다.
## 4. Metabase
Metabase는 데이터베이스를 바탕으로 시각화해주는 오픈소스 BI 툴이다. Metabase 공식 사이트에서 jar 파일을 받아 실행한다. (<https://www.metabase.com/start/oss/>)

이후 Database를 추가한다.(SparkSQL, url은 thrift 주소)
