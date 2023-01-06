import unittest

from transform.transformers.cora.ukis.ukis_transformer import perform_transforms
from transform.transformers.cora.ukis.ukis_transforms import TransformType


class TestUKISTransforms(unittest.TestCase):
    def test_yes_no_returns_yes_value(self):
        actual = perform_transforms({"123": "yes"}, {"123": TransformType.YESNO})
        expected = {"123": "10"}
        self.assertEqual(expected, actual)

    def test_yes_no_returns_no_value(self):
        actual = perform_transforms({"123": "no"}, {"123": TransformType.YESNO})
        expected = {"123": "01"}
        self.assertEqual(expected, actual)

    def test_yes_no_returns_empty_string(self):
        actual = perform_transforms({"123": ""}, {"123": TransformType.YESNO})
        expected = {"123": ""}
        self.assertEqual(expected, actual)

    def test_yes_no_returns_with_wrong_case(self):
        actual = perform_transforms({"123": "YES"}, {"123": TransformType.YESNO})
        expected = {"123": "10"}
        self.assertEqual(expected, actual)

    def test_high_importance_returns_correctly(self):
        actual = perform_transforms({"124": "high importance"}, {"124": TransformType.IMPORTANCE})
        expected = {"124": "1000"}
        self.assertEqual(expected, actual)

    def test_medium_importance_returns_correctly(self):
        actual = perform_transforms({"124": "medium importance"}, {"124": TransformType.IMPORTANCE})
        expected = {"124": "0100"}
        self.assertEqual(expected, actual)

    def test_low_importance_returns_correctly(self):
        actual = perform_transforms({"124": "low importance"}, {"124": TransformType.IMPORTANCE})
        expected = {"124": "0010"}
        self.assertEqual(expected, actual)

    def test_not_important_returns_correctly(self):
        actual = perform_transforms({"124": "not important"}, {"124": TransformType.IMPORTANCE})
        expected = {"124": "0001"}
        self.assertEqual(expected, actual)

    def test_importance_returns_empty_string(self):
        actual = perform_transforms({"124": ""}, {"124": TransformType.IMPORTANCE})
        expected = {"124": ""}
        self.assertEqual(expected, actual)

    def test_thousands_rounding_rounds_up(self):
        actual = perform_transforms({"125": "34567"}, {"125": TransformType.CURRENCY})
        expected = {"125": 35}
        self.assertEqual(expected, actual)

    def test_thousands_rounding_rounds_down(self):
        actual = perform_transforms({"125": "34467"}, {"125": TransformType.CURRENCY})
        expected = {"125": 34}
        self.assertEqual(expected, actual)

    def test_thousands_string(self):
        actual = perform_transforms({"125": "hello"}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    def test_thousands_none(self):
        actual = perform_transforms({"125": ""}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    # def test_checkbox_transform_choose_multiple(self):
    #
    #     response_data = {
    #             "126": "Yes",
    #             "127": "Yes",
    #         }
    #
    #     actual = perform_transforms(response_data, {})
    #
    #     expected = {
    #         "126": "1",
    #         "127": "1",
    #         "128": ""
    #     }
    #
    #     self.assertEqual(expected, actual)

    def test_checkbox_transform_returns_one(self):
        response_data = {
            "126": "Yes",
            "127": "Yes",
        }

        actual = perform_transforms(response_data, {"126": TransformType.CHECKBOX,
                                                    "127": TransformType.CHECKBOX})

        expected = {
            "126": "1",
            "127": "1",
        }

        self.assertEqual(expected, actual)

    def test_checkbox_transform_with_empty_values(self):
        response_data = {
            "126": "Yes",
            "127": "Yes",
        }

        expected_checkbox_qcodes = [
            "126", "127", "128", "129"
        ]

        actual = perform_transforms(response_data,
                                    {"126": TransformType.CHECKBOX,
                                     "127": TransformType.CHECKBOX},
                                    expected_checkbox_qcodes
                                    )

        expected = {
            "126": "1",
            "127": "1",
            "128": "",
            "129": ""
        }

        self.assertEqual(expected, actual)
