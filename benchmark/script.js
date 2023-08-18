import http from 'k6/http';
import {check} from "k6";

// docker run -i --rm --net=host loadimpact/k6 run --vus 1 --iterations 100 - <script.js

// const url = 'http://192.168.1.95:7312';
const url = 'http://127.0.0.1:7312';

export let options = {
    vus: 3,
    iterations: 1000,
    noConnectionReuse: true,
}

export function setup() {
    let keys = new Array();
    for (let id = 1; id <= 500; id++) {
        let res = http.post(url);
        keys.push(res.body);
    }
    return keys
}

export default function(keys) {
    let key = keys[Math.floor(Math.random() * keys.length)];
    let res = http.post(url + '/' + key);
    check(res, {"status 200": (r) => r.status === 200})
    let newVal = res.body

    res = http.get(url + '/' + key);
    check(res, {
        "status 200": (r) => r.status === 200,
        "counter match": (r) => r.body === newVal
    })
    // console.log('>>' + res.status + ' - ' + res.body);
}
