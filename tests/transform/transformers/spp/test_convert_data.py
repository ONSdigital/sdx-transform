import unittest

from transform.transformers.spp.convert_data import convert_to_spp, extract_answers, remove_prepend_values
from transform.transformers.spp.definitions import Answer, SPP


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

        self.assertEqual(expected, actual)

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

        self.assertEqual(expected, actual)

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

        self.assertEqual(expected, actual)

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
            Answer("c101", "Yes", "caaa", "product_codes"),
            Answer("c102", "No", "caaa", "product_codes"),
            Answer("d101", "Yes", "daaa", "product_codes"),
            Answer("d102", "No", "daaa", "product_codes"),
        ]

        self.assertEqual(expected, actual)

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
            Answer("c101", "Yes", "caaa", "product1"),
            Answer("c102", "No", "caaa", "product1"),
            Answer("d101", "Yes", "daaa", "product1"),
            Answer("d102", "No", "daaa", "product1"),
            Answer("c101", "Yes", "cbbb", "product1"),
            Answer("c102", "No", "cbbb", "product1"),
            Answer("c103", "Yes", "cccc", "product2"),
            Answer("c104", "No", "cccc", "product2"),
            Answer("105", "x", None, None),
            Answer("106", "y", None, None),
        ]

        self.assertEqual(expected, actual)

    def test_create_list_item_for_prefixed_qcodes(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "x"},
                {"answer_id": "a2", "value": "y"},
                {"answer_id": "a3", "value": "z"},
            ],
            "lists": [],
            "answer_codes": [
                {"answer_id": "a1", "code": "101"},
                {"answer_id": "a2", "code": "e102"},
                {"answer_id": "a3", "code": "f102"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "x", None, None),
            Answer("e102", "y", "e_list_item", "default"),
            Answer("f102", "z", "f_list_item", "default"),
        ]

        self.assertEqual(expected, actual)

    def test_create_list_items_for_prefixed_qcodes(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "x"},
                {"answer_id": "a2", "value": "y"},
                {"answer_id": "a3", "value": "z"},
                {"answer_id": "a4", "value": "a"},
                {"answer_id": "a5", "value": "b"},
            ],
            "lists": [],
            "answer_codes": [
                {"answer_id": "a1", "code": "101"},
                {"answer_id": "a2", "code": "e102"},
                {"answer_id": "a3", "code": "f102"},
                {"answer_id": "a4", "code": "e103"},
                {"answer_id": "a5", "code": "f103"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "x", None, None),
            Answer("e102", "y", "e_list_item", "default"),
            Answer("f102", "z", "f_list_item", "default"),
            Answer("e103", "a", "e_list_item", "default"),
            Answer("f103", "b", "f_list_item", "default"),
        ]

        self.assertEqual(expected, actual)

    def test_create_list_items_for_prefixed_qcodes_two(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "x"},
                {"answer_id": "a2", "value": "y"},
                {"answer_id": "a3", "value": "z"},
                {"answer_id": "a4", "value": "a"},
                {"answer_id": "a5", "value": "b"},
            ],
            "lists": [],
            "answer_codes": [
                {"answer_id": "a1", "code": "101"},
                {"answer_id": "a2", "code": "2e102"},
                {"answer_id": "a3", "code": "2f102"},
                {"answer_id": "a4", "code": "2e103"},
                {"answer_id": "a5", "code": "2f103"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "x", None, None),
            Answer("2e102", "y", "e_list_item", "default"),
            Answer("2f102", "z", "f_list_item", "default"),
            Answer("2e103", "a", "e_list_item", "default"),
            Answer("2f103", "b", "f_list_item", "default"),
        ]

        self.assertEqual(expected, actual)

    def test_create_list_items_for_prefixed_qcodes_two_digit(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "x"},
                {"answer_id": "a2", "value": "y"},
                {"answer_id": "a3", "value": "z"},
                {"answer_id": "a4", "value": "a"},
                {"answer_id": "a5", "value": "b"},
            ],
            "lists": [],
            "answer_codes": [
                {"answer_id": "a1", "code": "101"},
                {"answer_id": "a2", "code": "12e102"},
                {"answer_id": "a3", "code": "12f102"},
                {"answer_id": "a4", "code": "12e103"},
                {"answer_id": "a5", "code": "12f103"},
            ]
        }

        actual = extract_answers(data)
        expected = [
            Answer("101", "x", None, None),
            Answer("12e102", "y", "e_list_item", "default"),
            Answer("12f102", "z", "f_list_item", "default"),
            Answer("12e103", "a", "e_list_item", "default"),
            Answer("12f103", "b", "f_list_item", "default"),
        ]

        self.assertEqual(expected, actual)


