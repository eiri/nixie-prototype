# Nixie

![project: prototype](https://img.shields.io/badge/project-prototype-orange.svg)
[![Build Status](https://github.com/eiri/nixie-prototype/actions)](https://github.com/eiri/nixie-prototype/workflows/build/badge.svg)

## Overview

Service that allows to create, update and delete counters.

## tl;dr

```bash
$ python3 -m venv venv
$ . ./venv/bin/activate
$ python3 -m pip install --upgrade pip
$ pip3 install -r requirements.txt
$ pip3 install pytest
$ pytest
$ ./bin/nixie-server -d
```

## Setup
Make and activate venv. Then `pip install -r requirements.txt`

## Run server
```bash
$ ./bin/nixie-server -h
usage: nixie-server [-h] [-p PORT] [-d]

Start nixie server

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
  -d, --debug

$ ./bin/nixie-server -d
 * Running on http://127.0.0.1:7312/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 140-209-625
127.0.0.1 - - [03/Nov/2017 11:20:36] "POST / HTTP/1.1" 201 -
127.0.0.1 - - [03/Nov/2017 11:20:45] "GET /0e0d53f462784748a54f7526f265fc92 HTTP/1.1" 200 -
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
| `PUT`    | `/{key}/{val}`      | set counter to val      |
| `DELETE` | `/{key}`            | delete counter          |

_Note: Content-Type for all the requests is `text/plain`_

## Run tests
`pytest`

## License

[MIT](https://github.com/eiri/nixie/blob/master/LICENSE "MIT License")
