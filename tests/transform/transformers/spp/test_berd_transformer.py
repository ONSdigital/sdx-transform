import json
import unittest

from transform.transformers.spp.berd.berd_transformer import Answer, extract_answers, convert_to_spp, SPP


class BerdTransformerTests(unittest.TestCase):
    """
    Final output reqs:

    """

    def test_get_correct_qcode_from_json(self):
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

    def test_get_multiple_qcodes_from_json(self):
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

    def test_convert_to_spp(self):
        answer_list = [Answer("102", "Yes", "YxAbgY", "product_codes"), Answer("101", "No", "IBzcQr", "product_codes")]
        actual = convert_to_spp(answer_list)
        expected = [SPP("102", "Yes", 1), SPP("101", "No", 1)]

        self.assertEqual(actual, expected)

    def test_convert_to_spp_with_multiple_instances(self):
        answer_list = [Answer("101", "No", "123", "product_codes"), Answer("102", "Yes", "321", "product_codes")]
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

    # def test_example_berd(self):
    #     f = open("transform/transformers/spp/berd/berd_example.json")
    #     result: list = json.load(f)
    #
    #     data = result["data"]
    #     extracted = extract_answers(data)
    #
    #     for line in extracted:
    #         print(line)