import unittest

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
            "301": "22000",
            "302": "5000",
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
            "301": "22000",
            "302": "",
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
            "301": "22000",
            "302": "5000",
            "303": "insert text"
        }

        result = perform_transforms(data, transforms_spec)

        self.assertEqual(expected, result)
