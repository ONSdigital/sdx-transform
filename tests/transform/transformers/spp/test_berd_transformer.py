import json
import unittest

from transform.transformers.spp.berd.berd_transformer import Answer, extract_answers, convert_to_spp, SPP


class ExtractAnswerTests(unittest.TestCase):

    def test_match_value_to_code(self):
        data = {
            "answers": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "value": "Yes"
                },
            ],
            "lists": [],
            "answer_codes": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "code": "101"
                }
            ]
        }

        actual = extract_answers(data)
        expected = [Answer("101", "Yes", None, None)]

        self.assertEqual(actual, expected)

    def test_match_multiple_values_to_codes(self):
        data = {
            "answers": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "value": "Yes"
                },
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388b",
                    "value": "No"
                }
            ],
            "lists": [],
            "answer_codes": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388b",
                    "code": "101"
                },
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "code": "102"
                }
            ]
        }

        actual = extract_answers(data)
        expected = [Answer("102", "Yes", None, None), Answer("101", "No", None, None)]

        self.assertEqual(actual, expected)

    def test_add_list_item_id_to_answer(self):
        data = {
            "answers": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "value": "Yes",
                    "list_item_id": "YxAbgY"
                },
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388b",
                    "value": "No",
                    "list_item_id": "IBzcQr"
                }
            ],
            "lists": [
                {"items": ["YxAbgY", "IBzcQr"], "name": "product_codes"}
            ],
            "answer_codes": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388b",
                    "code": "101"
                },
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "code": "102"
                }
            ]
        }

        actual = extract_answers(data)
        expected = [Answer("102", "Yes", "YxAbgY", "product_codes"), Answer("101", "No", "IBzcQr", "product_codes")]

        self.assertEqual(actual, expected)

    def test_add_list_item_ids_with_letters(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a2", "value": "No", "list_item_id": "aaa"},
                {"answer_id": "a3", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a4", "value": "No", "list_item_id": "aaa"},
            ],
            "lists": [
                {"items": ["aaa"], "name": "product_codes"}
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "c101"},
                {"answer_id": "a2", "code": "c102"},
                {"answer_id": "a3", "code": "d101"},
                {"answer_id": "a4", "code": "d102"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "Yes", "caaa", "product_codes"),
            Answer("102", "No", "caaa", "product_codes"),
            Answer("101", "Yes", "daaa", "product_codes"),
            Answer("102", "No", "daaa", "product_codes"),
        ]

        self.assertEqual(actual, expected)

    def test_add_list_item_ids_with_letters_and_groups(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a2", "value": "No", "list_item_id": "aaa"},
                {"answer_id": "a3", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a4", "value": "No", "list_item_id": "aaa"},
                {"answer_id": "a5", "value": "Yes", "list_item_id": "bbb"},
                {"answer_id": "a6", "value": "No", "list_item_id": "bbb"},
                {"answer_id": "a7", "value": "Yes", "list_item_id": "ccc"},
                {"answer_id": "a8", "value": "No", "list_item_id": "ccc"},
                {"answer_id": "a9", "value": "x"},
                {"answer_id": "a10", "value": "y"},
            ],
            "lists": [
                {"items": ["aaa", "bbb"], "name": "product1"},
                {"items": ["ccc"], "name": "product2"},
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "c101"},
                {"answer_id": "a2", "code": "c102"},
                {"answer_id": "a3", "code": "d101"},
                {"answer_id": "a4", "code": "d102"},
                {"answer_id": "a5", "code": "c101"},
                {"answer_id": "a6", "code": "c102"},
                {"answer_id": "a7", "code": "c103"},
                {"answer_id": "a8", "code": "c104"},
                {"answer_id": "a9", "code": "105"},
                {"answer_id": "a10", "code": "106"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "Yes", "caaa", "product_codes"),
            Answer("102", "No", "caaa", "product_codes"),
            Answer("101", "Yes", "daaa", "product_codes"),
            Answer("102", "No", "daaa", "product_codes"),
            Answer("101", "Yes", "caaa", "product_codes"),
            Answer("102", "No", "caaa", "product_codes"),
            Answer("101", "Yes", "daaa", "product_codes"),
            Answer("102", "No", "daaa", "product_codes"),
            Answer("103", "x", None, None),
            Answer("104", "y", None, None),
        ]

        self.assertEqual(actual, expected)



