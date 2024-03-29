import datetime
import json
import unittest
from collections import OrderedDict

from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.response import SurveyResponseV1


class BatchFileTests(unittest.TestCase):

    def setUp(self):
        with open("./tests/data/eq-mwss.json", encoding="utf-8") as fh:
            self.src = fh.read()
            self.reply = json.loads(self.src)

    def test_pck_form_header(self):
        form_id = 5
        ru_ref = 49900001225
        check = "C"
        period = "200911"
        rv = CSFormatter._pck_form_header(form_id, ru_ref, check, period)
        self.assertEqual("0005:49900001225C:200911", rv)

    def test_pck_lines(self):
        """Tests conversions of various types of values."""
        inst_id = "0005"
        ru_ref = 49900001225
        check = "C"
        period = "200911"
        data = OrderedDict([
            ("0001", 2),
            ("0140", 124),
            ("0146", "This is a comment"),
            ("0151", 217222),
            ("0200", {})
        ])
        self.assertTrue(isinstance(val, int) for val in data.values())
        rv = CSFormatter._pck_lines(data, inst_id, ru_ref, check, period)
        self.assertEqual([
            "FV          ",
            "0005:49900001225C:200911",
            "0001 00000000002",
            "0140 00000000124",
            "0146 00000000001",
            "0151 00000217222",
            "0200 ???????????"
        ], rv)

    def test_idbr_receipt(self):
        self.reply["tx_id"] = "27923934-62de-475c-bc01-433c09fd38b8"
        response = SurveyResponseV1(self.reply)
        rv = CSFormatter.get_idbr(response.survey_id, response.ru_ref, response.ru_check, response.period)
        self.assertEqual("12346789012:A:134:201605", rv)

    def test_idbr_receipt_four_digit_period(self):
        self.reply["tx_id"] = "27923934-62de-475c-bc01-433c09fd38b8"
        response = SurveyResponseV1(self.reply)
        period = "1605"
        rv = CSFormatter.get_idbr(response.survey_id, response.ru_ref, response.ru_check, period)
        self.assertEqual("12346789012:A:134:201605", rv)

    def test_identifiers(self):
        self.reply["tx_id"] = "27923934-62de-475c-bc01-433c09fd38b8"
        self.reply["collection"]["period"] = "200911"
        response = SurveyResponseV1(self.reply)

        self.assertEqual(self.reply["tx_id"], response.tx_id)
        self.assertEqual(datetime.date(2017, 3, 1), response.submitted_at.date())
        self.assertEqual("134", response.survey_id)
        self.assertEqual("12346789012", response.ru_ref)
        self.assertEqual("A", response.ru_check)
        self.assertEqual("200911", response.period)

    def test_pck_from_transformed_data(self):
        self.reply["tx_id"] = "27923934-62de-475c-bc01-433c09fd38b8"
        self.reply["survey_id"] = "134"
        self.reply["collection"]["period"] = "200911"
        self.reply["metadata"]["ru_ref"] = "49900001225C"
        self.reply["data"] = OrderedDict([
            ("0001", 2),
            ("0140", 124),
            ("0151", 217222)
        ])
        response = SurveyResponseV1(self.reply)
        rv = CSFormatter._pck_lines(response.data, response.instrument_id, response.ru_ref,
                                    response.ru_check, response.period)
        self.assertEqual([
            "FV          ",
            "0005:49900001225C:200911",
            "0001 00000000002",
            "0140 00000000124",
            "0151 00000217222",
        ], rv)
