import glob
import json
import os
import unittest

from transform.transformers.response import SurveyResponse
from transform.transformers.transform_selector import get_transformer


def get_v3_responses():
    return glob.glob("./tests/pck/eq_comparison/v3/*.json")


def get_v2_path(v3_path: str):
    return f"./tests/pck/eq_comparison/v2/{os.path.basename(v3_path)}"


def get_file_as_dict(filename):
    with open(filename, encoding="utf-8") as fh:
        content = fh.read()
        return json.loads(content)


class TestCompareV2V3(unittest.TestCase):

    def test_compare_pck(self):

        self.maxDiff = None

        test_scenarios = get_v3_responses()

        for v3_response_path in test_scenarios:
            v3_dict = get_file_as_dict(v3_response_path)
            v2_dict = get_file_as_dict(get_v2_path(v3_response_path))

            transformer = get_transformer(SurveyResponse(v3_dict))
            pck_name_3, pck_v3 = transformer.create_pck()

            transformer = get_transformer(SurveyResponse(v2_dict))
            pck_name_2, pck_v2 = transformer.create_pck()

            print(" ")
            print(v3_response_path)

            print("\n======V3=======\n")
            print(pck_v3)

            print("\n======V2=======\n")
            print(pck_v2)

            self.assertEqual(pck_v2, pck_v3)
