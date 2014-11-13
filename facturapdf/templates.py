from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate


class DefaultTemplate:
    FIRST_PAGE_TEMPLATE_ID = 'fp'
    LATER_PAGES_TEMPLATE_ID = 'sp'

    def create_document(self, destination_file, units):
        margin = 10 * units

        doc = SimpleDocTemplate(destination_file, pagesize=A4, leftMargin=margin, rightMargin=margin,
                                 topMargin=margin, bottomMargin=margin, )

        # First page
        fp_header_left = Frame(doc.leftMargin + 10 * units, 260 * units, 30 * units, 30 * units)
        fp_header_right = Frame(doc.leftMargin + 50 * units, 260 * units, 100 * units, 30 * units)
        fp_body = Frame(doc.leftMargin, 45 * units, doc.width, 230 * units)
        fp_footer = Frame(doc.leftMargin, 20 * units, doc.width, 15 * units)
        fp = PageTemplate(id=self.FIRST_PAGE_TEMPLATE_ID, frames=[fp_header_left, fp_header_right, fp_body, fp_footer])

        # Second page
        sp_header_left = Frame(doc.leftMargin + 10 * units, 260 * units, 30 * units, 30 * units)
        sp_header_right = Frame(doc.leftMargin + 50 * units, 260 * units, 100 * units, 30 * units)
        sp_body = Frame(doc.leftMargin, 45 * units, doc.width, 230 * units)
        sp_footer = Frame(doc.leftMargin, 20 * units, doc.width, 15 * units)

        sp = PageTemplate(id=self.LATER_PAGES_TEMPLATE_ID, frames=[sp_header_left, sp_header_right, sp_body, sp_footer])

        doc.addPageTemplates([fp, sp])

        return doc