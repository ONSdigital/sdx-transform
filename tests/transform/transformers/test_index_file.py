import json
import time
import unittest

from transform.transformers.index_file import IndexFile
from transform.transformers.response import SurveyResponseV1


class IndexFileTests(unittest.TestCase):

    def setUp(self):
        with open("./tests/data/eq-mwss.json") as fb:
            data = fb.read()
        self.response = SurveyResponseV1(json.loads(data))
        self.image_names = ["Image1", "Image2"]

    # Not normal to test private variables , but setting current_time=datetime.datetime.utcnow() in init
    # will pass all tests but lead to a fixed date time in prod. IndexFile._current_time only exists for this test
    def test_date_not_set_at_initialisation(self):
        sut1 = IndexFile(self.response, len(self.image_names), self.image_names)
        time.sleep(0.01)
        sut2 = IndexFile(self.response, len(self.image_names), self.image_names)

        self.assertNotEqual(sut1._current_time, sut2._current_time)
