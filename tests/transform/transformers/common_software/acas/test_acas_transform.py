import unittest

from transform.transformers.common_software.acas.acas_transformer import perform_transforms
from transform.transformers.common_software.acas.acas_transforms import Transform


class TestPerformTransforms(unittest.TestCase):

    def test_currency(self):
        actual = perform_transforms({"123": "34567"}, {"123": Transform.CURRENCY})
        expected = {"123": "3000"}
        self.assertEqual(expected, actual)
