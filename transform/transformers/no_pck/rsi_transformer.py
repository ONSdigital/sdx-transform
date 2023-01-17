import json
from io import StringIO

import dateutil.parser
import structlog
from jinja2 import Environment, PackageLoader

from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer
from transform.utilities.formatter import Formatter

logger = structlog.get_logger()

env = Environment(loader=PackageLoader('transform', 'templates'))


class RSITransformer(SurveyTransformer):

    def __init__(self, response: SurveyResponse, sequence_no=1000):
        super().__init__(response, sequence_no)
        self._logger = logger
        self._batch_number = False
        self._idbr = StringIO()
        self._pck = StringIO()
        self._response_json = StringIO()

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

    def create_receipt(self):
        idbr_name = self._create_idbr()
        idbr = self._idbr.read()
        return idbr_name, idbr
