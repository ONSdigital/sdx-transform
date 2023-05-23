import unittest

from transform.transformers.common_software.sand_and_gravel.land_won_transformer import Transform,\
    perform_transforms


class LandTests(unittest.TestCase):

    def test_addition_spec(self):
        data = {
            "101": "",
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
            "147": "Here is a good comment",
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
            "147": Transform.TEXT,
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
            "147": 1,
            "608": 1660
        }

        self.assertEqual(expected, actual)
