import json
import os

import structlog

from transform.settings import SDX_FTP_IMAGE_PATH, SDX_FTP_DATA_PATH, SDX_FTP_RECEIPT_PATH, SDX_RESPONSE_JSON_PATH
from transform.transformers import ImageTransformer
from transform.transformers.image_requester import ImageRequester
from transform.transformers.response import SurveyResponse
from transform.transformers.survey import Survey
from transform.utilities.formatter import Formatter

logger = structlog.get_logger()


class SurveyTransformer:
    """Baseclass for specific survey transformers.

    Common functionality for transformer classes.
    Subclasses should provide their own implementations for create_pck().

    """

    def __init__(self, response: SurveyResponse, sequence_no, use_sdx_image: bool = False):
        self.survey_response = response
        self.sequence_no = sequence_no
        self.logger = logger
        if use_sdx_image:
            self.image_transformer = ImageRequester(self.logger, self.survey_response,
                                                    sequence_no=self.sequence_no, base_image_path=SDX_FTP_IMAGE_PATH)
        else:
            survey = Survey.load_survey(self.survey_response.survey_id, self.survey_response.instrument_id)
            self.image_transformer = ImageTransformer(self.logger, survey, self.survey_response,
                                                      sequence_no=self.sequence_no, base_image_path=SDX_FTP_IMAGE_PATH)

    def create_pck(self):
        """
        Must return a tuple containing the pck name, and the pck itself as string.
        """
        pck_name = ""
        pck = None
        return pck_name, pck

    def create_receipt(self):
        bound_logger = self.logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Creating IDBR receipt")
        idbr_name = Formatter.idbr_name(self.survey_response.submitted_at, self.survey_response.tx_id)
        idbr = Formatter.get_idbr(
            self.survey_response.survey_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.survey_response.period,
        )
        bound_logger.info("Successfully created IDBR receipt")
        return idbr_name, idbr

    def _create_images(self, img_seq=None):
        """
        Create the image files within the zip.
        """
        self.image_transformer.get_zipped_images(img_seq)

    def get_json(self):
        json_name = Formatter.response_json_name(self.survey_response.survey_id, self.survey_response.tx_id)
        json_file = json.dumps(self.survey_response.response)
        return json_name, json_file

    def get_zip(self, img_seq=None):

        pck_name, pck = self.create_pck()
        if pck is not None:
            self.image_transformer.append_to_zip(os.path.join(SDX_FTP_DATA_PATH, pck_name), pck)

        receipt_name, receipt = self.create_receipt()
        if receipt is not None:
            self.image_transformer.append_to_zip(os.path.join(SDX_FTP_RECEIPT_PATH, receipt_name), receipt)

        self._create_images(img_seq)

        # add original json to zip
        json_name, json_file = self.get_json()
        if json_file is not None:
            self.image_transformer.zip.append(os.path.join(SDX_RESPONSE_JSON_PATH, json_name), json_file)

        return self.image_transformer.get_zip()
