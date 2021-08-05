# VATECH Junhyun
------------------
##Kafka cluster 구성하기
kafka cluster는 보통 kafka(broker) 여러 대와 zookeeper 여러대로 구성된다. 물론 단일 kafka, zookeeper로 구성할 수 있다.

테스트를 위해 docker 환경에서 먼저 kafka cluster를 구성해보았다.
docker에 여러 컨테이너를 올리기에 용이한 docker-compose 방법을 썼다.
[단일 kafka, 단일 zookeeper 구성 yaml 파일]<https://github.com/JackCokebb/kafka-all/blob/master/kafkaServer/docker-compose-lone.yml>

docker가 설치되어있다는 가정하에, docker를 작동시키고, terminal에서 코드를 실행시킨다.
``` 
docker-compose -f docker-compose-lone.yml up -d
//-f: 파일명 지정, -d : background 실행
```
