# coding=utf-8

import unittest

from reportlab import platypus

from facturapdf import flowables
from facturapdf.chapters import chapter, element
from facturapdf.helper import chunks


class HelperTest(unittest.TestCase):
    def test_chunks(self):
        collection = [1, 2, 3, 4, 5]
        chunks_collection = chunks(collection, 2)

        self.assertEqual([[1, 2], [3, 4], [5]], chunks_collection)

    def test_chunks_with_a_fill_value(self):
        collection = [1, 2, 3, 4, 5]
        chunks_collection = chunks(collection, 2, 9)

        self.assertEqual([[1, 2], [3, 4], [5, 9]], chunks_collection)


class ElementTest(unittest.TestCase):
    def test_can_create_frame_breaks(self):
        self.assertIsInstance(element('framebreak'), platypus.doctemplate._FrameBreak)

    def test_can_create_simple_line_flowables(self):
        self.assertIsInstance(element('simpleline[185,0.1]',), flowables.SimpleLine)
        