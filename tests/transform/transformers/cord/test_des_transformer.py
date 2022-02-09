import unittest

from transform.transformers.cord.des import des_transformer
from transform.transformers.cord.des.des_transformer import perform_transform
from transform.transformers.cord.des.des_transforms import Transform


class DESTransformerTest(unittest.TestCase):

    def test_thousands(self):
        self.assertEqual('56', des_transformer.thousands('55907'))
        self.assertEqual('', des_transformer.thousands(''))

    def test_checkbox(self):
        self.assertEqual('1', des_transformer.checkbox("hello", "1", "0"))
        self.assertEqual('0', des_transformer.checkbox("", "1", "0"))

    def test_radio_button(self):
        mapping = {
            "Yes": "10",
            "No": "01"
        }
        self.assertEqual('10', des_transformer.radio_button("Yes, blah blah", mapping))
        self.assertEqual('01', des_transformer.radio_button("No ...", mapping))
        self.assertEqual('', des_transformer.radio_button("", mapping))

    def test_multi_qcode_radio_button(self):
        qcode_mapping = {
            "Less than 2Mbps": {
                "qcode": "277",
                "ticked": "1",
                "unticked": "0"
            },
            "2Mbps or more, but less than 10Mbps": {
                "qcode": "278",
                "ticked": "1",
                "unticked": "0"
            },
            "10Mbps or more, but less than 30Mbps": {
                "qcode": "279",
                "ticked": "1",
                "unticked": "0"
            }
        }

        expected = {"277": "0", "278": "1", "279": "0"}
        actual = des_transformer.multi_qcode_radio_button("2Mbps or more, but less than 10Mbps", qcode_mapping)
        self.assertEqual(expected, actual)

        expected = {"277": "", "278": "", "279": ""}
        actual = des_transformer.multi_qcode_radio_button("", qcode_mapping)
        self.assertEqual(expected, actual)

    def test_non_mutually_exclusive_multi_qcode_radio_button(self):
        qcode_mapping = {
            "Yes, we gave third parties access to our big data": {
                "qcode": "778",
                "ticked": "10",
                "unticked": "01"
            },
            "No, we did not give third parties access to our big data": {
                "qcode": "778",
                "ticked": "01",
                "unticked": "10"
            },
            "We did not hold any big data": {
                "qcode": "779",
                "ticked": "1",
                "unticked": "0",
                "excluder": "True"
            }
        }

        expected = {"778": "10", "779": "0"}
        actual = des_transformer.multi_qcode_radio_button("Yes, we gave third parties access to our big data", qcode_mapping)
        self.assertEqual(expected, actual)

        expected = {"778": "01", "779": "0"}
        actual = des_transformer.multi_qcode_radio_button("No, we did not give third parties access to our big data", qcode_mapping)
        self.assertEqual(expected, actual)

        expected = {"778": "", "779": "1"}
        actual = des_transformer.multi_qcode_radio_button("We did not hold any big data", qcode_mapping)
        self.assertEqual(expected, actual)

    def test_comment(self):
        self.assertEqual("10", des_transformer.comment("my comment", "10", "01"))
        self.assertEqual("01", des_transformer.comment("", "10", "01"))

    def test_transforms(self):
        transformations = {
            "022": [Transform.VALUE],
            "356": [
                Transform.RADIO,
                {
                    "Yes": "10",
                    "No": "01"
                }
            ],
            "277": [
                Transform.MULTI_RADIO,
                {
                    "Less than 2Mbps": {
                        "qcode": "277",
                        "ticked": "1",
                        "unticked": "0"
                    },
                    "2Mbps or more, but less than 10Mbps": {
                        "qcode": "278",
                        "ticked": "1",
                        "unticked": "0"
                    },
                    "10Mbps or more, but less than 30Mbps": {
                        "qcode": "279",
                        "ticked": "1",
                        "unticked": "0"
                    }
                }
            ],
            "600": [Transform.CHECKBOX, "1", "0"],
            "601": [Transform.CHECKBOX, "1", "0"],
            "610": [Transform.THOUSANDS],
            "612": [Transform.THOUSANDS],
            "500": [Transform.COMMENT, "1", "0"]
        }

        response_data = {
            "022": "80",
            "356": "Yes, we use a fixed broadband connection",
            "277": "Less than 2Mbps",
            "600": "App",
            "612": "42700",
            "500": "My comment!"
        }

        expected = {
            "022": "80",
            "356": "10",
            "277": "1",
            "278": "0",
            "279": "0",
            "600": "1",
            "601": "0",
            "610": "",
            "612": "43",
            "500": "1",
        }

        actual = perform_transform(response_data, transformations)

        self.assertEqual(expected, actual)
