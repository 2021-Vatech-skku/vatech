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
    var res = http.get(HOSTURL)
    group('echoserver', function() {
        check(res, {
            "Status was 200": (res) => res.status == 200,
        })
    })
    sleep(.1)
}

export function handleSummary(data) {
    console.log('Preparing the end-of-test summary...');
    const jsonpath = `./result/echoserver/json/${__ENV.ING_CTRL}.json`
    const textpath = `./result/echoserver/text/${__ENV.ING_CTRL}`
    var output = {}
    output[jsonpath] = JSON.stringify(data)
    output[textpath] = textSummary(data, { indent: ' ', enableColors: false })
    output['stdout'] = textSummary(data, { indent: ' ', enableColors: true })
    return output
  }