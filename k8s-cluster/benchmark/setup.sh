# !/bin/bash
# 외부 IP 여분 있는지 확인 필요함.
docker-compose up -d influxdb grafana
kubectl create ns benchmark --dry-run=client -o yaml | kubectl apply -f -
echo "Installing ingress controller.."
helm install haproxy-ingress deploy/manifests/controller/haproxy/charts -n benchmark
helm install nginx-ingress deploy/manifests/controller/nginx/charts -n benchmark
helm install istio-ingress deploy/manifests/controller/istio/charts -n benchmark

sleep 3

ISTIO_IP=`kubectl get svc -n benchmark istio-ingressgateway -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`
NGINX_IP=`kubectl get svc -n benchmark nginx-ingress-ingress-nginx-controller -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`
HAPROXY_IP=`kubectl get svc -n benchmark haproxy-ingress-kubernetes-ingress -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`

echo "${ISTIO_IP} istio.k8s.com" >> /etc/hosts
echo "${NGINX_IP} nginx.k8s.com" >> /etc/hosts
echo "${HAPROXY_IP} haproxy.k8s.com" >> /etc/hosts

kubectl apply -f deploy/manifests/ingress/haproxy.yaml -n benchmark
kubectl apply -f deploy/manifests/ingress/nginx.yaml -n benchmark
kubectl apply -f deploy/manifests/ingress/istio.yaml -n benchmark