# coding=utf-8
from reportlab.lib.units import mm
from reportlab.platypus import Table, Spacer, FrameBreak

from facturapdf import SimpleLine, DefaultStyling, generators
from facturapdf.flowables import Paragraph
from facturapdf.helper import get_image


class DefaultStrategy(object):
    """
    This class pretends to be an overridable
    strategy generator to create, tables, headers,
    and the differents components of the pdf
    so you can swap easily the stuff you want
    """

    def __init__(self, styling=None):
        self.styling = styling or DefaultStyling()

    UNITS = mm
    MAX_ROWS_PER_TABLE = 20
    FILL_ROWS_WITH = []

    def create_table(self, data, col_widths='*', row_heights=None, style=None):
        style = style or self.styling.table

        return Table(
            data=data,
            colWidths=col_widths, rowHeights=row_heights,
            style=style
        )

    def create_customer_table(self, data):
        Paragraph.next_style = self.styling.invoice_text

        section_a = self.create_table(
            [
                data.CUSTOMER_SECTION_A_TITLES,
                [
                    Paragraph(data.customer.code),
                    Paragraph(data.customer.name), data.customer.vat],
            ],
            col_widths=[35 * self.UNITS, 110 * self.UNITS, '*'
            ]
        )

        section_b = self.create_table(
            [
                data.CUSTOMER_SECTION_B_TITLES,
                [Paragraph(data.customer.address),
                 Paragraph(data.customer.city)]
            ], col_widths=[135 * self.UNITS, '*'])

        section_c = self.create_table(
            [
                data.CUSTOMER_SECTION_C_TITLES,
                [
                    data.customer.postal_code, Paragraph(data.customer.province),
                    Paragraph(data.customer.country)]
            ], col_widths=[25 * self.UNITS, '*', '*'
            ]
        )

        section_d = self.create_table([
            data.CUSTOMER_SECTION_D_TITLES,
            [Paragraph(data.customer.contact_name),
             Paragraph(data.customer.contact_phone),
             Paragraph(data.customer.contact_email)]
        ])

        return [section_a] + [section_b] + [section_c] + \
               [Spacer(0, 5 * self.UNITS)] + [section_d] + [Spacer(0, 5 * self.UNITS)]

    def create_metadata_table(self, current_page, total_pages, data):
        Paragraph.next_style = self.styling.invoice_text

        return [
            self.create_table([
                data.METADATA_TITLES,
                data.metadata.as_list() + ['%i de %i' % (current_page, total_pages,)]],
                col_widths=['*', '*', '*', 25 * self.UNITS, 20 * self.UNITS],
            ), Spacer(0 * self.UNITS, 5 * self.UNITS)
        ]

    def create_rows_table(self, rows_data, data, show_subtotal=False):
        Paragraph.next_style = self.styling.invoice_text

        for row in rows_data:
            # If an empty row is given to fill the table an exception is raised
            try:
                row[0] = Paragraph(row[0])
            except:
                pass

        rows_data.insert(0, data.TABLE_ROWS_TITLES)

        if show_subtotal:
            rows_data.append(['', '', data.SUBTOTAL_TEXT, data.metadata.subtotal])
            table_style = self.styling.table_rows_with_subtotal
        else:
            table_style = self.styling.table_rows_without_subtotal

        return self.create_table(rows_data, col_widths=[110 * self.UNITS, '*', '*', '*', ], style=table_style)

    def create_invoice_footer(self, data):
        Paragraph.next_style = self.styling.invoice_text

        invoice_footer_a = self.create_table([data.INVOICE_FOOTER_SECTION_A_TITLES, data.footer_a])
        invoice_footer_b = self.create_table([data.INVOICE_FOOTER_SECTION_B_TITLES, data.footer_b])

        return [Spacer(0, 5 * self.UNITS)] + [invoice_footer_a] + [Spacer(0, 5 * self.UNITS)] \
            + [invoice_footer_b] + [Spacer(0, 5 * self.UNITS)]

    def create_header(self, data):
        Paragraph.next_style = self.styling.invoice_text

        return [
            get_image(data.HEADER_LOGO, 40 * self.UNITS),
            FrameBreak(),
            Paragraph(data.HEADER_TEXT),
            FrameBreak(),
            Spacer(0, 5 * self.UNITS),
        ]

    def create_footer(self, data):
        Paragraph.next_style = self.styling.invoice_text
        return generators.chapter('framebreak', 'simpleline[524,0.28]', 'paragraph[%s]' % data.FOOTER_TEXT)
