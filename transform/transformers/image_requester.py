import json
import os.path

from transform.transformers.index_file import IndexFile
from .image_base import ImageBase
from .response import SurveyResponse
from ..settings import IMAGE_SERVICE_URL, sdx_app
from ..utilities.formatter import Formatter


class ImageRequester(ImageBase):
    """Transforms a survey and _response into a zip file
    """

    def __init__(self, response: SurveyResponse, current_time=None, sequence_no=1000,
                 base_image_path=""):

        super().__init__(response, current_time, sequence_no, base_image_path)

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
        self.index_file = IndexFile(self.response, 1, [image_name], self.current_time)

    def _build_zip(self, image_name, image_bytes):
        self.zip.append(os.path.join(self.image_path, image_name), image_bytes)
        self.zip.append(os.path.join(self.index_path, self.index_file.index_name), self.index_file.in_memory_index.getvalue())
        self.zip.rewind()

    def _request_image(self):
        survey_json = json.dumps(self.response.response)
        http_response = sdx_app.http_post(IMAGE_SERVICE_URL, "/image", survey_json)
        return http_response.content
