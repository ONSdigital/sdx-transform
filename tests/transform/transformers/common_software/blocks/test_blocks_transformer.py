import unittest

from transform.transformers.common_software.blocks.blocks_transformer import perform_transforms, Transform


class BricksTests(unittest.TestCase):

    def test_returns_qcodes_from_spec(self):
        data = {
            "999": "not in spec",
            "101": "100",
            "102": "20",
            "103": "15",
            "104": "Hello",
            "105": ""
        }

        transforms_spec = {
            "101": Transform.NO_TRANSFORM,
            "102": Transform.NO_TRANSFORM,
            "103": Transform.NO_TRANSFORM,
            "104": Transform.TEXT,
            "105": Transform.TEXT,
            "106": Transform.TEXT
        }

        actual = perform_transforms(data, transforms_spec)

        expected = {
            "101": 100,
            "102": 20,
            "103": 15,
            "104": 1,
            "105": 2,
            "106": 2
        }

        self.assertEqual(expected, actual)
