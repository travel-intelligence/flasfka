# -*- coding: utf-8 -*-

from __future__ import with_statement
import flask
import xdg.BaseDirectory
from flasfka import app
import kafka

APP_NAME = "flasfka"
XDG_CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
XDG_DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)


app.config.update(dict(
    HOSTS=["localhost:9092"],
    DEFAULT_GROUP="flasfka",
    CONSUMER_TIMEOUT=0.1,
    CONSUMER_LIMIT=100
    ))


def get_kafka_client():
    if not hasattr(flask.g, "kafka_client"):
        flask.g.kafka_client = kafka.KafkaClient(app.config["HOSTS"])
    return flask.g.kafka_client


def get_kafka_producer():
    if not hasattr(flask.g, "kafka_producer"):
        client = get_kafka_client()
        flask.g.kafka_producer = kafka.KeyedProducer(client)
    return flask.g.kafka_producer


def produce(topic, message, key=None):
    message = message.encode("utf-8")
    producer = get_kafka_producer()
    producer.send(topic, key, message)
    producer.stop()


def consume(topic, group, limit):
    if group is None:
        group = app.config["DEFAULT_GROUP"].encode("utf-8")
    client = get_kafka_client()
    consumer = kafka.SimpleConsumer(client, group, topic,
            iter_timeout=app.config["CONSUMER_TIMEOUT"])
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
    try:
        topic = topic.encode("utf-8")
        if group_or_key is not None:
            group_or_key = group_or_key.encode("utf-8")

        client = get_kafka_client()
        client.ensure_topic_exists(topic)

        if flask.request.method == "GET":
            limit = int(flask.request.args.get("limit", app.config["CONSUMER_LIMIT"]))
            group = group_or_key
            return flask.jsonify(consume(topic, group, limit))
        if flask.request.method == "POST":
            key = group_or_key
            produce(topic, flask.request.get_data(), key)
            return flask.make_response(("", 204, {}))
    except UnicodeDecodeError:
        return flask.make_response("Flafska only accepts utf-8", 400, {})


@app.after_request
def debug_cache_off(response):
    if app.config["DEBUG"]:
        response.headers["Cache-Control"] = "no-cache, max-age=0"
    return response
