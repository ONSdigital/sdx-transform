import unittest

from transform.transformers.common_software.acas.acas_transformer import perform_initial_transforms, \
    perform_derived_transforms, perform_replacement_transforms, extract_pck_period
from transform.transformers.common_software.acas.acas_transforms import TransformType, DerivedTransformType, \
    DerivedTransform


class TestPerformInitialTransforms(unittest.TestCase):

    def test_currency_round_up(self):
        actual = perform_initial_transforms({"123": "34567"}, {"123": TransformType.CURRENCY})
        expected = {"123": 35}
        self.assertEqual(expected, actual)

    def test_currency_round_down(self):
        actual = perform_initial_transforms({"124": "34499"}, {"124": TransformType.CURRENCY})
        expected = {"124": 34}
        self.assertEqual(expected, actual)

    def test_currency_string(self):
        actual = perform_initial_transforms({"124": "hello"}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    def test_currency_none(self):
        actual = perform_initial_transforms({"124": ""}, {"124": TransformType.CURRENCY})
        expected = {}
        self.assertEqual(expected, actual)

    def test_date(self):
        actual = perform_initial_transforms({"11": "01/11/2022"}, {"11": TransformType.DATE})
        expected = {"11": 11122}
        self.assertEqual(expected, actual)

    def test_date_wrong(self):
        actual = perform_initial_transforms({"11": "01/11/20221"}, {"11": TransformType.DATE})
        expected = {}
        self.assertEqual(expected, actual)

    def test_date_none(self):
        actual = perform_initial_transforms({"11": ""}, {"11": TransformType.DATE})
        expected = {}
        self.assertEqual(expected, actual)

    def test_text(self):
        actual = perform_initial_transforms({"125": "hello"}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 1}
        self.assertEqual(expected, actual)

    def test_text_empty(self):
        actual = perform_initial_transforms({"125": ""}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 2}
        self.assertEqual(expected, actual)

    def test_text_none(self):
        actual = perform_initial_transforms({"125": ""}, {"125": TransformType.TEXT_FIELD})
        expected = {"125": 2}
        self.assertEqual(expected, actual)

    def test_number_transform(self):
        actual = perform_initial_transforms({"126": "100"}, {"126": TransformType.NUMBER})
        expected = {"126": 100}
        self.assertEqual(expected, actual)

    def test_number_transform_with_alpha(self):
        actual = perform_initial_transforms({"126": "ten"}, {"126": TransformType.NUMBER})
        expected = {}
        self.assertEqual(expected, actual)

    def test_negative(self):
        actual = perform_initial_transforms({"126": "-1"}, {"126": TransformType.NUMBER})
        expected = {"126": 99999999999}
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
            "101": 30998,
            "102": 1,
            "103": 2
        }

        actual = perform_initial_transforms(response_data, transformation_dict)
        self.assertEqual(expected, actual)


class TestDeriveTransforms(unittest.TestCase):

    def test_addition(self):
        transformed_data = {
            "100": 1,
            "101": 1,
        }

        expected = {
            "100": 1,
            "101": 1,
            "102": 2
        }

        actual = perform_derived_transforms(
            transformed_data,
            {"102": DerivedTransform(DerivedTransformType.ADDITION, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_addition_with_unused_codes(self):
        data = {
            "100": 1,
            "101": 1,
            "200": 5
        }

        expected = {
            "100": 1,
            "101": 1,
            "103": 2,
            "200": 5
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.ADDITION, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_addition_when_parent_missing(self):
        data = {
            "100": 1,
        }

        expected = {
            "100": 1,
            "103": 1,
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.ADDITION, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_non_zeros_all_non_zeros(self):
        data = {
            "100": 10,
            "101": 10,
        }

        expected = {
            "100": 10,
            "101": 10,
            "103": 2,
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.NON_ZEROS, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_non_zeros_with_zeros(self):
        data = {
            "100": 0,
            "101": 0,
        }

        expected = {
            "100": 0,
            "101": 0,
            "103": 1,
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.NON_ZEROS, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_non_zeros_some_non_zeros(self):
        data = {
            "100": 10,
            "101": 0,
        }

        expected = {
            "100": 10,
            "101": 0,
            "103": 2,
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.NON_ZEROS, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_non_zeros_with_parent_missing(self):
        data = {
            "101": 10,
        }

        expected = {
            "101": 10,
            "103": 2,
        }

        actual = perform_derived_transforms(
            data,
            {"103": DerivedTransform(DerivedTransformType.NON_ZEROS, ["100", "101"])}
        )

        self.assertEqual(expected, actual)

    def test_non_zeros_with_zeros_and_parent_missing(self):
        data = {
            "101": 0,
        }

        expected = {
            "101": 0,
            "103": 1,
        }

        actual = perform_derived_transforms(
            data, {"103": DerivedTransform(DerivedTransformType.NON_ZEROS, ["100", "101"])}
        )

        self.assertEqual(expected, actual)


class TestPerformReplacementTransforms(unittest.TestCase):

    def test_replace(self):
        response_data = {"100": "Yes"}
        transformed_data = {}
        replacement_transforms = {
            "100": {
                "101": lambda v: 1 if v == "Yes" else 2,
                "102": lambda v: 1 if v == "No" else 2,
            }
        }

        actual = perform_replacement_transforms(response_data, transformed_data, replacement_transforms)
        expected = {
            "101": 1,
            "102": 2
        }
        self.assertEqual(expected, actual)


class TestPeriodForPck(unittest.TestCase):
    def test_extract_pck_period(self):
        # arrange
        expected_period = '22'
        pck_period = extract_pck_period('202212')
        self.assertEqual(expected_period, pck_period)

    def test_extract_pck_period_23(self):
        # arrange
        expected_period = '23'
        pck_period = extract_pck_period('202312')
        self.assertEqual(expected_period, pck_period)

    def test_extract_pck_short_period(self):
        # arrange
        expected_period = '22'
        pck_period = extract_pck_period('2022')
        self.assertEqual(expected_period, pck_period)

    def test_extract_pck_two_digit_period(self):
        # arrange
        expected_period = '22'
        pck_period = extract_pck_period('22')
        self.assertEqual(expected_period, pck_period)
