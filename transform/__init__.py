import requests
from flask import Flask
from fastapi import FastAPI
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from transform.logger import logging_config

logging_config()

app = FastAPI()

from .views import main  # noqa
__version__ = "4.3.2"

# Configure the number of retries attempted before failing call
session = requests.Session()

retries = Retry(total=5, backoff_factor=0.1)

session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
