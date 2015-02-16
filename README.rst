Flasfka
=======

Push/Pull on Kafka over HTTP

API
===

Send
----

    curl -X POST --data-binary "hello world" http://127.0.0.1:5000/my-topic/"

This pushes `hello world` to the topic `my-topic`.

    curl -X POST --data-binary "hello again" http://127.0.0.1:5000/my-topic/my-key/"

This pushes `hello again` to the topic `my-topic` with the key `my-key`

Fetch
-----

    curl http://127.0.0.1:5000/my-topic/

This retrieves the last 20 messages posted to `my-topic`, from the default
group `flasfka`.

    curl http://127.0.0.1:5000/my-topic/my-group/

This retrieves the last 20 messages posted to `my-topic`, from the group
`my-group`.
