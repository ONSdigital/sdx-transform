import datetime
import json
import unittest

from transform.transformers.response import SurveyResponse
from transform.transformers.survey import MissingIdsException


class SurveyResponseTests(unittest.TestCase):
    response_json = '''{
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "origin": "uk.gov.ons.edc.eq",
            "survey_id": "009",
            "version": "0.0.1",
            "tx_id": "897fbe8c-fa67-4406-b05c-3e893bc1af78",
            "collection": {
                "instrument_id": "0106",
                "period": "201605"
            },
            "submitted_at": "2022-08-19T10:39:40Z",
            "metadata": {
                "user_id": "789473423",
                "ru_ref": "12345678901A",
                "ref_period_start_date": "2022-08-01",
                "ref_period_end_date": "2022-08-31"
            },
            "data": {
                "146": "some comment"
            }
        }'''

    def setUp(self) -> None:
        self.response = json.loads(self.response_json)

    def test_all_metadata_present(self):
        result = SurveyResponse(self.response)

        self.assertEqual("897fbe8c-fa67-4406-b05c-3e893bc1af78", result.tx_id)
        self.assertEqual("009", result.survey_id)
        self.assertEqual("0106", result.instrument_id)
        self.assertEqual("201605", result.period)
        self.assertEqual("12345678901", result.ru_ref)
        self.assertEqual("A", result.ru_check)
        self.assertEqual("2022-08-19T10:39:40Z", result.submitted_at_raw)
        self.assertEqual(datetime.date(2022, 8, 19), result.submitted_at.date())
        self.assertEqual("2022-08-01", result.ref_period_start_date)
        self.assertEqual("2022-08-31", result.ref_period_end_date)

    def test_no_instrument_id_raises_missing_ids_exception(self):
        del self.response["collection"]["instrument_id"]

        with self.assertRaises(MissingIdsException):
            SurveyResponse(self.response)
