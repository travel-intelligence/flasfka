# -*- coding: utf-8 -*-

__version__ = "1.1.5"

# "import flask" is wrapped in a try/catch clause for setup.py to get the
# version without requiring flask
try:
    import flask
    app = flask.Flask(__name__)
    from . import api
except ImportError: # pragma: no cover
    pass
