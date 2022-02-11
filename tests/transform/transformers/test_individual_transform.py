import json
import unittest

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

        filename = "./tests/pck/common_software/202.1808.json"
        expected_filename = "./tests/pck/common_software/202.1808.nobatch"

        submission_dict = get_file_as_dict(filename)
        expected = get_file_as_string(expected_filename)
        print("Expected:")
        print(expected)

        transformer = get_transformer(submission_dict)
        pck_name, pck = transformer.create_pck()

        actual = pck
        print(" ")
        print("Actual:")
        print(actual)

        self.assertEqual(expected, actual)
