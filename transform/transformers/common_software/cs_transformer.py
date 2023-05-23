import json
from io import StringIO

import dateutil.parser
from jinja2 import Environment, PackageLoader
from sdx_gcp.app import get_logger

from transform.transformers.common_software.pck_transformer import PCKTransformer
from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer
from transform.utilities.formatter import Formatter

logger = get_logger()

env = Environment(loader=PackageLoader('transform', 'templates'))


class CSTransformer(SurveyTransformer):

    def __init__(self, response: SurveyResponse, sequence_no=1000):
        super().__init__(response, sequence_no)
        self._logger = logger
        self._batch_number = False
        self._idbr = StringIO()
        self._pck = StringIO()
        self._response_json = StringIO()

    def _create_pck(self):
        template = env.get_template('pck.tmpl')
        pck_transformer = PCKTransformer(self.survey, self.survey_response)
        answers = pck_transformer.derive_answers()
        cs_form_id = pck_transformer.get_cs_form_id()
        sub_date_str = pck_transformer.get_subdate_str()

        template_output = template.render(response=self.survey_response,
                                          submission_date=sub_date_str,
                                          batch_number=self._batch_number,
                                          form_id=cs_form_id,
                                          answers=answers)
        self._pck.write(template_output)
        self._pck.seek(0)

        # Vacancy surveys have a requirement to go to common software as survey_id 181.
        # We only change the filename as the survey_id isn't included in the content of
        # the pck file.
        vacancies_surveys = ["182", "183", "184", "185"]
        if self.survey['survey_id'] in vacancies_surveys:
            pck_name = Formatter.pck_name('181', self.survey_response.tx_id)
        else:
            pck_name = Formatter.pck_name(self.survey['survey_id'], self.survey_response.tx_id)

        return pck_name

    def _create_idbr(self):
        template = env.get_template('idbr.tmpl')
        template_output = template.render(response=self.survey_response)
        submission_date = dateutil.parser.parse(self.survey_response.submitted_at_raw)

        # Format is RECddMM_batchId.DAT
        # e.g. REC1001_30000.DAT for 10th January, batch 30000
        idbr_name = Formatter.idbr_name(submission_date, self.survey_response.tx_id)
        self._idbr.write(template_output)
        self._idbr.seek(0)
        return idbr_name

    def _create_response_json(self):
        original_json_name = Formatter.response_json_name(self.survey['survey_id'], self.survey_response.tx_id)
        self._response_json.write(json.dumps(self.survey_response))
        self._response_json.seek(0)
        return original_json_name

    def create_pck(self):
        pck_name = self._create_pck()
        pck = self._pck.read()
        return pck_name, pck

    def create_receipt(self):
        idbr_name = self._create_idbr()
        idbr = self._idbr.read()
        return idbr_name, idbr
