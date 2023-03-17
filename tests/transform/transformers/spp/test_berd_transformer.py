import json
import unittest

from transform.transformers.response import InvalidDataException, SurveyResponse, SurveyResponseV1
from transform.transformers.spp.berd.berd_transformer import BERDTransformer
from transform.transformers.spp.berd.collect_items import collect_list_items
from transform.transformers.spp.convert_data import convert_to_spp, extract_answers
from transform.transformers.spp.definitions import Answer, SPP


class BERDTransformerTests(unittest.TestCase):

    def test_full_transform(self):
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
                {"answer_id": "a11", "value": "x"},
                {"answer_id": "a12", "value": "y"},
                {"answer_id": "a13", "value": "x"},
                {"answer_id": "a14", "value": "y"},
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
                {"answer_id": "a11", "code": "56e107"},
                {"answer_id": "a12", "code": "56e108"},
                {"answer_id": "a13", "code": "56f107"},
                {"answer_id": "a14", "code": "56f108"},
            ]
        }

        response = SurveyResponse({})
        response.tx_id = "40809d1f-5efa-41e3-91b8-5b63f1da9bd0"
        response.survey_id = "002"
        response.instrument_id = "0001"
        response.ru_ref = "12346789012A"
        response.period = "202212"
        response.data = data

        transformer = BERDTransformer(response)
        filename, result = transformer.get_json()
        json_dict = json.loads(result)

        expected = {
            'formtype': '0001',
            'reference': '12346789012A',
            'period': '202212',
            'survey': '002',
            'responses': [
                {'questioncode': '101', 'response': 'Yes', 'instance': 1},
                {'questioncode': '102', 'response': 'No', 'instance': 1},
                {'questioncode': '101', 'response': 'Yes', 'instance': 2},
                {'questioncode': '102', 'response': 'No', 'instance': 2},
                {'questioncode': '101', 'response': 'Yes', 'instance': 3},
                {'questioncode': '102', 'response': 'No', 'instance': 3},
                {'questioncode': '103', 'response': 'Yes', 'instance': 1},
                {'questioncode': '104', 'response': 'No', 'instance': 1},
                {'questioncode': '105', 'response': 'x', 'instance': 0},
                {'questioncode': '106', 'response': 'y', 'instance': 0},
                {'questioncode': '107', 'response': 'x', 'instance': 1},
                {'questioncode': '108', 'response': 'y', 'instance': 1},
                {'questioncode': '107', 'response': 'x', 'instance': 2},
                {'questioncode': '108', 'response': 'y', 'instance': 2}
            ]
        }

        self.assertEqual("002_40809d1f5efa41e3.json", filename)
        self.assertEqual(expected, json_dict)

    def test_invalid_transform(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Yes", "list_item_id": "aaa"},

            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "c101"},
            ]
        }

        response = SurveyResponse({})
        response.tx_id = "40809d1f-5efa-41e3-91b8-5b63f1da9bd0"
        response.survey_id = "002"
        response.instrument_id = "0001"
        response.ru_ref = "12346789012A"
        response.period = "202212"
        response.data = data

        with self.assertRaises(InvalidDataException):
            BERDTransformer(response)

    def test_extract_answers(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Civil Research and Development", "list_item_id": "qObPqR"},
                {"answer_id": "a1", "value": "Defence Research and Development", "list_item_id": "Uztndf"},
                {"answer_id": "a1", "value": "Both, civil and defence Research and Development", "list_item_id": "GjDKpD"},
                {"answer_id": "a6", "value": "1 - Agriculture", "list_item_id": "qObPqR"},
                {"answer_id": "a6", "value": "2 - Mining and quarrying", "list_item_id": "Uztndf"},
                {"answer_id": "a6", "value": "3 - Food products and beverages", "list_item_id": "GjDKpD"},
                {"answer_id": "a2", "value": 10000, "list_item_id": "qObPqR"},
                {"answer_id": "a2", "value": 5000, "list_item_id": "GjDKpD"},
                {"answer_id": "a3", "value": 5000, "list_item_id": "qObPqR"},
                {"answer_id": "a3", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a4", "value": 1000, "list_item_id": "Uztndf"},
                {"answer_id": "a4", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a5", "value": 500, "list_item_id": "Uztndf"},
                {"answer_id": "a5", "value": 1000, "list_item_id": "GjDKpD"}
            ],
            "lists": [
                {"items": ["qObPqR", "Uztndf", "GjDKpD"], "name": "product_codes"},
                {"items": ["ebQYeQ", "ImViOn"], "name": "product_codes_2"}
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "200"},
                {"answer_id": "a6", "code": "201"},
                {"answer_id": "a2", "code": "c202"},
                {"answer_id": "a3", "code": "c203"},
                {"answer_id": "a4", "code": "d202"},
                {"answer_id": "a5", "code": "d203"}
            ]
        }

        expected = [
            Answer(qcode='200', value='Civil Research and Development', list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='200', value='Defence Research and Development', list_item_id='Uztndf', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='GjDKpD', group='product_codes'),
            Answer(qcode='201', value='1 - Agriculture', list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='201', value='2 - Mining and quarrying', list_item_id='Uztndf', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='GjDKpD', group='product_codes'),
            Answer(qcode='c202', value='10000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c202', value='5000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='c203', value='5000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c203', value='3000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='d202', value='1000', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d202', value='3000', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='d203', value='500', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d203', value='1000', list_item_id='dGjDKpD', group='product_codes')]

        actual = extract_answers(data)
        self.assertEqual(expected, actual)

    def test_collected_list_items(self):
        answer_list = [
            Answer(qcode='200', value='Civil Research and Development', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='200', value='Defence Research and Development', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='201', value='1 - Agriculture, hunting and forestry; fishing', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='201', value='2 - Mining and quarrying (including solids, liquids and gases)', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='c202', value='10000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c202', value='5000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='c203', value='5000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c203', value='3000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='d202', value='1000', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d202', value='3000', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='d203', value='500', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d203', value='1000', list_item_id='dGjDKpD', group='product_codes')
        ]

        expected = [
            SPP(questioncode='200', response='Civil Research and Development', instance=1),
            SPP(questioncode='200', response='Defence Research and Development', instance=2),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=3),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=4),
            SPP(questioncode='201', response='1 - Agriculture, hunting and forestry; fishing', instance=1),
            SPP(questioncode='201', response='2 - Mining and quarrying (including solids, liquids and gases)', instance=2),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=3),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=4),
            SPP(questioncode='c202', response='10000', instance=1),
            SPP(questioncode='c202', response='5000', instance=3),
            SPP(questioncode='c203', response='5000', instance=1),
            SPP(questioncode='c203', response='3000', instance=3),
            SPP(questioncode='d202', response='1000', instance=2),
            SPP(questioncode='d202', response='3000', instance=4),
            SPP(questioncode='d203', response='500', instance=2),
            SPP(questioncode='d203', response='1000', instance=4)
        ]

        actual = convert_to_spp(answer_list)
        self.assertEqual(expected, actual)

    def test_full_example(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Civil Research and Development", "list_item_id": "qObPqR"},
                {"answer_id": "a1", "value": "Defence Research and Development", "list_item_id": "Uztndf"},
                {"answer_id": "a1", "value": "Both, civil and defence Research and Development",
                 "list_item_id": "GjDKpD"},
                {"answer_id": "a6", "value": "1 - Agriculture, hunting and forestry; fishing",
                 "list_item_id": "qObPqR"},
                {"answer_id": "a6", "value": "2 - Mining and quarrying (including solids, liquids and gases)",
                 "list_item_id": "Uztndf"},
                {"answer_id": "a6", "value": "3 - Food products and beverages", "list_item_id": "GjDKpD"},
                {"answer_id": "a2", "value": 10000, "list_item_id": "qObPqR"},
                {"answer_id": "a2", "value": 5000, "list_item_id": "GjDKpD"},
                {"answer_id": "a3", "value": 5000, "list_item_id": "qObPqR"},
                {"answer_id": "a3", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a4", "value": 1000, "list_item_id": "Uztndf"},
                {"answer_id": "a4", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a5", "value": 500, "list_item_id": "Uztndf"},
                {"answer_id": "a5", "value": 1000, "list_item_id": "GjDKpD"}
            ],
            "lists": [
                {"items": ["qObPqR", "Uztndf", "GjDKpD"], "name": "product_codes"},
                {"items": ["ebQYeQ", "ImViOn"], "name": "product_codes_2"}
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "200"},
                {"answer_id": "a6", "code": "201"},
                {"answer_id": "a2", "code": "c202"},
                {"answer_id": "a3", "code": "c203"},
                {"answer_id": "a4", "code": "d202"},
                {"answer_id": "a5", "code": "d203"}
            ]
        }

        expected = [
             SPP(questioncode='200', response='Civil Research and Development', instance=1),
             SPP(questioncode='200', response='Defence Research and Development', instance=2),
             SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=3),
             SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=4),
             SPP(questioncode='201', response='1 - Agriculture, hunting and forestry; fishing', instance=1),
             SPP(questioncode='201', response='2 - Mining and quarrying (including solids, liquids and gases)',
                 instance=2),
             SPP(questioncode='201', response='3 - Food products and beverages', instance=3),
             SPP(questioncode='201', response='3 - Food products and beverages', instance=4),
             SPP(questioncode='c202', response='10000', instance=1),
             SPP(questioncode='c202', response='5000', instance=3),
             SPP(questioncode='c203', response='5000', instance=1),
             SPP(questioncode='c203', response='3000', instance=3),
             SPP(questioncode='d202', response='1000', instance=2),
             SPP(questioncode='d202', response='3000', instance=4),
             SPP(questioncode='d203', response='500', instance=2),
             SPP(questioncode='d203', response='1000', instance=4)
        ]

        actual = convert_to_spp(collect_list_items(extract_answers(data)))

        self.assertEqual(expected, actual)

    def test_from_file(self):
        with open('tests/transform/transformers/spp/berd_survey_v1.json') as f:
            response = json.load(f)
        print(response)
        survey_response = SurveyResponseV1(response)
        transformer = BERDTransformer(survey_response)
        print(json.dumps(survey_response.response))
        print(transformer.get_json()[1])
