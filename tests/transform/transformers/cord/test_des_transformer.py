import unittest

from transform.transformers.cord.des import des_transformer


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

    def test_comment(self):
        self.assertEqual("10", des_transformer.comment("my comment", "10", "01"))
        self.assertEqual("01", des_transformer.comment("", "10", "01"))
