import http from 'k6/http'
import { sleep, check, group } from 'k6'
import { Rate } from 'k6/metrics'

export let errorRate = new Rate('error')
const HOSTURL = `https://${__ENV.HOST}` // gcr.io official use tls

export let options = {
    stages: [
        {duration: '10s', target: 500}, 
        {duration: '1m', target: 500}, 
        {duration: '10s', target: 5000}, 
        {duration: '3m', target: 5000},
        {duration: '10s', target: 100}, 
        {duration: '1m', target: 100},
        {duration: '10s', target: 0}, 
    ]
}

export function setup() {

}

export default function() {
    let params = {
        timeout: "180s"
    }
    var res = http.get(HOSTURL, params)
    group('echoserver', function() {
        check(res, {
            "Status was 200": (res) => res.status == 200,
        })
    })
    if (res.status != 200) errorRate.add(1)
    sleep(1)
}