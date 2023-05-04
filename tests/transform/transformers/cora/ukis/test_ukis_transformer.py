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

    def test_yes_no_with_significant(self):
        actual = perform_transforms({"123": "Yes, they were significant"}, {"123": TransformType.YESNO})
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
        expected = {"125": "35"}
        self.assertEqual(expected, actual)

    def test_thousands_rounding_rounds_down(self):
        actual = perform_transforms({"125": "34467"}, {"125": TransformType.CURRENCY})
        expected = {"125": "34"}
        self.assertEqual(expected, actual)

    def test_thousands_string(self):
        actual = perform_transforms({"125": "hello"}, {"125": TransformType.CURRENCY})
        expected = {"125": ""}
        self.assertEqual(expected, actual)

    def test_thousands_none(self):
        actual = perform_transforms({"125": ""}, {"125": TransformType.CURRENCY})
        expected = {"125": ""}
        self.assertEqual(expected, actual)

    def test_checkbox_transform_returns_one(self):
        response_data = {
            "126": "Checkbox Information",
            "127": "more checkbox information",
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
            "126": "Checkbox information",
            "127": "More checkbox information",
        }

        actual = perform_transforms(response_data,
                                    {"126": TransformType.CHECKBOX,
                                     "127": TransformType.CHECKBOX,
                                     "128": TransformType.CHECKBOX,
                                     "129": TransformType.CHECKBOX})

        expected = {
            "126": "1",
            "127": "1",
            "128": "",
            "129": ""
        }

        self.assertEqual(expected, actual)

    def test_percent_radio_transform(self):
        response_data = {
            "101": "Over 90%",
            "102": "40-90%",
            "103": "Less than 40%",
            "104": "none",
            "105": ""
        }

        transforms = {
            "101": TransformType.PERCENT_RADIO,
            "102": TransformType.PERCENT_RADIO,
            "103": TransformType.PERCENT_RADIO,
            "104": TransformType.PERCENT_RADIO,
            "105": TransformType.PERCENT_RADIO,
        }

        actual = perform_transforms(response_data, transforms)

        expected = {
            "101": "0001",
            "102": "0010",
            "103": "0011",
            "104": "0100",
            "105": ""
        }

        self.assertEqual(expected, actual)

    def test_percentage_transform(self):
        actual = perform_transforms({"101": "84"}, {"101": TransformType.PERCENTAGE})
        expected = {"101": "84"}
        self.assertEqual(expected, actual)

    def test_text_transform(self):
        actual = perform_transforms({"101": "hello"}, {"101": TransformType.TEXT})
        expected = {"101": "1"}
        self.assertEqual(expected, actual)

        actual = perform_transforms({"101": ""}, {"101": TransformType.TEXT})
        expected = {"101": "2"}
        self.assertEqual(expected, actual)

    def test_distance_radio_transform(self):
        actual = perform_transforms(
            {"2121": "Within 15 miles of one of the physical sites of your business and within the uk"},
            {"2121": TransformType.DISTANCE_RADIO})

        expected = {
            "2121": "1",
            "2122": "0",
            "2123": "0",
            "2124": "0"
        }
        self.assertEqual(expected, actual)

    def test_distance_radio_transform_with_existing_dict(self):
        actual = {
            "101": "10",
            "102": "1"
        }

        distance_dict = perform_transforms(
            {"2121": "Within 15 miles of one of the physical sites of your business and within the uk"},
            {"2121": TransformType.DISTANCE_RADIO})

        actual.update(distance_dict)

        expected = {
            "101": "10",
            "102": "1",
            "2121": "1",
            "2122": "0",
            "2123": "0",
            "2124": "0"
        }
        self.assertEqual(expected, actual)
