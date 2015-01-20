# coding=utf-8

import unittest
from tests.helper import get_initios_logo_path

from reportlab import platypus

from facturapdf import flowables
from facturapdf.generators import element, chapter
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
    def setUp(self):
        self.logo = get_initios_logo_path()

    def test_can_create_frame_breaks(self):
        self.assertIsInstance(element('framebreak'), platypus.doctemplate._FrameBreak)

    def test_can_create_simple_line_flowables(self):
        self.assertIsInstance(element('simpleline[185,0.1]',), flowables.SimpleLine)

    def test_can_create_paragraphs(self):
        self.assertIsInstance(element('paragraph[Paragraph text]'), flowables.Paragraph)

    def test_can_create_images(self):
        self.assertIsInstance(element('image[%s,%s]' % (self.logo, 20)), platypus.Image)

    def test_can_create_spacers(self):
        self.assertIsInstance(element('spacer[0,5]'), platypus.Spacer)


class ChapterTest(unittest.TestCase):
    def test_create_a_list_of_elements(self):
        elements = chapter('framebreak', 'simpleline[185,0.1]', 'framebreak')

        self.assertIsInstance(elements[0], platypus.doctemplate._FrameBreak)
        self.assertIsInstance(elements[1], flowables.SimpleLine)
        self.assertIsInstance(elements[2], platypus.doctemplate._FrameBreak)
