from abc import ABCMeta, abstractmethod
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate


class Template:
    UNITS = None
    MARGIN = None

    FIRST_PAGE_TEMPLATE_ID = 'fp'
    LATER_PAGES_TEMPLATE_ID = 'sp'

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_document(self, destination_file):
        pass


class DefaultTemplate(Template):
    def __init__(self):
        self.UNITS = mm
        self.MARGIN = 10 * self.UNITS

    def create_document(self, destination_file):
        doc = SimpleDocTemplate(destination_file, pagesize=A4, leftMargin=self.MARGIN, rightMargin=self.MARGIN,
                                 topMargin=self.MARGIN, bottomMargin=self.MARGIN, )

        # First page
        fp_header_left = Frame(doc.leftMargin + 10 * self.UNITS, 260 * self.UNITS, 30 * self.UNITS, 30 * self.UNITS)
        fp_header_right = Frame(doc.leftMargin + 50 * self.UNITS, 260 * self.UNITS, 100 * self.UNITS, 30 * self.UNITS)
        fp_body = Frame(doc.leftMargin, 45 * self.UNITS, doc.width, 230 * self.UNITS)
        fp_footer = Frame(doc.leftMargin, 20 * self.UNITS, doc.width, 15 * self.UNITS)
        fp = PageTemplate(id=self.FIRST_PAGE_TEMPLATE_ID, frames=[fp_header_left, fp_header_right, fp_body, fp_footer])

        # Second page
        sp_header_left = Frame(doc.leftMargin + 10 * self.UNITS, 260 * self.UNITS, 30 * self.UNITS, 30 * self.UNITS)
        sp_header_right = Frame(doc.leftMargin + 50 * self.UNITS, 260 * self.UNITS, 100 * self.UNITS, 30 * self.UNITS)
        sp_body = Frame(doc.leftMargin, 45 * self.UNITS, doc.width, 230 * self.UNITS)
        sp_footer = Frame(doc.leftMargin, 20 * self.UNITS, doc.width, 15 * self.UNITS)

        sp = PageTemplate(id=self.LATER_PAGES_TEMPLATE_ID, frames=[sp_header_left, sp_header_right, sp_body, sp_footer])

        doc.addPageTemplates([fp, sp])

        return doc