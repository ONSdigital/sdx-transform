import datetime
import unittest

import pytest

from transform.transformers.survey import Survey, MissingSurveyException


class SurveyTests(unittest.TestCase):

    def test_datetime_ms_with_colon_in_timezone(self):
        rv = Survey.parse_timestamp("2017-01-11T17:18:53.020222+00:00")
        self.assertIsInstance(rv, datetime.datetime)

    def test_datetime_ms_with_timezone(self):
        rv = Survey.parse_timestamp("2017-01-11T17:18:53.020222+0000")
        self.assertIsInstance(rv, datetime.datetime)

    def test_datetime_zulu(self):
        rv = Survey.parse_timestamp("2017-01-11T17:18:53Z")
        self.assertIsInstance(rv, datetime.datetime)

    def test_date_iso(self):
        rv = Survey.parse_timestamp("2017-01-11")
        self.assertNotIsInstance(rv, datetime.datetime)
        self.assertIsInstance(rv, datetime.date)

    def test_date_diary(self):
        rv = Survey.parse_timestamp("11/07/2017")
        self.assertNotIsInstance(rv, datetime.datetime)
        self.assertIsInstance(rv, datetime.date)

    def test_date_period(self):
        rv = Survey.parse_timestamp("201605")
        self.assertNotIsInstance(rv, datetime.datetime)
        self.assertIsInstance(rv, datetime.date)

    def test_load_survey(self):
        survey_id = "134"
        instrument_id = "0005"
        rv = Survey.load_survey(survey_id, instrument_id, "./tests/data/{survey_id}.{instrument_id}.json")
        self.assertIsNotNone(rv)

    def test_load_survey_miss(self):
        with pytest.raises(MissingSurveyException):
            Survey.load_survey("127", "0001", "./tests/data/{survey_id}.{instrument_id}.json")
