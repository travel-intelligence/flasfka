flasfka
=======

|Build Status| |Coverage|

Push/Pull on Kafka over HTTP

Installation
============

You can install kafka with pip:

::

    pip install kafka

Alternatively, you can build and use the `debian package
<https://github.com/travel-intelligence/flasfka-deb>`_

Configuration
=============

The second step is to set up flasfka to talk to the Kafka cluster. To do
so, the following variables are available. Put this in a file (for example
``/etc/flasfka.conf.py``):

::

    # Hosts in the kafka cluster (list of ip:port)
    HOSTS=["localhost:9092"]

    # What group to use when listening to a topic
    DEFAULT_GROUP="flasfka"

    # How long to wait when polling a topic for new messages
    CONSUMER_TIMEOUT=0.1

    # Maximum of messages returned when consuming from a topic
    CONSUMER_LIMIT=100

The file will be read at flasfka startup, provided it is in the
environment variable ``FLASFKA_CONFIG``:

::

    export FLASFKA_CONFIG=/etc/flasfka.conf.py

Usage
=====

Now, assuming flasfka is configured and running:

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

.. |Build Status| image:: https://travis-ci.org/travel-intelligence/flasfka.svg?branch=master
    :target: https://travis-ci.org/travel-intelligence/flasfka

.. |Coverage| image:: https://coveralls.io/repos/travel-intelligence/flasfka/badge.svg
    :target: https://coveralls.io/r/travel-intelligence/flasfka
