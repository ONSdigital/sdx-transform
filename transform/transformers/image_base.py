import datetime
import os.path

from transform.transformers.in_memory_zip import InMemoryZip
from .response import SurveyResponse


class ImageBase:
    """Transforms a survey and _response into a zip file.
    """

    def __init__(self, logger, response: SurveyResponse, current_time=None, sequence_no=1000,
                 base_image_path=""):

        if current_time is None:
            current_time = datetime.datetime.utcnow()

        self.zip = InMemoryZip()
        self.current_time = current_time
        self.logger = logger
        self.response = response
        self.image_path = "" if base_image_path == "" else os.path.join(base_image_path, "Images")
        self.index_path = "" if base_image_path == "" else os.path.join(base_image_path, "Index")

    def append_to_zip(self, path: str, data: str):
        self.zip.append(path, data)

    def get_zipped_images(self, num_sequence=None):
        """Builds the images and the index_file file into the zip file.
        It appends data to the zip , so any data in the zip
        prior to this executing is not deleted.
        """
        return self.zip

    def get_zip(self):
        """Get access to the in memory zip """
        self.zip.rewind()
        return self.zip.in_memory_zip
