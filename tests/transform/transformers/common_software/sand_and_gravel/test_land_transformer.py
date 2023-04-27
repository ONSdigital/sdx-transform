import unittest

from transform.transformers.common_software.sand_and_gravel.land_won_transformer import Transform,\
    perform_transforms


class LandTests(unittest.TestCase):

    def test_addition_spec(self):
        data = {
            "101": "0",
            "102": "10",
            "103": "10",
            "999": "1000"
        }

        transform_spec = {
            "101": Transform.UNIT,
            "102": Transform.UNIT,
            "103": Transform.UNIT
        }

        addition_spec = {
            "200": ["101", "102", "103"]
        }

        actual = perform_transforms(data, transform_spec, addition_spec)

        expected = {
            "101": 0,
            "102": 10,
            "103": 10,
            "200": 20
        }

        self.assertEqual(expected, actual)

    def test_comments_transform(self):
        data = {
            "101": "0",
            "102": "10",
            "201": "hello",
            "202": "",
        }

        transform_spec = {
            "101": Transform.UNIT,
            "102": Transform.UNIT,
            "201": Transform.TEXT,
            "202": Transform.TEXT
        }

        addition_spec = {}

        actual = perform_transforms(data, transform_spec, addition_spec)

        expected = {
            "101": 0,
            "102": 10,
            "201": 1,
            "202": 2
        }

        self.assertEqual(expected, actual)
