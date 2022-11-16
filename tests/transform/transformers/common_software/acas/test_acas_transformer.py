import unittest
from datetime import datetime

from transform.transformers.common_software.acas.acas_transformer import perform_transforms
from transform.transformers.common_software.acas.acas_transforms import TransformType


class TestPerformTransforms(unittest.TestCase):

    def test_currency_round_up(self):
        actual = perform_transforms({"123": "34567"}, {"123": TransformType.CURRENCY})
        expected = {"123": 35}
        self.assertEqual(expected, actual)

    def test_currency_round_down(self):
        actual = perform_transforms({"124": "34499"}, {"124": TransformType.CURRENCY})
        expected = {"124": 34}
        self.assertEqual(expected, actual)

    def test_currency_string(self):
        actual = perform_transforms({"124": "hello"}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    def test_currency_none(self):
        actual = perform_transforms({"124": None}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    def test_date(self):
        actual = perform_transforms({"11": "01/11/2022"}, {"11": TransformType.DATE})
        expected = {"11": datetime(2022, 11, 1, 0, 0)}
        self.assertEqual(expected, actual)

    def test_date_wrong(self):
        actual = perform_transforms({"11": "01/11/20221"}, {"11": TransformType.DATE})
        expected = {}
        self.assertEqual(expected, actual)

    def test_date_none(self):
        actual = perform_transforms({"11": None}, {"11": TransformType.DATE})
        expected = {}
        self.assertEqual(expected, actual)

    def test_text(self):
        actual = perform_transforms({"125": "hello"}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 1}
        self.assertEqual(expected, actual)

    def test_text_empty(self):
        actual = perform_transforms({"125": ""}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 2}
        self.assertEqual(expected, actual)

    def test_text_none(self):
        actual = perform_transforms({"125": None}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 2}
        self.assertEqual(expected, actual)

    def test_number_transform(self):
        actual = perform_transforms({"126": "100"}, {"126": TransformType.NUMBER})
        expected = {"126": 100}
        self.assertEqual(expected, actual)

    def test_number_transform_with_alpha(self):
        actual = perform_transforms({"126": "ten"}, {"126": TransformType.NUMBER})
        expected = {}
        self.assertEqual(expected, actual)

    def test_multiple_qcodes(self):

        response_data = {
            "100": "982374",
            "101": "03/09/1998",
            "102": "car",
            "103": None
        }

        transformation_dict = {
            "100": TransformType.CURRENCY,
            "101": TransformType.DATE,
            "102": TransformType.TEXT_FIELD,
            "103": TransformType.TEXT_FIELD
        }

        expected = {
            "100": 982,
            "101": datetime(1998, 9, 3, 0, 0),
            "102": 1,
            "103": 2
        }

        actual = perform_transforms(response_data, transformation_dict)
        self.assertEqual(expected, actual)


class TestDeriveTransforms(unittest.TestCase):
    pass
