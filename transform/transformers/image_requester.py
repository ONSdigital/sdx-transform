import json
import os.path
import time

import requests
from sdx_gcp.errors import RetryableError

from transform.transformers.index_file import IndexFile
from .image_base import ImageBase
from .response import SurveyResponse
from ..utilities.formatter import Formatter


class ImageServiceError(Exception):
    pass


class ImageRequester(ImageBase):
    """Transforms a survey and _response into a zip file
    """

    def __init__(self, logger, response: SurveyResponse, current_time=None, sequence_no=1000,
                 base_image_path=""):

        super().__init__(logger, response, current_time, sequence_no, base_image_path)

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
        trying = True
        retries = 0
        max_retries = 3
        http_response = None
        while trying:
            try:
                http_response = self._post(survey_json)
                trying = False
            except RetryableError:
                retries += 1
                if retries > max_retries:
                    trying = False
                else:
                    # sleep for 20 seconds
                    time.sleep(20)
                    self.logger.info("trying again...")

        if http_response and http_response.status_code == 200:
            return http_response.content
        else:
            msg = "Bad response from sdx-image"
            self.logger.error(msg, status_code=http_response.status_code)
            raise ImageServiceError(http_response.reason)

    def _post(self, survey_json):
        """Constructs the http call to the transform service endpoint and posts the request"""

        url = "http://sdx-image:80/image"
        self.logger.info(f"Calling {url}")
        try:
            response = requests.post(url, survey_json)
        except Exception:
            self.logger.error("Connection error", request_url=url)
            raise RetryableError("Connection error")

        return response
