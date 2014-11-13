# coding=utf-8
from reportlab.lib.units import mm
from reportlab.platypus import Table, Paragraph, Spacer, FrameBreak
from facturapdf import SimpleLine, DefaultStyling
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
        section_a = self.create_table(
            [
                data.CUSTOMER_SECTION_A_TITLES,
                [
                    Paragraph(data.customer.code, self.styling.invoice_text),
                    Paragraph(data.customer.name, self.styling.invoice_text), data.customer.vat],
            ],
            col_widths=[35 * self.UNITS, 110 * self.UNITS, '*'
            ]
        )

        section_b = self.create_table(
            [
                data.CUSTOMER_SECTION_B_TITLES,
                [Paragraph(data.customer.address, self.styling.invoice_text),
                 Paragraph(data.customer.city, self.styling.invoice_text)]
            ], col_widths=[135 * self.UNITS, '*'])

        section_c = self.create_table(
            [
                data.CUSTOMER_SECTION_C_TITLES,
                [
                    data.customer.postal_code, Paragraph(data.customer.province, self.styling.invoice_text),
                    Paragraph(data.customer.country, self.styling.invoice_text)]
            ], col_widths=[25 * self.UNITS, '*', '*'
            ]
        )

        section_d = self.create_table([
            data.CUSTOMER_SECTION_D_TITLES,
            [Paragraph(data.customer.contact_name, self.styling.invoice_text),
             Paragraph(data.customer.contact_phone, self.styling.invoice_text),
             Paragraph(data.customer.contact_email, self.styling.invoice_text)]
        ])

        return [section_a] + [section_b] + [section_c] + \
               [Spacer(0, 5 * self.UNITS)] + [section_d] + [Spacer(0, 5 * self.UNITS)]

    def create_metadata_table(self, current_page, total_pages, data):
        return [
            self.create_table([
                                  data.METADATA_TITLES,
                                  data.metadata.as_list() + ['%i de %i' % (current_page, total_pages,)]],
                              col_widths=['*', '*', '*', 25 * self.UNITS, 20 * self.UNITS],
            ), Spacer(0 * self.UNITS, 5 * self.UNITS)
        ]

    def create_rows_table(self, rows_data, data, show_subtotal=False):
        for row in rows_data:
            # If an empty row is given to fill the table an exception is raised
            try:
                row[0] = Paragraph(row[0], self.styling.invoice_text)
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
        invoice_footer_a = self.create_table([data.INVOICE_FOOTER_SECTION_A_TITLES, data.footer_a])
        invoice_footer_b = self.create_table([data.INVOICE_FOOTER_SECTION_B_TITLES, data.footer_b])

        return [Spacer(0, 5 * self.UNITS)] + [invoice_footer_a] + [Spacer(0, 5 * self.UNITS)] \
               + [invoice_footer_b] + [Spacer(0, 5 * self.UNITS)]

    def create_header(self, data):
        return [
            get_image(data.HEADER_LOGO, 40 * self.UNITS),
            FrameBreak(),
            Paragraph(data.HEADER_TEXT, self.styling.invoice_text),
            FrameBreak(),
            Spacer(0, 5 * self.UNITS),
        ]

    def create_footer(self, data):
        return [
            FrameBreak(),
            SimpleLine(185 * self.UNITS, 0.1 * self.UNITS),
            Paragraph(data.FOOTER_TEXT, self.styling.invoice_text)
        ]