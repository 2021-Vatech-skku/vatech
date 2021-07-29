import http from 'k6/http'
import { sleep, check, group } from 'k6'
import { Rate } from 'k6/metrics'
import { randomString } from "https://jslib.k6.io/k6-utils/1.1.0/index.js"
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

export let errorRate = new Rate('error')
const HOSTURL = `https://${__ENV.HOST}` // gcr.io official use tls

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