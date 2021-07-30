import http from 'k6/http'
import { sleep, check, group } from 'k6'
import { Rate } from 'k6/metrics'

export let errorRate = new Rate('error')
export let v1Rate = new Rate('v1')
export let v2Rate = new Rate('v2')

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
    errorRate.add(res.status != 200)
    v1Rate.add(res.body == 1)
    v2Rate.add(res.body == 2)
    sleep(1)
}