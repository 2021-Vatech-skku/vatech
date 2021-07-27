     █ setup

       █ Elasticsearch index creation

         ✓ index creation checked

     █ Elasticsearch

       █ Elastic up

         ✗ status was 200
          ↳  98% — ✓ 615824 / ✗ 11311
         ✗ exist: You Know, for Search
          ↳  98% — ✓ 615824 / ✗ 11311

       █ Send documentation

         ✗ status is 201
          ↳  99% — ✓ 615719 / ✗ 101
         ✗ successful:true
          ↳  99% — ✓ 615719 / ✗ 101

     █ teardown

       █ Elasticsearch index deletion

         ✓ status was 200

     checks.........................: 99.08%  ✓ 2463088     ✗ 22824  
     data_received..................: 852 MB  2.2 MB/s
     data_sent......................: 362 MB  921 kB/s
     group_duration.................: avg=3.07s    min=2.64ms med=1.94s max=1m20s  p(90)=6.5s  p(95)=8.98s 
     http_req_blocked...............: avg=68.57ms  min=0s     med=3µs   max=28.28s p(90)=9µs   p(95)=17µs  
     http_req_connecting............: avg=68.51ms  min=0s     med=0s    max=28.27s p(90)=0s    p(95)=0s    
     http_req_duration..............: avg=2.04s    min=0s     med=1.13s max=1m4s   p(90)=4.76s p(95)=6.42s 
       { expected_response:true }...: avg=2.05s    min=2.48ms med=1.14s max=1m3s   p(90)=4.79s p(95)=6.44s 
     http_req_failed................: 0.91%   ✓ 11412       ✗ 1231546
     http_req_receiving.............: avg=955.29µs min=0s     med=37µs  max=4.39s  p(90)=324µs p(95)=823µs 
     http_req_sending...............: avg=2.43ms   min=0s     med=16µs  max=4.26s  p(90)=511µs p(95)=3.55ms
     http_req_tls_handshaking.......: avg=0s       min=0s     med=0s    max=0s     p(90)=0s    p(95)=0s    
     http_req_waiting...............: avg=2.04s    min=0s     med=1.12s max=1m4s   p(90)=4.76s p(95)=6.42s 
     http_reqs......................: 1242958 3165.164321/s
     iteration_duration.............: avg=5.66s    min=4.78ms med=4.55s max=1m21s  p(90)=9.76s p(95)=12.9s 
     iterations.....................: 627131  1596.97485/s
     vus............................: 5       min=0         max=10000
     vus_max........................: 10000   min=10000     max=10000