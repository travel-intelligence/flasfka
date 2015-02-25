# -*- coding: utf-8 -*-

from __future__ import with_statement
from flasfka import app, __version__
import flask
import kafka
import json


app.config.update(dict(
    HOSTS=["localhost:9092"],
    DEFAULT_GROUP="flasfka",
    CONSUMER_TIMEOUT=0.1,
    CONSUMER_LIMIT=100
))

app.config.from_envvar("FLASFKA_CONFIG", silent=True)


def get_kafka_client():
    if not hasattr(flask.g, "kafka_client"):
        flask.g.kafka_client = kafka.KafkaClient(app.config["HOSTS"])
    return flask.g.kafka_client


def get_kafka_producer():
    if not hasattr(flask.g, "kafka_producer"):
        client = get_kafka_client()
        flask.g.kafka_producer = kafka.KeyedProducer(client)
    return flask.g.kafka_producer


def get_kafka_consumer(group, topic):
    client = get_kafka_client()
    return kafka.SimpleConsumer(
        client, group, topic,
        iter_timeout=app.config["CONSUMER_TIMEOUT"]
    )


def produce(topic, messages, key=None):
    producer = get_kafka_producer()
    for message in messages:
        if type(message) not in (unicode, str):
            raise TypeError
        producer.send(topic, key, message.encode("utf-8"))
    producer.stop()


def consume(topic, group, limit):
    if group is None:
        group = app.config["DEFAULT_GROUP"].encode("utf-8")
    consumer = get_kafka_consumer(group, topic)
    res = {"group": group.decode("utf-8"), "messages": []}
    for n, message in enumerate(consumer):
        res["messages"].append(message.message.value.decode("utf-8"))
        if n >= limit - 1:
            break
    consumer.commit()
    consumer.stop()
    return res


@app.route("/<topic>/", methods=["GET", "POST"])
@app.route("/<topic>/<group_or_key>/", methods=["GET", "POST"])
def flasfka(topic, group_or_key=None):
    topic = topic.encode("utf-8")
    if group_or_key is not None:
        group_or_key = group_or_key.encode("utf-8")

    client = get_kafka_client()
    client.ensure_topic_exists(topic)

    if flask.request.method == "GET":
        limit = int(flask.request.args.get(
            "limit", app.config["CONSUMER_LIMIT"]
            ))
        group = group_or_key
        return flask.jsonify(consume(topic, group, limit))
    if flask.request.method == "POST":
        key = group_or_key
        data = flask.request.get_json(force=True)
        try:
            produce(topic, data["messages"], key)
            return flask.make_response(("", 204, {}))
        except (KeyError, TypeError):
            return flask.make_response((
                'expected format: {"messages": ["message1", ...]}',
                400,
                {}
            ))

# Snippet to attach the version to every request
@app.after_request
def add_version_header(response):
    response.headers["X-Flasfka-Version"] = __version__
    return response
