import json
import os
import unittest

from sdx_gcp.app import SdxApp

from transform.views.main import transform


def get_file_as_string(filename):

    f = open(filename)
    contents = f.read()

    f.close()

    return contents


def get_expected_file(filename, output_type):
    filename, _ = os.path.splitext(filename)
    return "%s.%s" % (filename, output_type)


def get_expected_output(filename, output_type):
    output_filename = get_expected_file(filename, output_type)

    print("Loading expected output %s " % output_filename)

    return get_file_as_string(output_filename)


class TestTransformService(unittest.TestCase):

    transform_endpoint = "/transform"

    def setUp(self):
        sdx_app = SdxApp("sdx-transform")

        sdx_app.add_post_endpoint(transform, rule="/transform")

        app = sdx_app.app

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    def test_invalid_input(self):
        r = self.app.post(self.transform_endpoint, data="rubbish")

        self.assertEqual(400, r.status_code)

    def test_invalid_survey_id(self):
        # Create an invalid survey id payload
        payload_str = get_file_as_string("./tests/pck/common_software/017.0001.json")
        payload_object = json.loads(payload_str)
        payload_object["survey_id"] = "666"
        payload = json.dumps(payload_object)

        r = self.app.post(self.transform_endpoint, data=payload)
        self.assertEqual(400, r.status_code)

    def test_missing_survey_id(self):
        # Create a survey with missing survey id
        payload_str = get_file_as_string("./tests/pck/common_software/017.0001.json")
        payload_object = json.loads(payload_str)
        del payload_object["survey_id"]
        payload = json.dumps(payload_object)

        r = self.app.post(self.transform_endpoint, data=payload)

        self.assertEqual(r.status_code, 400)
