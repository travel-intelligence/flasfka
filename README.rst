Flasfka
=======

|Build Status| |Coverage|

Push/Pull on Kafka over HTTP

API
---

Send
----

    curl -X POST --data-binary "hello world" "http://127.0.0.1:5000/my-topic/"

This pushes ``hello world`` to the topic ``my-topic``.

    curl -X POST --data-binary "hello again" "http://127.0.0.1:5000/my-topic/my-key/"

This pushes ``hello again`` to the topic ``my-topic`` with the key
``my-key``.

Fetch
-----

    curl http://127.0.0.1:5000/my-topic/

This retrieves the last 20 messages posted to ``my-topic``, from the
default group ``flasfka``.

    curl http://127.0.0.1:5000/my-topic/my-group/

This retrieves the last 20 messages posted to ``my-topic``, from the group
``my-group``.

Limitations
===========

Flafska only accepts utf-8 data. If you want to pass arbitrary data, it is
better to encode it to base64 before.

.. |Build Status| image:: https://travis-ci.org/travel-intelligence/flasfka.svg?branch=master
    :target: https://travis-ci.org/travel-intelligence/flasfka

.. |Coverage| image:: https://coveralls.io/repos/travel-intelligence/flasfka/badge.svg
    :target: https://coveralls.io/r/travel-intelligence/flasfka
