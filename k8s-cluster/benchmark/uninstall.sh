helm uninstall haproxy-ingress
helm uninstall nginx-ingress
helm uninstall istio-ingress

ISTIO_IP=`kubectl get svc -n benchmark istio-ingressgateway -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`
NGINX_IP=`kubectl get svc -n benchmark nginx-ingress-ingress-nginx-controller -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`
HAPROXY_IP=`kubectl get svc -n benchmark haproxy-ingress-kubernetes-ingress -o jsonpath="{.status.loadBalancer.ingress[0].ip}"`

sudo sed -i'.back' "/${ISTIO_IP} istio.k8s.com/d" /etc/hosts
sudo sed -i'.back' "/${NGINX_IP} nginx.k8s.com/d" /etc/hosts
sudo sed -i'.back' "/${HAPROXY_IP} haproxy.k8s.com/d" /etc/hosts

kubectl delete ns benchmark