class CovertToSppTests(unittest.TestCase):

    def test_convert_to_spp(self):
        answer_list = [Answer("101", "Yes", "YxAbgY", "product_codes"),
                       Answer("102", "No", "IBzcQr", "product_codes")]
        actual = convert_to_spp(answer_list)
        expected = [SPP("101", "Yes", 1), SPP("102", "No", 2)]

        self.assertEqual(expected, actual)

    def test_convert_to_spp_with_multiple_instances(self):
        answer_list = [Answer("101", "No", "123", "product_codes"),
                       Answer("102", "Yes", "321", "product_codes")]
        actual = convert_to_spp(answer_list)
        expected = [SPP("101", "No", 1), SPP("102", "Yes", 2)]

        self.assertEqual(expected, actual)

    def test_convert_to_spp_with_multiple_groups(self):
        answer_list = [
            Answer("101", "No", "123", "product_codes"),
            Answer("102", "Yes", "321", "product_codes"),
            Answer("103", "Yes", "321", "product_codes_2")
        ]
        actual = convert_to_spp(answer_list)
        expected = [SPP("101", "No", 1), SPP("102", "Yes", 2), SPP("103", "Yes", 1)]

        self.assertEqual(expected, actual)

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

        self.assertEqual(expected, actual)

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

        self.assertEqual(expected, actual)

    def test_internal_and_external(self):
        answer_list = [
            Answer("101", "Yes", "caaa", "internal"),
            Answer("102", "No", "caaa", "internal"),
            Answer("101", "Yes", "daaa", "internal"),
            Answer("102", "No", "daaa", "internal"),
            Answer("101", "Yes", "cbbb", "internal"),
            Answer("102", "No", "cbbb", "internal"),
            Answer("103", "Yes", "cccc", "external"),
            Answer("104", "No", "cccc", "external"),
            Answer("105", "x", None, None),
            Answer("106", "y", None, None),
        ]

        actual = convert_to_spp(answer_list)
        expected = [
            SPP("101", "Yes", 1), SPP("102", "No", 1),
            SPP("101", "Yes", 2), SPP("102", "No", 2),
            SPP("101", "Yes", 3), SPP("102", "No", 3),
            SPP("103", "Yes", 1), SPP("104", "No", 1),
            SPP("105", "x", 0), SPP("106", "y", 0),
        ]

        self.assertEqual(expected, actual)

    def test_generated_list_items(self):
        answer_list = [
            Answer("101", "x", None, None),
            Answer("102", "y", "e_list_item", "default"),
            Answer("102", "z", "f_list_item", "default"),
            Answer("103", "a", "e_list_item", "default"),
            Answer("103", "b", "f_list_item", "default"),
        ]

        actual = convert_to_spp(answer_list)
        expected = [
            SPP("101", "x", 0),
            SPP("102", "y", 1),
            SPP("102", "z", 2),
            SPP("103", "a", 1),
            SPP("103", "b", 2),
        ]

        self.assertEqual(expected, actual)


class RemovePrependValuesTests(unittest.TestCase):

    def test_prepend_values(self):
        data = [
            {'questioncode': 'c101', 'response': 'Yes', 'instance': 1},
            {'questioncode': 'c102', 'response': 'No', 'instance': 1},
            {'questioncode': 'd101', 'response': 'Yes', 'instance': 2},
            {'questioncode': '56f108', 'response': 'y', 'instance': 2}
        ]

        actual = remove_prepend_values(data)

        expected = [
            {'questioncode': '101', 'response': 'Yes', 'instance': 1},
            {'questioncode': '102', 'response': 'No', 'instance': 1},
            {'questioncode': '101', 'response': 'Yes', 'instance': 2},
            {'questioncode': '108', 'response': 'y', 'instance': 2}
        ]

        self.assertEqual(expected, actual)

    def test_prepend_values_some_without_prefix(self):
        data = [
            {'questioncode': '101', 'response': 'Yes', 'instance': 0},
            {'questioncode': 'c102', 'response': 'No', 'instance': 1},
            {'questioncode': 'd102', 'response': 'Yes', 'instance': 2},
            {'questioncode': '56f108', 'response': 'y', 'instance': 2}
        ]

        actual = remove_prepend_values(data)

        expected = [
            {'questioncode': '101', 'response': 'Yes', 'instance': 0},
            {'questioncode': '102', 'response': 'No', 'instance': 1},
            {'questioncode': '102', 'response': 'Yes', 'instance': 2},
            {'questioncode': '108', 'response': 'y', 'instance': 2}
        ]

        self.assertEqual(expected, actual)
