# -*- coding: utf-8 -*-

from __future__ import with_statement
import flask
import xdg.BaseDirectory
from flasfka import app

APP_NAME = "flasfka"
XDG_CONFIG_DIR = xdg.BaseDirectory.save_config_path(APP_NAME)
XDG_DATA_DIR = xdg.BaseDirectory.save_data_path(APP_NAME)

app.config.update(dict(
    HOSTS=["localhost:9092"]
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

def get_kafka():
    if not hasattr(flask.g, "kafka"):
        flask.g.kafka = KafkaClient(app.config["HOSTS"])
    return flask.g.kafka

def kafka_post(topic, message, key=None):
    kafka = get_kafka()
    if key is None:
        producer = SimpleProducer(kafka)
        producer.send_messages(topic, message)
    else:
        producer = KeyedProducer(kafka)
        producer.send(topic, key, message)

def kafka_get(topic, group=None):
    kafka = get_kafka()


@app.route("/", methods=["GET", "POST"])
@app.route("/<topic>/", methods=["GET", "POST"])
@app.route("/<group>/<topic>/", methods=["GET", "POST"])
def flasfka(group=None, topic=None):
    kafka_send("hello", "world")
    return json_response(200, "hello")


@app.after_request
def debug_cache_off(response):
    if app.config["DEBUG"]:
        response.headers["Cache-Control"] = "no-cache, max-age=0"
    return response
