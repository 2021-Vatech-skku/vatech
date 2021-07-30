# Ingress Controller benchmark

## setup
```
sudo sh setup.sh
```
---
## benchmark
benchmark 폴더에서 돌려야 합니다.  
Ingress controller - service ip는 직접 매핑해줘야 합니다 (i.e. /etc/hosts)
### load test
```
sh shell/benchmark.sh 
```
### load test - with custom app

```
#                      APP  VU   Duration
sh shell/benchmark.sh nginx 3000 3m
```
---
## Uninstall
```
sh uninstall.sh
```