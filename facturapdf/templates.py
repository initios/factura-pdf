from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate


class DefaultTemplate(object):
    FIRST_PAGE_TEMPLATE_ID = 'fp'
    LATER_PAGES_TEMPLATE_ID = 'sp'

    def create_document(self, destination_file, units):
        margin = 10 * units

        doc = SimpleDocTemplate(destination_file, pagesize=A4, leftMargin=margin, rightMargin=margin,
                                topMargin=margin, bottomMargin=margin, )

        header_left = Frame(margin + 10, 260 * units, 45 * units, 30 * units)
        header_right = Frame(60 * units, 260 * units, 150 * units, 30 * units)
        body = Frame(margin, 45 * units, doc.width, 230 * units)
        footer = Frame(margin, 20 * units, doc.width, 15 * units)

        fp = PageTemplate(id=self.FIRST_PAGE_TEMPLATE_ID, frames=[header_left, header_right, body, footer])
        sp = PageTemplate(id=self.LATER_PAGES_TEMPLATE_ID, frames=[header_left, header_right, body, footer])

        doc.addPageTemplates([fp, sp])

        return doc