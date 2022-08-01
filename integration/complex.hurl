# create counter
POST http://127.0.0.1:7312
content-type: "text/plain"
nixie-step: 4
nixie-name: Quoter
nixie-description: A counter with step 4
3

HTTP/1.1 201
[Captures]
key: body
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "4"
header "Nixie-Name" == "Quoter"
header "Nixie-Description" == "A counter with step 4"
body matches "^\\w{21}$"


# check counter
HEAD http://127.0.0.1:7312/{{key}}

HTTP/1.1 204
[Asserts]
header "Content-Type" not exists
header "Nixie-Step" == "4"
header "Nixie-Name" == "Quoter"
header "Nixie-Description" == "A counter with step 4"
``````


# read counter
GET http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "4"
header "Nixie-Name" == "Quoter"
header "Nixie-Description" == "A counter with step 4"
```3```


# update counter
POST http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "4"
header "Nixie-Name" == "Quoter"
header "Nixie-Description" == "A counter with step 4"
```7```


# patch counter
PATCH http://127.0.0.1:7312/{{key}}
content-type: "text/plain"
nixie-step: 5
nixie-name: Quiter
nixie-description: A counter with step 5


HTTP/1.1 204
[Asserts]
header "Content-Type" not exists
header "Nixie-Step" == "5"
header "Nixie-Name" == "Quiter"
header "Nixie-Description" == "A counter with step 5"
``````


# update counter again
POST http://127.0.0.1:7312/{{key}}

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
header "Nixie-Step" == "5"
header "Nixie-Name" == "Quiter"
header "Nixie-Description" == "A counter with step 5"
```12```


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
