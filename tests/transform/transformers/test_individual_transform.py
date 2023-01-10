import json
import unittest

from transform.transformers.response import SurveyResponse
from transform.transformers.transform_selector import get_transformer


def get_file_as_string(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents


def get_file_as_dict(filename):

    with open(filename, encoding="utf-8") as fh:
        content = fh.read()
        return json.loads(content)


class TestIndividualSurveyTransformer(unittest.TestCase):

    def test_transform_pck(self):

        self.maxDiff = None

        filename = "./tests/pck/cord/187.0002.json"
        expected_filename = "./tests/pck/cord/187.0002.pck"

        submission_dict = get_file_as_dict(filename)
        expected = get_file_as_string(expected_filename)
        print("\n======EXPECTED=======\n")
        print(expected)

        transformer = get_transformer(SurveyResponse(submission_dict))
        pck_name, pck = transformer.create_pck()

        actual = pck
        print("\n======ACTUAL=======\n")
        print(actual)

        self.assertEqual(expected, actual)
