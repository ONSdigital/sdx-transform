import json
import os.path
import threading

import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib3.exceptions import MaxRetryError

from transform.transformers.index_file import IndexFile
from .image_base import ImageBase

# Configure the number of retries attempted before failing call
from .response import SurveyResponse
from ..utilities.formatter import Formatter

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1)
session.mount('http://', HTTPAdapter(max_retries=retries))


class RetryableError(Exception):
    """
    Exception to be raised to indicate that the survey submission should be retried.
    This should be used when the failure was caused by circumstances outside of this services
    control that might change e.g. another service being down.
    """
    pass


class ImageRequester(ImageBase):
    """Transforms a survey and _response into a zip file
    """

    def __init__(self, logger, survey, response: SurveyResponse, current_time=None, sequence_no=1000,
                 base_image_path=""):

        super().__init__(logger, survey, response, current_time, sequence_no, base_image_path)

    def get_zipped_images(self, num_sequence=None):
        """Builds the images and the index_file file into the zip file.
        It appends data to the zip , so any data in the zip
        prior to this executing is not deleted.
        """
        image_bytes = self._request_image()
        image_name = self._get_image_name()
        self._create_index(image_name)
        self._build_zip(image_name, image_bytes)
        return self.zip

    def _get_image_name(self):
        tx_id = self.response.tx_id
        return Formatter.get_image_name(tx_id, 1)

    def _create_index(self, image_name):
        self.index_file = IndexFile(self.logger, self.response, 1, [image_name], self.current_time)

    def _build_zip(self, image_name, image_bytes):
        self.zip.append(os.path.join(self.image_path, image_name), image_bytes)
        self.zip.append(os.path.join(self.index_path, self.index_file.index_name), self.index_file.in_memory_index.getvalue())
        self.zip.rewind()

    def _request_image(self):
        survey_json = json.dumps(self.response.response)
        http_response = self._post(survey_json)

        if http_response.status_code == 200:
            return http_response.content
        else:
            msg = "Bad response from sdx-image"
            self.logger.error(msg, status_code=http_response.status_code)
            raise Exception(msg)

    def _post(self, survey_json):
        """Constructs the http call to the transform service endpoint and posts the request"""

        url = "http://sdx-image:80/image"
        self.logger.info(f"Calling {url}")
        try:
            response = session.post(url, survey_json)
        except MaxRetryError:
            self.logger.error("Max retries exceeded", request_url=url)
            raise RetryableError("Max retries exceeded")
        except ConnectionError:
            self.logger.error("Connection error", request_url=url)
            raise RetryableError("Connection error")

        return response
