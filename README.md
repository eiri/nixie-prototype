# Nixie

![project: prototype](https://img.shields.io/badge/project-prototype-orange.svg)
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

## Run tests

Short `pytest`

Single suite and verbose `pytest tests/test_api.py -sv`

All with coverage `pytest --cov=nixie`

All with coverage and html report `pytest --cov=nixie --cov-report html`

## License

[MIT](https://github.com/eiri/nixie-prototype/blob/master/LICENSE "MIT License")
