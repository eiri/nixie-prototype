# Nixie

![project: prototype](https://img.shields.io/badge/project-prototype%3A0.3.0-orange)
[![Build Status](https://github.com/eiri/nixie-prototype/workflows/build/badge.svg)](https://github.com/eiri/nixie-prototype/actions)

## Overview

Service that allows to create, update and delete counters.

## tl;dr

```bash
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ pytest
$ ./bin/nixie-cli -d
```

## Setup
Make and activate venv. Then `pip install -r requirements.txt`

## Run server
```bash
$ ./bin/nixie-cli -h
Usage: nixie-cli [OPTIONS]

  Start Nixie server

Options:
  --version           Show the version and exit.
  -p, --port INTEGER  server port
  -d, --debug         run server in debug mode
  -h, --help          Show this message and exit.

$ ./bin/nixie-cli -d
 * Running on http://127.0.0.1:7312/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 140-209-625
127.0.0.1 - - [03/Nov/2017 11:20:36] "POST / HTTP/1.1" 201 -
127.0.0.1 - - [03/Nov/2017 11:20:45] "GET /7ybcVEkCLNcdD9X3zGMid HTTP/1.1" 200 -
...
```

### REST API

| Method   | Path     | Description
| -------- | -------- | -----------------------
| `GET`    | `/`      | List all counters' keys.
| `POST`   | `/`      | Create a new coutner.
| `HEAD`   | `/{key}` | Check if a specific counter exists.
| `GET`    | `/{key}` | Return a value of a specific counter.
| `POST`   | `/{key}` | Increase or decrease a specific counter on its step and return an updated value.
| `PATCH`  | `/{key}` | Update metadata for a specific counter.
| `DELETE` | `/{key}` | Delete a specific counter.

For more details read [OpenAPI specs](https://github.com/eiri/nixie-prototype/blob/master/openapi.yaml "OpenAPI specs")

## Lint

Install [ruff](https://beta.ruff.rs/docs/) with `pip install ruff` then run `ruff check .`

To autofix problems run `russ check . --fix`, ruff's pretty good with that.

## Run unit tests

Short `pytest`

Single suite and verbose `pytest tests/test_api.py -sv`

All with coverage `pytest --cov=nixie`

All with coverage and html report `pytest --cov=nixie --cov-report html`


## Run integration tests

Install [hurl](https://hurl.dev) either with `brew` or with `asdf`.

Start nixie in one terminal with `./bin/nixie-cli -d`

Then run `hurl --test ./integration/*.hurl`

```
$ hurl --test ./integration/*.hurl
./integration/01-keys.hurl: Running [1/3]
./integration/01-keys.hurl: Success (9 request(s) in 23 ms)
./integration/02-basic.hurl: Running [2/3]
./integration/02-basic.hurl: Success (8 request(s) in 7 ms)
./integration/03-complex.hurl: Running [3/3]
./integration/03-complex.hurl: Success (9 request(s) in 6 ms)
--------------------------------------------------------------------------------
Executed files:  3
Succeeded files: 3 (100.0%)
Failed files:    0 (0.0%)
Duration:        37 ms
```

## Run benchmark

Install [k6](https://k6.io) either with `brew` or with `asdf`.

Start nixie in one terminal with `./bin/nixie-cli -d`

Then run ` k6 run benchmark/script.js`

```
$ k6 run benchmark/script.js

          /\      |‾‾| /‾‾/   /‾‾/
     /\  /  \     |  |/  /   /  /
    /  \/    \    |     (   /   ‾‾\
   /          \   |  |\  \ |  (‾)  |
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: benchmark/script.js
     output: -

  scenarios: (100.00%) 1 scenario, 3 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1000 iterations shared among 3 VUs (maxDuration: 10m0s, gracefulStop: 30s)


     ✓ status 200
     ✓ counter match

     █ setup

     checks.........................: 100.00% ✓ 3000        ✗ 0
     data_received..................: 433 kB  697 kB/s
     data_sent......................: 320 kB  515 kB/s
     http_req_blocked...............: avg=81.24µs  min=40µs     med=79µs    max=1.26ms   p(90)=108µs  p(95)=118µs
     http_req_connecting............: avg=67.69µs  min=32µs     med=65µs    max=655µs    p(90)=94µs   p(95)=104µs
     http_req_duration..............: avg=500.74µs min=175µs    med=519µs   max=2.78ms   p(90)=648µs  p(95)=692µs
       { expected_response:true }...: avg=500.74µs min=175µs    med=519µs   max=2.78ms   p(90)=648µs  p(95)=692µs
     http_req_failed................: 0.00%   ✓ 0           ✗ 2500
     http_req_receiving.............: avg=17.78µs  min=6µs      med=16µs    max=744µs    p(90)=23µs   p(95)=27.04µs
     http_req_sending...............: avg=12.78µs  min=4µs      med=11µs    max=903µs    p(90)=16µs   p(95)=20µs
     http_req_tls_handshaking.......: avg=0s       min=0s       med=0s      max=0s       p(90)=0s     p(95)=0s
     http_req_waiting...............: avg=470.16µs min=149µs    med=489.5µs max=2.75ms   p(90)=617µs  p(95)=662µs
     http_reqs......................: 2500    4026.763481/s
     iteration_duration.............: avg=1.51ms   min=893.41µs med=1.3ms   max=167.69ms p(90)=1.52ms p(95)=1.59ms
     iterations.....................: 1000    1610.705392/s


running (00m00.6s), 0/3 VUs, 1000 complete and 0 interrupted iterations
default ✓ [======================================] 3 VUs  00m00.5s/10m0s  1000/1000 shared iters
```

## License

[MIT](https://github.com/eiri/nixie-prototype/blob/main/LICENSE "MIT License")
