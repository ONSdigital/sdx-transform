import unittest

from transform.transformers.common_software.sand_and_gravel.marine_dredged_transformer import perform_transforms
from transform.transformers.common_software.sand_and_gravel.marine_dredged_transforms import Transform


class MarineTests(unittest.TestCase):

    def test_unit_test_sets_0_with_string(self):
        data = {
            "601": "hello",
            "602": "20",
            "603": "30",
        }

        transform_spec = {
            "601": Transform.UNIT,
            "602": Transform.UNIT,
            "603": Transform.UNIT,
        }

        addition_spec = {
            "101": ["601", "602", "603"]
        }

        expected = {
            "601": 0,
            "602": 20,
            "603": 30,
            "101": 50,
        }

        actual = perform_transforms(data, transform_spec, addition_spec)

        self.assertEqual(expected, actual)

    def test_full_survey(self):
        data = {
            "999": "Sand",
            "998": "Gravel, Pebbles, Shingle, Flint",
            "997": "Sand and gravel used for constructional fill",
            "601": "10",
            "602": "20",
            "603": "30",
            "604": "100",
            "605": "200",
            "606": "300",
            "607": "1000",
            "995": "portsmouth",
            "148": "Here is a good comment",
            "146": "Another good comment"
        }

        transform_spec = {
            "601": Transform.UNIT,
            "602": Transform.UNIT,
            "603": Transform.UNIT,
            "604": Transform.UNIT,
            "605": Transform.UNIT,
            "606": Transform.UNIT,
            "607": Transform.UNIT,
            "146": Transform.TEXT,
            "148": Transform.TEXT,
        }

        addition_spec = {
            "608": ["601", "602", "603", "604", "605", "606", "607"]
        }

        actual = perform_transforms(data, transform_spec, addition_spec)

        expected = {
            "601": 10,
            "602": 20,
            "603": 30,
            "604": 100,
            "605": 200,
            "606": 300,
            "607": 1000,
            "146": 1,
            "148": 1,
            "608": 1660
        }

        self.assertEqual(expected, actual)
