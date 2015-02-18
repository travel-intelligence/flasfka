Flasfka
=======

|Build Status| |Coverage|

Push/Pull on Kafka over HTTP

Configuration
=============

To configure how the server should talk to Kafka, the following variables
are available. Put this in a file (for example ``/etc/flasfka.conf.py``):

::

    HOSTS=["localhost:9092"]
    DEFAULT_GROUP="flasfka"
    CONSUMER_TIMEOUT=0.1
    CONSUMER_LIMIT=100

The file will be read at flasfka startup, provided you export its path:

::

    export FLASFKA_CONFIG=/etc/flasfka.conf.py

Usage
=====

Assuming flasfka is configured and running:

send
----

::

    curl -X POST --data-binary "hello world" "http://127.0.0.1:5000/my-topic/"

This pushes ``hello world`` to the topic ``my-topic``.

::

    curl -X POST --data-binary "hello again" "http://127.0.0.1:5000/my-topic/my-key/"

This pushes ``hello again`` to the topic ``my-topic`` with the key
``my-key``.

fetch
-----

::

    curl http://127.0.0.1:5000/my-topic/

This retrieves the last 100 messages posted to ``my-topic``, from the
default group ``flasfka``.

::

    curl http://127.0.0.1:5000/my-topic/?limit=20

This retrieves the last 20 messages posted to ``my-topic``, from the
default group ``flasfka``.

::

    curl http://127.0.0.1:5000/my-topic/my-group/

This retrieves the last 100 messages posted to ``my-topic``, from the group
``my-group``.

Limitations
===========

Flafska only accepts utf-8 data. If you want to pass arbitrary data, it is
better to encode it to base64 before.

.. |Build Status| image:: https://travis-ci.org/travel-intelligence/flasfka.svg?branch=master
    :target: https://travis-ci.org/travel-intelligence/flasfka

.. |Coverage| image:: https://coveralls.io/repos/travel-intelligence/flasfka/badge.svg
    :target: https://coveralls.io/r/travel-intelligence/flasfka
