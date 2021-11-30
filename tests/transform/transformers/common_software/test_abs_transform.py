import unittest

from transform.transformers.common_software.cs_formatter import CSFormatter


class ABSTests(unittest.TestCase):

    def test_idbr_receipt(self):
        """
        Tests inter-departmental business register receipt
        """
        return_value = CSFormatter._idbr_receipt("202", "12346789012", "A", "21")
        self.assertEqual("12346789012:A:202:202112", return_value)
