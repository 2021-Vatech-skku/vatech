#!/bin/bash

BENCHMARK_SCRIPT=scripts/echoserver.js
SCRIPT_BASENAME=${BENCHMARK_SCRIPT##*/}
SCRIPT_BASENAME=${SCRIPT_BASENAME%.js}
VUS=${1:-1000}
DURATION=${2:-3m}
HOST=benchmark.k8s.com

echo "Starting benchmark using ${BENCHMARK_SCRIPT} with vus ${VUS}, duration ${DURATION}."

setup() { 
  helm repo add haproxy-ingress https://haproxy-ingress.github.io/charts > /dev/null
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx > /dev/null
  helm repo update > /dev/null

  kubectl create ns benchmark --dry-run -o yaml | kubectl apply -f - > /dev/null
  kubectl config set-context --current --namespace=benchmark > /dev/null

  kubectl apply -f deploy/manifests/service.yaml > /dev/null
  kubectl apply -f deploy/manifests/deployment.yaml > /dev/null
  echo "Waiting for deployment ready.."
  kubectl wait -f deploy/manifests/deployment.yaml --for condition=available --timeout=3m > /dev/null
  mkdir -p ./result
  mkdir -p ./result/echoserver
  mkdir -p ./result/echoserver/json/
  mkdir -p ./result/echoserver/text/
  sleep 5

}

haproxy_bench() {
  echo "--- HAproxy Benchmark"
  echo "installing HAproxy ingress.."
  helm install haproxy-ingress haproxy-ingress/haproxy-ingress \
    --namespace benchmark \
    --set resources.limits.cpu=2000m \
    --set resources.limits.memory=1024Mi > /dev/null 2>&1
  sleep 3
  kubectl apply -f deploy/manifests/ingress/haproxy.yaml -n benchmark > /dev/null
  
  echo "Waiting for haproxy controller ready.."
  kubectl wait pod -n benchmark -l app.kubernetes.io/name=haproxy-ingress --for condition=ready --timeout=5m > /dev/null
  sleep 10
  
  echo "Starting haproxy bench."
  k6 run $BENCHMARK_SCRIPT \
    --vus $VUS --duration $DURATION \
    -e HOST=$HOST -e ING_CTRL=haproxy \
    --out json=echoserver_haproxy.json \
    --insecure-skip-tls-verify

  echo "\nCleanup.."
  kubectl delete -f deploy/manifests/ingress/haproxy.yaml -n benchmark > /dev/null
  helm uninstall haproxy-ingress > /dev/null
  sleep 10
}

nginx_bench() {
  echo "--- NGINX Benchmark"
  echo "installing nginx ingress.."
  helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace benchmark \
    --set resources.limits.cpu=2000m \
    --set resources.limits.memory=1024Mi > /dev/null 2>&1

  sleep 5
  kubectl apply -f deploy/manifests/ingress/nginx.yaml -n benchmark --timeout 20s > /dev/null
  
  echo "Waiting for nginx controller ready.."
  kubectl wait pod -n benchmark -l app.kubernetes.io/name=ingress-nginx --timeout=5m --for condition=ready > /dev/null
  sleep 10

  echo "Starting nginx bench."
  k6 run $BENCHMARK_SCRIPT \
    --vus $VUS --duration $DURATION \
    -e HOST=$HOST -e ING_CTRL=nginx \
    --out json=echoserver_nginx.json \
    --insecure-skip-tls-verify

  echo "\nCleanup.."
  kubectl delete -f deploy/manifests/ingress/nginx.yaml -n benchmark > /dev/null
  helm uninstall ingress-nginx > /dev/null
  sleep 10
}

istio_bench() {
  echo "--- Istio Benchmark"
  echo "installing istio ingress.."
  helm install istio-ingress deploy/manifests/istio/charts/gateways/istio-ingress \
    -n benchmark > /dev/null 2>&1
  sleep 3
  kubectl apply -f deploy/manifests/ingress/istio.yaml -n benchmark > /dev/null

  echo "Waiting for istio controller ready.."
  kubectl wait pod -n benchmark -l app=istio-ingressgateway --timeout=5m --for condition=ready > /dev/null
  sleep 10

  echo "Starting istio bench."
  k6 run $BENCHMARK_SCRIPT \
    --vus $VUS --duration $DURATION \
    -e HOST=$HOST -e ING_CTRL=istio \
    --out json=echoserver_istio.json \
    --insecure-skip-tls-verify

  echo "\nCleanup.."
  kubectl delete -f deploy/manifests/ingress/istio.yaml -n benchmark > /dev/null
  helm delete istio-ingress -n benchmark > /dev/null
  sleep 10
}

teardown() {
  echo "Finishing all jobs.."
  helm repo remove haproxy-ingress > /dev/null
  helm repo remove ingress-nginx > /dev/null
  kubectl delete -f deploy/manifests/deployment.yaml > /dev/null
  kubectl delete -f deploy/manifests/service.yaml > /dev/null
  kubectl config set-context --current --namespace=default > /dev/null
}

setup
haproxy_bench
nginx_bench
istio_bench
teardown
exit