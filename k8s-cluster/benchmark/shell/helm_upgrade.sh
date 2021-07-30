helm upgrade haproxy-ingress ../deploy/manifests/controller/haproxy/charts
helm upgrade istio-ingress ../deploy/manifests/contorller/istio/charts
helm upgrade ingress-nginx ../deploy/manifests/contorller/nginx/charts