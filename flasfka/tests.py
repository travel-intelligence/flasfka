# -*- coding: utf-8 -*-

from __future__ import with_statement
import unittest
import random
import string
import json
import os
from . import app


def random_ascii_string(n=20):
    return ''.join(random.SystemRandom().choice(string.ascii_letters +
                   string.digits) for _ in range(n))


class FlafskaTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(dict(
            TESTING=True,
            ))
        self.app = app.test_client()

    def test_send_fetch(self):
        topic = random_ascii_string()
        message = {"messages": [random_ascii_string()]}

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 204)

        response = self.app.get("/" + topic + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': u'flasfka', u'messages':
                         message["messages"]})

    def test_send_fetch_group(self):
        topic = random_ascii_string()
        message = {"messages": [random_ascii_string()]}
        group = random_ascii_string()

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 204)

        response = self.app.get("/" + topic + "/" + group + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': group, u'messages':
                         message["messages"]})

    def test_send_non_json_data(self):
        message = '\xe5\xa2\xbe\xaa\xa7\xf8\xdf\x00\xc6\xbd'
        topic = random_ascii_string()

        response = self.app.post("/" + topic + "/", data=message)
        self.assertEqual(response.status_code, 400)

    def test_send_fetch_2_groups(self):
        topic = random_ascii_string()
        message = {"messages": [random_ascii_string()]}

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 204)

        group = "group_1"
        response = self.app.get("/" + topic + "/" + group + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': group, u'messages':
                         message["messages"]})

        group = "group_2"
        response = self.app.get("/" + topic + "/" + group + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': group, u'messages':
                         message["messages"]})

    def test_send_fetch_same_group(self):
        topic = random_ascii_string()
        message = {"messages": [random_ascii_string()]}

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 204)

        group = "group"
        response = self.app.get("/" + topic + "/" + group + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': group, u'messages':
                         message["messages"]})

        response = self.app.get("/" + topic + "/" + group + "/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEqual(body, {u'group': group, u'messages': []})

    def test_limit(self):
        topic = random_ascii_string()
        message = {"messages": ["hello %i" % i for i in range(400)]}

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 204)

        for _ in range(20):
            response = self.app.get("/" + topic + "/" + "?limit=10")
            self.assertEqual(response.status_code, 200)
            body = json.loads(response.data)
            self.assertLessEqual(len(body['messages']), 10)

    def test_send_wrong_messages(self):
        topic = random_ascii_string()
        message = {"messages": [{"a": "dictionary"}]}

        response = self.app.post("/" + topic + "/",
                                 data=json.dumps(message))
        self.assertEqual(response.status_code, 400)
