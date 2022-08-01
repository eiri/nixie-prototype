# create counter
POST http://127.0.0.1:7312

HTTP/1.1 201
[Captures]
key: body
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "1"
header "Nixie-Name" not exists
header "Nixie-Description" not exists
body matches "^\\w{21}$"


# check counter
HEAD http://127.0.0.1:7312/{{key}}

HTTP/1.1 204
[Asserts]
header "Content-Type" not exists
header "Nixie-Step" == "1"
header "Nixie-Name" not exists
header "Nixie-Description" not exists
``````

# read counter
GET http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "1"
header "Nixie-Name" not exists
header "Nixie-Description" not exists
```0```


# update counter
POST http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "1"
header "Nixie-Name" not exists
header "Nixie-Description" not exists
```1```


# update counter again
POST http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "1"
header "Nixie-Name" not exists
header "Nixie-Description" not exists
```2```


# delete counter
DELETE http://127.0.0.1:7312/{{key}}

HTTP/1.1 204
[Asserts]
header "Content-Type" not exists
header "Nixie-Step" not exists
header "Nixie-Name" not exists
header "Nixie-Description" not exists
body matches "^$"


# confirm counter deleted
GET http://127.0.0.1:7312/{{key}}

HTTP/1.1 *
[Asserts]
status == 404


# confirm counter can't be deleted again
DELETE http://127.0.0.1:7312/{{key}}

HTTP/1.1 *
[Asserts]
status == 404
