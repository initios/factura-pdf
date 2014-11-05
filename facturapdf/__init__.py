from reportlab.platypus import NextPageTemplate, PageBreak
from facturapdf.helper import chunks
from facturapdf.styles import DefaultStyling
from facturapdf.templates import DefaultTemplate
from .flowables import SimpleLine
from .strategies import DefaultStrategy
from .dtos import Customer


class InvoiceGenerator(object):
    HEADER_LOGO = None
    HEADER_TEXT = 'Calle de la empresa 2, bajo - oficina 3'

    MAX_ROWS_PER_TABLE = 20
    FILL_ROWS_WITH = []

    def __init__(self, strategy=None, template=None):
        self.strategy = strategy or DefaultStrategy()
        self.template = template or DefaultTemplate()

    def generate(self, destination_file, rows, customer, metadata, subtotal, footer_a_data, footer_b_data):
        doc = self.template.create_document(destination_file)

        # Generation of shared flowables
        header = self.strategy.create_header(self.HEADER_LOGO, self.HEADER_TEXT)
        customer_section = self.strategy.create_customer_table(customer)
        invoice_footer = self.strategy.create_invoice_footer(footer_a_data, footer_b_data)
        footer = self.strategy.create_footer('Footer text with company legal information', self.template.UNITS)

        story = [
            NextPageTemplate(DefaultTemplate.FIRST_PAGE_TEMPLATE_ID)
        ]

        rows_chunks = chunks(rows, self.MAX_ROWS_PER_TABLE, self.FILL_ROWS_WITH)

        for counter, row_chunk in enumerate(rows_chunks):
            is_first_page = counter == 0
            is_last_page = len(rows_chunks) == counter+1

            story.extend(header)
            story.extend(self.strategy.create_metadata_table(counter + 1, len(rows_chunks), metadata))

            if is_first_page:
                story.extend(customer_section)

            story.append(
                self.strategy.create_rows_table(row_chunk, subtotal, is_last_page))

            if is_last_page:
                story.extend(invoice_footer)

            story.extend(footer)
            story.append(NextPageTemplate(DefaultTemplate.LATER_PAGES_TEMPLATE_ID))

            if not is_last_page:
                story.append(PageBreak())

        doc.build(flowables=story)