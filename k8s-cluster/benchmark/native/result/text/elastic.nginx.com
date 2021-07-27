     █ setup

       █ Elasticsearch index creation

         ✓ index creation checked

     █ Elasticsearch

       █ Write documentation

         ✗ status is 201
          ↳  99% — ✓ 462988 / ✗ 15
         ✗ successful:true
          ↳  99% — ✓ 462988 / ✗ 15

     █ teardown

       █ Elasticsearch index deletion

         ✓ status was 200

     checks.........................: 99.99% ✓ 925978      ✗ 30     
     data_received..................: 242 MB 1.3 MB/s
     data_sent......................: 212 MB 1.1 MB/s
     group_duration.................: avg=2.34s   min=92.9ms med=1.36s max=1m4s   p(90)=5.2s   p(95)=7.54s  
     http_req_blocked...............: avg=37.87ms min=1µs    med=4µs   max=9.04s  p(90)=22µs   p(95)=46µs   
     http_req_connecting............: avg=37.72ms min=0s     med=0s    max=9.04s  p(90)=0s     p(95)=0s     
     http_req_duration..............: avg=1.66s   min=5.28ms med=1.07s max=1m0s   p(90)=3.6s   p(95)=4.39s  
       { expected_response:true }...: avg=1.66s   min=5.28ms med=1.07s max=59.72s p(90)=3.6s   p(95)=4.39s  
     http_req_failed................: 0.00%  ✓ 15          ✗ 462991 
     http_req_receiving.............: avg=2.95ms  min=0s     med=37µs  max=5.44s  p(90)=473µs  p(95)=1.29ms 
     http_req_sending...............: avg=22.33ms min=6µs    med=34µs  max=4s     p(90)=38.1ms p(95)=96.67ms
     http_req_tls_handshaking.......: avg=0s      min=0s     med=0s    max=0s     p(90)=0s     p(95)=0s     
     http_req_waiting...............: avg=1.63s   min=5.11ms med=1.04s max=1m0s   p(90)=3.56s  p(95)=4.37s  
     http_reqs......................: 463006 2432.996333/s
     iteration_duration.............: avg=3.64s   min=1.09s  med=2.51s max=1m6s   p(90)=7.14s  p(95)=9.28s  
     iterations.....................: 463003 2432.980569/s
     vus............................: 0      min=0         max=10000
     vus_max........................: 10000  min=10000     max=10000