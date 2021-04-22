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

| Method   | Path                | Description             |
| -------- | ------------------- | ----------------------- |
| `GET`    | `/`                 | list of counters        |
| `POST`   | `/`                 | create new counter      |
| `HEAD`   | `/{key}`            | check if counter exists |
| `GET`    | `/{key}`            | read counter            |
| `PUT`    | `/{key}/incr`       | increase counter by 1   |
| `PUT`    | `/{key}/incr/{val}` | increase counter by val |
| `PUT`    | `/{key}/decr`       | decrease counter by 1   |
| `PUT`    | `/{key}/decr/{val}` | decrease counter by val |
| `DELETE` | `/{key}`            | delete counter          |

_Note: Content-Type for all the requests is `text/plain`_

## Run tests
`pytest`

## License

[MIT](https://github.com/eiri/nixie/blob/master/LICENSE "MIT License")
