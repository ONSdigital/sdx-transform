import json
import unittest

from transform.transformers.common_software.bricks.bricks_transform_spec import TRANSFORMS_SPEC
from transform.transformers.common_software.bricks.bricks_transformer import get_prepend_value, perform_transforms, \
    Transform, prepend_to_qcode, PREPEND_QCODE


class BricksTests(unittest.TestCase):

    def test_prepend_value_to_qcodes(self):
        actual = prepend_to_qcode("01", "2")
        expected = "201"

        self.assertEqual(expected, actual)

    def test_get_prepend_value(self):
        data = {
            PREPEND_QCODE: "Concrete",
        }

        result = get_prepend_value(data)

        expected = "3"

        self.assertEqual(expected, result)

    def test_perform_transforms_value(self):
        data = {
            "01": "22000",
            "02": "5000",
            "9999": "Concrete",
        }

        transforms_spec = {
            "01": Transform.PREPEND,
            "02": Transform.PREPEND,
        }

        expected = {
            "301": 22000,
            "302": 5000,
        }

        result = perform_transforms(data, transforms_spec)

        self.assertEqual(expected, result)

    def test_perform_transforms_doesnt_fail_for_missing_answers_or_qcodes(self):
        data = {
            "01": "22000",
            "02": "",
            "9999": "Concrete",
        }

        transforms_spec = {
            "01": Transform.PREPEND,
            "02": Transform.PREPEND,
            "03": Transform.PREPEND,
            "04": Transform.PREPEND,
        }

        expected = {
            "301": 22000,
        }

        result = perform_transforms(data, transforms_spec)

        self.assertEqual(expected, result)

    def test_perform_transforms_text(self):
        data = {
            "01": "22000",
            "02": "5000",
            "303": "insert text",
            "9999": "Concrete",
        }

        transforms_spec = {
            "01": Transform.PREPEND,
            "02": Transform.PREPEND,
            "303": Transform.TEXT
        }

        expected = {
            "301": 22000,
            "302": 5000,
            "303": 1
        }

        result = perform_transforms(data, transforms_spec)

        self.assertEqual(expected, result)

    def test_perform_transforms_addition(self):
        data = {
            "01": "1000",
            "11": "1000",
            "21": "1000",
            "02": "10000",
            "12": "10000",
            "22": "10000",
            "9999": "Concrete",
        }

        transforms_spec = {
            "01": Transform.PREPEND,
            "11": Transform.PREPEND,
            "21": Transform.PREPEND,
            "02": Transform.PREPEND,
            "12": Transform.PREPEND,
            "22": Transform.PREPEND,
            "501": Transform.ADDITION,
            "502": Transform.ADDITION,
            "503": Transform.ADDITION,
            "504": Transform.ADDITION
        }

        expected = {
            "301": 1000,
            "311": 1000,
            "321": 1000,
            "302": 10000,
            "312": 10000,
            "322": 10000,
            "501": 3000,
            "502": 30000,
            "503": 0,
            "504": 0
        }

        result = perform_transforms(data, transforms_spec)

        self.assertEqual(expected, result)

    def test_example_data(self):
        with open("tests/transform/transformers/common_software/bricks/bricks.json") as json_file:
            json_data = json.load(json_file)
            json_data = json_data["data"]

            actual = perform_transforms(json_data, TRANSFORMS_SPEC)
            print(actual)

            expected = {
                '301': 22000,
                '302': 5000,
                '303': 8000,
                '304': 7000,
                '311': 9000,
                '312': 1000,
                '313': 2000,
                '314': 6000,
                '145': 1,
                '146': 1,
                '501': 31000,
                '502': 6000,
                '503': 10000,
                '504': 13000
            }

            self.assertEqual(expected, actual)
