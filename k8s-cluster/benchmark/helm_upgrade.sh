helm upgrade haproxy-ingress deploy/manifests/haproxy/charts
helm upgrade istio-ingress deploy/manifests/istio/charts/gateways/istio-ingress
helm upgrade ingress-nginx deploy/manifests/ingress-nginx/charts

