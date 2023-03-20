from flask import Flask


from transform.logger import logging_config

logging_config()

app = Flask(__name__)

from .views import main  # noqa
__version__ = "1.16.7"
