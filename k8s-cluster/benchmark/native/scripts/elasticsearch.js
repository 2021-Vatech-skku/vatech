import http from 'k6/http'
import { sleep, check, group } from 'k6'
import { Rate } from 'k6/metrics'
import { randomString } from "https://jslib.k6.io/k6-utils/1.1.0/index.js"
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

export let errorRate = new Rate('error')
const ElasticURL = `http://${__ENV.HOST}`
const IndexName = "/k6-benchmark"

export function setup() {
  group('Elasticsearch index creation', function () {
    let params = {
      headers: {
        'Authorization': "Basic aGFydWJhbmQ6aGFydTEwMDQ=",
        'Content-Type': 'application/json'
      }
    }
    let body = JSON.stringify({
    })
    let res = http.put(ElasticURL + IndexName, body, params)
    let checkIndex = http.get(ElasticURL + IndexName, params)

    check(checkIndex, {
      'index creation checked': c => c.status == 200
    })
  })
}

export default function () {
  group('Elasticsearch', function () {
    // group('Elastic up', function () {
    //   let params = {
    //     headers: {
    //       Authorization: "Basic aGFydWJhbmQ6aGFydTEwMDQ="
    //     }
    //   }
    //   let res = http.get(ElasticURL, params)

    //   check(res, {
    //     'status was 200': res => res.status == 200,
    //     'exist: You Know, for Search': res => JSON.parse(res.body).tagline == "You Know, for Search",
    //   })
    // })

    group('Write documentation', function () {
      let params = {
        headers: {
          'Authorization': "Basic aGFydWJhbmQ6aGFydTEwMDQ=",
          'Content-type': "application/json"
        }
      }
      let body = JSON.stringify({
        'randomString1': randomString(32),
        'randomString2': randomString(32),
        'randomString3': randomString(32),
        'randomString4': randomString(32),
        'randomString5': randomString(32)
      });

      let res = http.post(ElasticURL + IndexName + '/_doc', body, params)
      check(res, {
        'status is 201': r => r.status == 201,
        'successful:true': r => JSON.parse(res.body)._shards.successful >= 1,
      }) || errorRate.add(1)
    })
  })
  sleep(1)
}

export function teardown() {
  group('Elasticsearch index deletion', function () {
    let params = {
      headers: {
        Authorization: "Basic aGFydWJhbmQ6aGFydTEwMDQ="
      }
    }
    let res = http.del(ElasticURL + IndexName, {}, params)
    check(res, {
      'status was 200': res => res.status == 200
    })
  })
}

export function handleSummary(data) {
  console.log('Preparing the end-of-test summary...');
  const jsonpath = `./result/json/${__ENV.ELASTIC_HOST}.json`
  const textpath = `./result/text/${__ENV.ELASTIC_HOST}`
  var output = {}
  output[jsonpath] = JSON.stringify(data)
  output[textpath] = textSummary(data, { indent: ' ', enableColors: false })
  output['stdout'] = textSummary(data, { indent: ' ', enableColors: true })
  return output
}