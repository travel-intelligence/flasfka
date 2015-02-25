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

    curl -X POST --data-binary '{"messages": ["msg1", "msg2"]}' "http://127.0.0.1:5000/my-topic/"

This pushes ``msg1`` then ``msg2`` to the topic ``my-topic``.

::

    curl -X POST --data-binary '{"messages": ["msg3"]}' "http://127.0.0.1:5000/my-topic/my-key/"

This pushes ``msg3`` to the topic ``my-topic`` with the key ``my-key``.

fetch
-----

::

    curl http://127.0.0.1:5000/my-topic/

This retrieves a maximum of 100 of the last messages posted to
``my-topic``, from the default group ``flasfka``.

::

    curl http://127.0.0.1:5000/my-topic/my-group/

This retrieves a maximum of 100 of the last messages posted to
``my-topic``, from the group ``my-group``.

::

    curl http://127.0.0.1:5000/my-topic/?limit=20

This retrieves a maximum of 20 of the last messages posted to
``my-topic``, from the default group ``flasfka``.

Limitations
===========

Flafska only accepts json data, so your messages need to be in utf-8. If
you want to pass arbitrary data, it is recommended to encode them to a
suitable format before (e.g. base64).

See also
========

Rudimentary (fpm-based) `Debian package
<https://github.com/travel-intelligence/flasfka-deb>`_

.. |Build Status| image:: https://travis-ci.org/travel-intelligence/flasfka.svg?branch=master
    :target: https://travis-ci.org/travel-intelligence/flasfka

.. |Coverage| image:: https://coveralls.io/repos/travel-intelligence/flasfka/badge.svg
    :target: https://coveralls.io/r/travel-intelligence/flasfka
