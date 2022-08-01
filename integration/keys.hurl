# empty keys list
GET http://127.0.0.1:7312

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
body matches "^$"


# create counter
POST http://127.0.0.1:7312

HTTP/1.1 201
[Captures]
key1: body


# check key in the list
GET http://127.0.0.1:7312

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
body matches "^\\w{21}$"


# create second counter
POST http://127.0.0.1:7312

HTTP/1.1 201
[Captures]
key2: body


# check two keys in the list
GET http://127.0.0.1:7312

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
body matches "^\\w{21}\\n\\w{21}$"


# delete first key
DELETE http://127.0.0.1:7312/{{key1}}

HTTP/1.1 204


# confim one key in the list
GET http://127.0.0.1:7312

HTTP/1.1 200
[Asserts]
header "Content-Type" contains "text/plain"
body matches "^\\w{21}$"


# delete second key
DELETE http://127.0.0.1:7312/{{key2}}

HTTP/1.1 204


# confirm no keys in the list
GET http://127.0.0.1:7312

HTTP/1.1 200
[Asserts]
body matches "^$"
