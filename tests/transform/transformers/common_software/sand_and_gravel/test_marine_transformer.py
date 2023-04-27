import unittest

from transform.transformers.common_software.sand_and_gravel.marine_dredged_transformer import perform_transforms
from transform.transformers.common_software.sand_and_gravel.marine_dredged_transforms import Transform


class MarineTests(unittest.TestCase):

    def test_full_survey(self):
        data = {
            "999": "Sand",
            "998": "Gravel, Pebbles, Shingle, Flint",
            "997": "Sand and gravel used for constructional fill",
            "601": "10",
            "602": "100",
            "603": "1000",
            "604": "20",
            "605": "200",
            "606": "2000",
            "607": "3000",
            "995": "PORTSMOUTH",
            "148": "hello",
            "146": "hello again"
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
            "602": 100,
            "603": 1000,
            "604": 20,
            "605": 200,
            "606": 2000,
            "607": 3000,
            "146": 1,
            "148": 1,
            "608": 6330
        }

        self.assertEqual(expected, actual)