class CovertToSppTests(unittest.TestCase):

    def test_convert_to_spp(self):
        answer_list = [Answer("102", "Yes", "YxAbgY", "product_codes"),
                       Answer("101", "No", "IBzcQr", "product_codes")]
        actual = convert_to_spp(answer_list)
        expected = [SPP("102", "Yes", 1), SPP("101", "No", 1)]

        self.assertEqual(actual, expected)

    def test_convert_to_spp_with_multiple_instances(self):
        answer_list = [Answer("101", "No", "123", "product_codes"),
                       Answer("102", "Yes", "321", "product_codes")]
        actual = convert_to_spp(answer_list)
        expected = [SPP("101", "No", 1), SPP("102", "Yes", 2)]

        self.assertEqual(actual, expected)

    def test_convert_to_spp_with_multiple_groups(self):
        answer_list = [
            Answer("101", "No", "123", "product_codes"),
            Answer("102", "Yes", "321", "product_codes"),
            Answer("103", "Yes", "321", "product_codes_2")
        ]
        actual = convert_to_spp(answer_list)
        expected = [SPP("101", "No", 1), SPP("102", "Yes", 2), SPP("103", "Yes", 1)]

        self.assertEqual(actual, expected)

    def test_convert_to_spp_with_multiple_groups_2(self):
        answer_list = [
            Answer("100", "Yes", None, None),
            Answer("101", "No", None, None),
            Answer("102", "No", "123", "group_1"),
            Answer("102", "Yes", "321", "group_1"),
            Answer("102", "No", "144", "group_1"),
            Answer("256", "Yes", "999", "group_2"),
            Answer("257", "No", "999", "group_2"),
            Answer("389", "Yes", "321", "group_3"),
            Answer("303", "Yes", "444", "group_3"),
            Answer("309", "Yes", "444", "group_3"),
            Answer("303", "Yes", "555", "group_3"),

        ]
        actual = convert_to_spp(answer_list)
        expected = [
            SPP("100", "Yes", 0),
            SPP("101", "No", 0),
            SPP("102", "No", 1),
            SPP("102", "Yes", 2),
            SPP("102", "No", 3),
            SPP("256", "Yes", 1),
            SPP("257", "No", 1),
            SPP("389", "Yes", 1),
            SPP("303", "Yes", 2),
            SPP("309", "Yes", 2),
            SPP("303", "Yes", 3),
        ]

        self.assertEqual(actual, expected)

    def test_convert_civil_and_defence_internal_only(self):
        answer_list = [
            Answer("101", "No", "c111", "product_codes"),
            Answer("102", "Yes", "c111", "product_codes"),
            Answer("101", "No", "d111", "product_codes"),
            Answer("102", "Yes", "d111", "product_codes"),
            Answer("101", "No", "c222", "product_codes"),
            Answer("102", "Yes", "c222", "product_codes"),
        ]
        actual = convert_to_spp(answer_list)
        expected = [
            SPP("101", "No", 1), SPP("102", "Yes", 1),
            SPP("101", "No", 2), SPP("102", "Yes", 2),
            SPP("101", "No", 3), SPP("102", "Yes", 3),
        ]

        self.assertEqual(actual, expected)


class ExampleTests(unittest.TestCase):

    def test_example_berd(self):
        f = open("transform/transformers/spp/berd/berd_example.json")
        result: list = json.load(f)

        data = result["data"]
        extracted = convert_to_spp(extract_answers(data))

        for line in extracted:
            print(line)
