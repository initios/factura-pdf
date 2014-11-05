# coding=utf-8
import unittest
from facturapdf import chunks


class TestHelper(unittest.TestCase):
    def test_chunks(self):
        collection = [1, 2, 3, 4, 5]
        chunks_collection = chunks(collection, 2)

        self.assertEqual([[1, 2], [3, 4], [5]], chunks_collection)

    def test_chunks_with_a_fill_value(self):
        collection = [1, 2, 3, 4, 5]
        chunks_collection = chunks(collection, 2, 9)

        self.assertEqual([[1, 2], [3, 4], [5, 9]], chunks_collection)

    def test_chunks_with_a_fill_value_in_a_multidimensional_list(self):
        collection = [[1, 2], [3, 4], [5]]
        chunks_collection = chunks(collection, 2, 9, True)

        self.assertEqual([ [[1, 2], [3, 4]], [[5, 9]] ], chunks_collection)