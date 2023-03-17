import unittest

from transform.transformers.spp.berd.collect_items import is_subset_of, collect_list_items
from transform.transformers.spp.definitions import Answer


class CollectItemsTests(unittest.TestCase):

    def test_is_subset_of(self):
        list_item_id = 'qObPqR'
        compare_with = 'cqObPqR'
        self.assertTrue(is_subset_of(list_item_id, compare_with))

    def test_is_not_subset_of(self):
        list_item_id = 'qObPqR'
        compare_with = 'cqObTqR'
        self.assertFalse(is_subset_of(list_item_id, compare_with))

    def test_same_is_not_subset_of(self):
        list_item_id = 'qObPqR'
        compare_with = 'qObPqR'
        self.assertFalse(is_subset_of(list_item_id, compare_with))

    def test_collect_simple(self):
        answer_list = [
            Answer(qcode='200', value="1", list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
        ]

        expected = [
            Answer(qcode='200', value="1", list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
        ]

        actual = collect_list_items(answer_list)
        self.assertEqual(expected, actual)

    def test_collect_no_item_id(self):
        answer_list = [
            Answer(qcode='101', value="Yes", list_item_id=None, group=None),
            Answer(qcode='200', value="1", list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
        ]

        expected = [
            Answer(qcode='101', value="Yes", list_item_id=None, group=None),
            Answer(qcode='200', value="1", list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
        ]

        actual = collect_list_items(answer_list)
        self.assertEqual(expected, actual)

    def test_collect_creates_new_answer(self):
        answer_list = [
            Answer(qcode='200', value="1", list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='d201', value="3", list_item_id='dqObPqR', group='product_codes'),
        ]

        expected = [
            Answer(qcode='200', value="1", list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='200', value="1", list_item_id='dqObPqR', group='product_codes'),
            Answer(qcode='c201', value="2", list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='d201', value="3", list_item_id='dqObPqR', group='product_codes'),
        ]

        actual = collect_list_items(answer_list)
        self.assertEqual(expected, actual)

    def test_large_collect_list_items(self):
        answer_list = [
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

        expected = [
            Answer(qcode='200', value='Civil Research and Development', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='200', value='Defence Research and Development', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='201', value='1 - Agriculture', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='201', value='2 - Mining and quarrying', list_item_id='dUztndf', group='product_codes'),
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

        def sort_func(answer: Answer) -> str:
            return answer.qcode

        actual = collect_list_items(answer_list)
        self.assertEqual(expected.sort(key=sort_func), actual.sort(key=sort_func))
