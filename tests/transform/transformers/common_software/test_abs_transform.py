import json
import unittest

from transform.transformers.common_software.abs_transformer import ABSTransformer
from transform.transformers.common_software.cs_formatter import CSFormatter


class ABSTests(unittest.TestCase):

    def test_idbr_receipt(self):
        """
        Tests inter-departmental business register receipt
        """
        return_value = CSFormatter._idbr_receipt("202", "12346789012", "A", "21")
        self.assertEqual("12346789012:A:202:202112", return_value)

    def test_pck_name(self):
        with open("tests/replies/202.1802.json", "r") as fp:
            response = json.load(fp)

        response['tx_id'] = "11111111-2222-3333-4444-555555555555"
        print(response)
        pck_name, pck = ABSTransformer(response).create_pck()
        self.assertEqual("053_1111111122223333", pck_name)
