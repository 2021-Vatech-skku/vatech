# VATECH Junhyun
------------------
## Kafka cluster 구성하기
kafka cluster는 보통 kafka(broker) 여러 대와 zookeeper 여러대로 구성된다. 물론 단일 kafka, zookeeper로 구성할 수 있다.

테스트를 위해 docker 환경에서 먼저 kafka cluster를 구성해보았다.
docker에 여러 컨테이너를 올리기에 용이한 docker-compose 방법을 썼다.
[단일 kafka, 단일 zookeeper 구성 yaml 파일](https://github.com/JackCokebb/kafka-all/blob/master/kafkaServer/docker-compose-lone.yml)

docker가 설치되어있다는 가정하에, docker를 작동시키고, terminal에서 코드를 실행시킨다.
``` 
//f: 파일명 지정, -d : background 실행
docker-compose -f docker-compose-lone.yml up -d
```

docker 프로그램으로 확인시, container들이 잘 올라간 것을 확인할 수 있다.
--------------
kafka에서 제공하는 shell 파일 내에 [kafka-console-consumer.sh, kafka-console-consumer.sh](https://kafka.apache.org/quickstart)로도 kafka 정상 작동 여부를 확인할 수 있지만,
[python code](https://github.com/2021-Vatech-skku/vatech/tree/junhyun/kafkaClients)를 이용해서 확인할 수 있다.

vscode와 같은 코드 에디터에서 실행해도 되고, terminal을 이용해도 된다.
python 3.x 이상 버전을 사용했다.
```bash
//python producer로 data를 kafka에 전송
python3 sample-producer.py

//python consumer로 data consume test
python3 sample-consumer.py

//실행시 port number, topic name, bootstrap.server 설정 등에 주의한다. 
//개인 설정에 맞게 실행
```

