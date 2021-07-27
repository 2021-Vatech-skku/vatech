     █ setup

       █ Elasticsearch index creation

         ✓ index creation checked

     █ Elasticsearch

       █ Elastic up

         ✗ status was 200
          ↳  99% — ✓ 636885 / ✗ 5496
         ✗ exist: You Know, for Search
          ↳  99% — ✓ 636885 / ✗ 5496

       █ Send documentation

         ✗ status is 201
          ↳  99% — ✓ 636844 / ✗ 41
         ✗ successful:true
          ↳  99% — ✓ 636844 / ✗ 41

     █ teardown

       █ Elasticsearch index deletion

         ✓ status was 200

     checks.........................: 99.56%  ✓ 2547460     ✗ 11074  
     data_received..................: 752 MB  2.0 MB/s
     data_sent......................: 382 MB  1.0 MB/s
     group_duration.................: avg=3s       min=2.72ms med=1.78s max=1m39s  p(90)=6.71s p(95)=9s    
     http_req_blocked...............: avg=5.75ms   min=0s     med=3µs   max=16.37s p(90)=7µs   p(95)=13µs  
     http_req_connecting............: avg=5.74ms   min=0s     med=0s    max=16.35s p(90)=0s    p(95)=0s    
     http_req_duration..............: avg=2.04s    min=0s     med=1.13s max=1m1s   p(90)=4.83s p(95)=7.14s 
       { expected_response:true }...: avg=2.05s    min=2.56ms med=1.14s max=59.66s p(90)=4.85s p(95)=7.15s 
     http_req_failed................: 0.43%   ✓ 5537        ✗ 1273732
     http_req_receiving.............: avg=772.84µs min=0s     med=35µs  max=3.47s  p(90)=250µs p(95)=584µs 
     http_req_sending...............: avg=1.87ms   min=0s     med=16µs  max=2.39s  p(90)=368µs p(95)=2.88ms
     http_req_tls_handshaking.......: avg=0s       min=0s     med=0s    max=0s     p(90)=0s    p(95)=0s    
     http_req_waiting...............: avg=2.04s    min=0s     med=1.13s max=1m1s   p(90)=4.83s p(95)=7.14s 
     http_reqs......................: 1279269 3407.53287/s
     iteration_duration.............: avg=5.56s    min=1.2s   med=4.25s max=1m39s  p(90)=9.77s p(95)=12.16s
     iterations.....................: 642381  1711.082167/s
     vus............................: 0       min=0         max=10000
     vus_max........................: 10000   min=10000     max=10000