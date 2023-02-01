import datetime
import json
import unittest

from transform.transformers.response import SurveyResponseV1, SurveyResponseV2
from transform.transformers.survey import MissingIdsException


class SurveyResponseTests(unittest.TestCase):
    response_json = '''{
            "case_id": "a9bf1f7c-3f86-407b-9a0f-86cc1c18e8b1",
            "tx_id": "04743704-e33d-4aef-9006-445d9dd31907",
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.1",
            "origin": "uk.gov.ons.edc.eq",
            "collection_exercise_sid": "8ad61a89-015f-4512-bf28-8381ff90bcae",
            "schema_name": "mbs_0106",
            "flushed": false,
            "submitted_at": "2023-01-12T14:53:00+00:00",
            "launch_language_code": "en",
            "survey_metadata": {
                "survey_id": "009",
                "trad_as": "ESSENTIAL ENTERPRISE LTD.",
                "ref_p_end_date": "2016-05-31",
                "ref_p_start_date": "2016-05-01",
                "ru_name": "ESSENTIAL ENTERPRISE LTD.",
                "user_id": "UNKNOWN",
                "ru_ref": "12346789012A",
                "period_id": "201605",
                "form_type": "0106"
            },
            "data": {"9999": "Yes, I can report for this period", "40": "28000", "146": "Very good survey!"},
            "started_at": "2023-01-12T14:52:30.136084+00:00",
            "submission_language_code": "en"
        }'''

    def setUp(self) -> None:
        self.response = json.loads(self.response_json)

    def test_all_metadata_present(self):
        result = SurveyResponseV2(self.response)

        self.assertEqual("04743704-e33d-4aef-9006-445d9dd31907", result.tx_id)
        self.assertEqual("009", result.survey_id)
        self.assertEqual("0106", result.instrument_id)
        self.assertEqual("201605", result.period)
        self.assertEqual("12346789012", result.ru_ref)
        self.assertEqual("A", result.ru_check)
        self.assertEqual("2023-01-12T14:53:00+00:00", result.submitted_at_raw)
        self.assertEqual(datetime.date(2023, 1, 12), result.submitted_at.date())
        self.assertEqual("2016-05-01", result.ref_period_start_date)
        self.assertEqual("2016-05-31", result.ref_period_end_date)

    def test_no_form_type_raises_missing_ids_exception(self):
        del self.response["survey_metadata"]["form_type"]

        with self.assertRaises(MissingIdsException):
            SurveyResponseV1(self.response)
