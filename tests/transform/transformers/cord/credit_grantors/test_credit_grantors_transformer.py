import json
import unittest

from transform.transformers.cord.credit_grantors.credit_grantors_transform_spec import TRANSFORMS_SPEC
from transform.transformers.cord.credit_grantors.credit_grantors_transformer import perform_transforms


class CreditTests(unittest.TestCase):

    def test_example_with_no_answer(self):
        data = {
            "9999": "Yes, I can report for this period",
            "9996": "Yes",
            "9995": "Yes",
            "9994": "first business, second business",
            "9001": "-5000",
            "9003": "2000",
            "9005": "1000",
            "9007": "3000",
            "9008": "-2000",
            "9010": "5000",
            "9012": "-1000",
            "9014": "2000",
        }

        actual = perform_transforms(data, TRANSFORMS_SPEC)

        expected = {
            '9001': -5000,
            '9003': 2000,
            '9005': 1000,
            '9007': 3000,
            '9008': -2000,
            '9010': 5000,
            '9012': -1000,
            '9014': 2000,
        }

        self.assertEqual(expected, actual)

    def test_example_data(self):
        with open("tests/transform/transformers/cord/credit_grantors/credit_grantors.json") as json_file:
            json_data = json.load(json_file)
            json_data = json_data["data"]

            actual = perform_transforms(json_data, TRANSFORMS_SPEC)
            print(actual)

            expected = {
                '9001': 10000,
                '9003': 15000,
                '9005': 3000,
                '9007': 2000,
                '9008': 1000,
                '9010': 8000,
                '9012': 3000,
                '9014': 15000,
                '9002': 1000,
                '9004': 4000,
                '9006': 3000,
                '9009': 2000,
                '9016': 6000,
                '9011': 5000,
                '9013': 1000,
                '9015': -6000
            }

            self.assertEqual(expected, actual)
