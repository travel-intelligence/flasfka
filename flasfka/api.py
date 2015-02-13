# -*- coding: utf-8 -*-

from __future__ import with_statement
import flask
import xdg.BaseDirectory
from flasfka import app
from kafka import SimpleProducer, KafkaClient, SimpleConsumer, KeyedProducer

APP_NAME = "flasfka"
XDG_CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
XDG_DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)


app.config.update(dict(
    HOSTS=["localhost:9092"],
    DEFAULT_GROUP="flasfka",
    CONSUMER_TIMEOUT=1,
    CONSUMER_LIMIT=20
    ))


def json_response(status, body={}):
    """
    Builds a response object with the content type set to json
    """
    status_message = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not found",
        413: "Request entity too large",
        429: "Too many requests",
        500: "Internal error"
        }
    if not isinstance(body, dict):
        body = {"message": body}
    if status != 200:
        body["status"] = status_message[status]
        body["status_code"] = status
    response = flask.jsonify(body)
    response.status = str(status)
    return response


def get_kafka_client():
    if not hasattr(flask.g, "kafka_client"):
        flask.g.kafka_client = KafkaClient(app.config["HOSTS"])
    return flask.g.kafka_client


def get_kafka_producer():
    if not hasattr(flask.g, "kafka_producer"):
        client = get_kafka_client()
        flask.g.kafka_producer = KeyedProducer(client, batch_send=True)
    return flask.g.kafka_producer


def produce(topic, message, key=None):
    message = message.encode("utf-8")
    producer = get_kafka_producer()
    producer.send(topic, key, message)


def consume(topic, group=app.config["DEFAULT_GROUP"].encode("utf-8"), limit=20):
    client = get_kafka_client()
    consumer = SimpleConsumer(client, group, topic,
            iter_timeout=app.config["CONSUMER_TIMEOUT"])
    res = []
    for n, message in enumerate(consumer):
        res.append(message.message.value.decode("utf-8"))
        if n >= limit - 1:
            break
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
        group = group_or_key
        return json_response(200, consume(topic, group))
    if flask.request.method == "POST":
        key = group_or_key
        produce(topic, flask.request.get_data(), key)
        return flask.make_response(("", 204, {}))
        #return json_response(200, "hello")


@app.after_request
def debug_cache_off(response):
    if app.config["DEBUG"]:
        response.headers["Cache-Control"] = "no-cache, max-age=0"
    return response
