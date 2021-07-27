     █ setup

       █ Elasticsearch index creation

         ✓ index creation checked

     █ Elasticsearch

       █ Write documentation

         ✗ status is 201
          ↳  99% — ✓ 421689 / ✗ 536
         ✗ successful:true
          ↳  99% — ✓ 421689 / ✗ 536

     █ teardown

       █ Elasticsearch index deletion

         ✓ status was 200

     checks.........................: 99.87% ✓ 843380      ✗ 1072   
     data_received..................: 178 MB 935 kB/s
     data_sent......................: 196 MB 1.0 MB/s
     group_duration.................: avg=2.78s   min=90.23ms med=1.52s max=1m27s  p(90)=5.65s   p(95)=9.94s 
     http_req_blocked...............: avg=40.47ms min=1µs     med=4µs   max=13.31s p(90)=21µs    p(95)=43µs  
     http_req_connecting............: avg=40.36ms min=0s      med=0s    max=13.31s p(90)=0s      p(95)=0s    
     http_req_duration..............: avg=2.3s    min=13.81ms med=1.29s max=59.31s p(90)=4.87s   p(95)=9.17s 
       { expected_response:true }...: avg=2.28s   min=13.81ms med=1.28s max=40s    p(90)=4.86s   p(95)=9.08s 
     http_req_failed................: 0.12%  ✓ 536         ✗ 421692 
     http_req_receiving.............: avg=21.44ms min=0s      med=35µs  max=14.21s p(90)=504µs   p(95)=1.31ms
     http_req_sending...............: avg=14.51ms min=6µs     med=31µs  max=3.22s  p(90)=18.72ms p(95)=69.7ms
     http_req_tls_handshaking.......: avg=0s      min=0s      med=0s    max=0s     p(90)=0s      p(95)=0s    
     http_req_waiting...............: avg=2.26s   min=13.6ms  med=1.26s max=59.31s p(90)=4.82s   p(95)=9.05s 
     http_reqs......................: 422228 2223.645547/s
     iteration_duration.............: avg=3.99s   min=1.09s   med=2.65s max=1m27s  p(90)=7.18s   p(95)=10.99s
     iterations.....................: 422225 2223.629747/s
     vus............................: 0      min=0         max=10000
     vus_max........................: 10000  min=10000     max=10000