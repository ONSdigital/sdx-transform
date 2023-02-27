import unittest

from transform.transformers.spp.berd.berd_transformer import Answer


class BerdTransformerTests(unittest.TestCase):
    """
    Final output reqs:

    """

    def test_get_correct_qcode_from_json(self):
        data = {
            "answers": [
                {
                    "answer_id": "answerb3840e82-aeaf-4a85-8556-84f2e1e5388a",
                    "value": "Yes, I can report for this period"
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

        answer = Answer()
        answer.qcode = 1
        pass
