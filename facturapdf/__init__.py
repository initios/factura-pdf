from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import NextPageTemplate, Paragraph, FrameBreak, PageBreak
from facturapdf.helper import chunks
from facturapdf.templates import DefaultTemplate, Template
from .flowables import SimpleLine
from .strategies import DefaultStrategy
from .dtos import Customer


class InvoiceGenerator:
    styles = getSampleStyleSheet()

    def __init__(self, strategy=None, template=None):
        self.invoice_text_style = self.styles.get('Normal')
        self.strategy = strategy or DefaultStrategy()
        self.template = template or DefaultTemplate()

    def generate(self, destination_file, header_logo, rows, customer, metadata, header_text):
        doc = self.template.create_document(destination_file)

        # Generation of shared flowables
        header = self.strategy.create_header(header_logo, header_text, self.invoice_text_style)
        customer_section = self.strategy.create_customer_table(customer, self.invoice_text_style)
        invoice_footer = self.strategy.create_invoice_footer()
        footer = self.strategy.create_footer('Footer text with company legal information',
                                             self.template.UNITS, self.invoice_text_style)

        story = [
            NextPageTemplate(Template.FIRST_PAGE_TEMPLATE_ID)
        ]

        rows_chunks = chunks(rows, 10)

        for counter, row_chunk in enumerate(rows_chunks):
            is_first_page = counter == 0
            is_last_page = len(rows_chunks) == counter+1

            story.extend(header)
            story.extend(self.strategy.create_metadata_table(counter + 1, len(rows_chunks), metadata))

            if is_first_page:
                story.extend(customer_section)

            story.append(
                self.strategy.create_rows_table(row_chunk, self.invoice_text_style, show_subtotal=is_last_page))

            if is_last_page:
                story.extend(invoice_footer)

            story.extend(footer)
            story.append(NextPageTemplate(Template.LATER_PAGES_TEMPLATE_ID))

            if not is_last_page:
                story.append(PageBreak())

        doc.build(flowables=story)