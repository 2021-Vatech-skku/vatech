APP=${1:-nginx}
VUS=${2:-3000}
DURATION=${3:-3m}

BENCHMARK_PATH=.
MANIFESTS_PATH=${BENCHMARK_PATH}/deploy/manifests
VALUE_FILE=${MANIFESTS_PATH}/istio/charts/gateways/istio-ingress/values.yaml

BENCHMARK_SCRIPT=scripts/${APP}.js
SCRIPT_BASENAME=${BENCHMARK_SCRIPT##*/}
SCRIPT_BASENAME=${SCRIPT_BASENAME%.js}

PWD=`pwd`


echo "Starting istio-cpu benchmark using ${BENCHMARK_SCRIPT} with vus ${VUS}, duration ${DURATION}."

setup() {    
    kubectl apply -f ${MANIFESTS_PATH}/${APP}/ -n benchmark > /dev/null
    echo "Waiting for deployment ready.."
    kubectl wait -f ${MANIFESTS_PATH}/${APP}/deployment.yaml --for condition=available --timeout=3m > /dev/null
    sleep 3
}

istio_bench() {
    setup
    echo "istio Benchmark"
    HOST=istio.k8s.com
    docker-compose run -v ${PWD}/scripts:/scripts \
        k6 run /scripts/${APP}.js \
        --vus $VUS --duration $DURATION \
        -e HOST=$HOST -e ING_CTRL=istio \
        --insecure-skip-tls-verify

    kubectl delete -f ${MANIFESTS_PATH}/${APP}/deployment.yaml --grace-period=20 > /dev/null
}

bench() {
    echo "benchmark with $1 cpu.."
    echo "Waiting for upgrade.."
    sed -i '' 's/cpu: [0-9][0-9]*m/cpu: '"$1"'/' $VALUE_FILE
    helm upgrade istio-ingress deploy/manifests/istio/charts/gateways/istio-ingress > /dev/null
    echo "Upgrade Complete."
    echo "Waiting for ingress controller ready.."
    sleep 10
    kubectl wait pod -n benchmark -l app=istio-ingressgateway --timeout=5m --for condition=ready > /dev/null
    echo "Ingress controller pod ready."
    istio_bench
}

cpu_list=(
    200m
    300m
    400m
    500m
)

for vcpu in ${cpu_list[@]}; do
    clear
    bench $vcpu
    echo "Cleaning up and Cool down.."
    sleep 60
done

kubectl delete -f ${MANIFESTS_PATH}/${APP} -n benchmark > /dev/null