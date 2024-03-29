import datetime
import dateutil.parser

from io import BytesIO

from sdx_gcp.app import get_logger

from transform import settings
from transform.transformers.response import SurveyResponseV1
from transform.utilities.formatter import Formatter
from transform.views.image_filters import get_env, format_date

logger = get_logger()


class IndexFile:
    """Class for creating in memory index_file file using BytesIO."""

    def __init__(self, response_data, image_count, image_names,
                 current_time=None, sequence_no=1000):

        if current_time is None:
            current_time = datetime.datetime.utcnow()

        self.in_memory_index = BytesIO()
        self._response = response_data
        self._image_count = image_count
        self._creation_time = {
            'short': format_date(current_time, 'short'),
            'long': format_date(current_time)
        }
        self.index_name = self._get_index_name(self._response)
        self._current_time = current_time  # used to test if current_time gets set to a default value in init definition
        self._build_index(image_names)

    def rewind(self):
        """Rewinds the read-write position of the in-memory in_memory_index to the start."""
        self.in_memory_index.seek(0)

    def _build_index(self, image_names):
        """Builds the in_memory_index file contents into self.in_memory_index"""
        env = get_env()
        template = env.get_template('csv.tmpl')

        image_path = settings.FTP_PATH + settings.SDX_FTP_IMAGE_PATH + "\\Images"
        template_output = template.render(
            SDX_FTP_IMAGES_PATH=image_path,
            images=image_names,
            response=self._response,
            creation_time=self._creation_time
        )

        msg = "Adding image to in_memory_index"
        for image_name in image_names:
            logger.info(msg, file=image_name)

        self.in_memory_index.write(template_output.encode())
        self.rewind()

    @staticmethod
    def _get_index_name(response: SurveyResponseV1):
        survey_id = response.survey_id
        submission_date = dateutil.parser.parse(response.submitted_at_raw)
        submission_date_str = format_date(submission_date, 'short')
        tx_id = response.tx_id
        return Formatter.get_index_name(survey_id, submission_date_str, tx_id)
