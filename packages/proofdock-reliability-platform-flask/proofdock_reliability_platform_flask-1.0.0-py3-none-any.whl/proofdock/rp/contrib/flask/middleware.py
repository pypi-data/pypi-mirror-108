from flask import Flask, request
from logzero import logger

from proofdock.rp.contrib.flask.config import FlaskConfig
from proofdock.rp.core import chaos


def _before_request():
    """Runs before each request.
    See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.before_request
    """

    # do not attack access control methods - pre flight requests
    if request.access_control_request_method:
        return

    attack_ctx = {"type": "python.flask.request", "params": {"route": request.path}}
    chaos.attack(attack_ctx)


class FlaskMiddleware(object):

    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        try:
            config = FlaskConfig(app)
            chaos.register(config, ["python.flask.request"])
            self.app.before_request(_before_request)
        except Exception as ex:
            logger.error("Unable to configure chaos middleware. Error: %s", ex, stack_info=True)
