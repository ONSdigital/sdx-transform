import os.path
import subprocess

from transform.transformers.index_file import IndexFile
from .image_base import ImageBase
from .pdf_transformer import PDFTransformer
from .response import SurveyResponse
from ..utilities.formatter import Formatter


class ImageTransformer(ImageBase):
    """Transforms a survey and _response into a zip file
    """

    def __init__(self, survey, response: SurveyResponse, current_time=None, sequence_no=1000,
                 base_image_path=""):

        super().__init__(response, current_time, sequence_no, base_image_path)

        self.survey = survey
        self._page_count = -1
        self.index_file = None
        self._pdf = None
        self._image_names = []
        self.sequence_no = sequence_no

    def get_zipped_images(self, num_sequence=None):
        """Builds the images and the index_file file into the zip file.
        It appends data to the zip , so any data in the zip
        prior to this executing is not deleted.
        """
        self._create_pdf()
        self._build_image_names(num_sequence, self._page_count)
        self._create_index()
        self._build_zip()
        return self.zip

    def _get_image_name(self, i: int):
        tx_id = self.response.tx_id
        return Formatter.get_image_name(tx_id, i)

    def _create_pdf(self):
        """Create a pdf which will be used as the basis for images """
        pdf_transformer = PDFTransformer(self.survey, self.response)
        self._pdf, self._page_count = pdf_transformer.render_pages()
        return self._pdf

    def _build_image_names(self, num_sequence, image_count):
        """Build a collection of image names to use later"""
        for i in self._get_image_sequence_list(image_count):
            self._image_names.append(self._get_image_name(i))

    def _create_index(self):
        self.index_file = IndexFile(self.response, self._page_count, self._image_names,
                                    self.current_time, self.sequence_no)

    def _build_zip(self):
        i = 0
        for image in self._extract_pdf_images(self._pdf):
            self.zip.append(os.path.join(self.image_path, self._image_names[i]), image)
            i += 1
        self.zip.append(os.path.join(self.index_path, self.index_file.index_name), self.index_file.in_memory_index.getvalue())
        self.zip.rewind()

    @staticmethod
    def _extract_pdf_images(pdf_stream):
        """
        Extract pdf pages as jpegs
        """

        process = subprocess.Popen(["pdftoppm", "-jpeg"],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result, errors = process.communicate(pdf_stream)

        if errors:
            raise IOError("images:Could not extract Images from pdf: {0}".format(repr(errors)))

        # FFD9 is an end of image marker in jpeg images
        for image in result.split(b'\xFF\xD9'):
            if len(image) > 11:  # we can get an end of file marker after the image and a jpeg header is 11 bytes long
                yield image

    @staticmethod
    def _get_image_sequence_list(n):
        return [i for i in range(1, n + 1)]
