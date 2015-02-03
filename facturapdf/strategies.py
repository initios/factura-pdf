# coding=utf-8
from reportlab.lib.units import mm
from reportlab.platypus import Table, Spacer

from facturapdf import DefaultStyling, generators
from facturapdf.flowables import Paragraph


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
        return Table(data=data, colWidths=col_widths or '*', rowHeights=row_heights,
                     style=style or self.styling.table)

    def _create_customer_section_a_table(self, data, col_widths=None, row_heights=None, style=None,
                                         paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        return self.create_table([
                data.CUSTOMER_SECTION_A_TITLES,
                [Paragraph(data.customer.code), Paragraph(data.customer.name), data.customer.vat],
            ],
            col_widths=col_widths or [35 * self.UNITS, 110 * self.UNITS, '*'],
            row_heights=row_heights, style=style
        )

    def _create_customer_section_b_table(self, data, col_widths=None, row_heights=None, style=None,
                                             paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        return self.create_table([
                data.CUSTOMER_SECTION_B_TITLES,
                [Paragraph(data.customer.address), Paragraph(data.customer.city)]
            ],
            col_widths=col_widths or [135 * self.UNITS, '*'],
            row_heights=row_heights, style=style
        )

    def _create_customer_section_c_table(self, data, col_widths=None, row_heights=None, style=None,
                                         paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        return self.create_table([
                data.CUSTOMER_SECTION_C_TITLES,
                [data.customer.postal_code, Paragraph(data.customer.province), Paragraph(data.customer.country)]
            ], col_widths=col_widths or [25 * self.UNITS, '*', '*'],
            row_heights=row_heights, style=style
        )

    def _create_customer_section_d_table(self, data, col_widths=None, row_heights=None, style=None,
                                         paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        return self.create_table([
                data.CUSTOMER_SECTION_D_TITLES,
                [Paragraph(data.customer.contact_name), Paragraph(data.customer.contact_phone),
                Paragraph(data.customer.contact_email)],
            ], col_widths=col_widths or '*',
            row_heights=row_heights, style=style
        )

    def create_customer_table(self, data):
        section_a = self._create_customer_section_a_table(data)
        section_b = self._create_customer_section_b_table(data)
        section_c = self._create_customer_section_c_table(data)
        section_d = self._create_customer_section_d_table(data)

        return [section_a]+[section_b]+[section_c]+[Spacer(0, 5 * self.UNITS)]+[section_d]+[Spacer(0, 5 * self.UNITS)]

    def create_metadata_table(self, current_page, total_pages, data, col_widths=None, row_heights=None, style=None,
                              paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        return [
            self.create_table(
                [data.METADATA_TITLES, data.metadata.as_list() + ['%i de %i' % (current_page, total_pages)]],
                col_widths=col_widths or ['*', '*', '*', 25 * self.UNITS, 20 * self.UNITS],
                row_heights=row_heights, style=style,
            ), Spacer(0 * self.UNITS, 5 * self.UNITS)
        ]

    def _rows_with_subtotal_table(self, data, col_widths=None, row_heights=None, style=None, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text
        return self.create_table(data, col_widths=col_widths or [110 * self.UNITS, '*', '*', '*', ],
                                 row_heights=row_heights, style=style or self.styling.table_rows_with_subtotal)

    def _rows_without_subtotal_table(self, data, col_widths=None, row_heights=None, style=None, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text
        return self.create_table(data, col_widths=col_widths or [110 * self.UNITS, '*', '*', '*', ],
                                 row_heights=row_heights, style=style or self.styling.table_rows_without_subtotal)

    def create_rows_table(self, rows_data, data, show_subtotal=False, col_widths=None, row_heights=None, style=None,
                          subtotal_style=None, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        for row in rows_data:
            try:
                # If an empty row is given to fill the table an exception is raised
                row[0] = Paragraph(row[0])
            except IndexError:
                pass

        rows_data.insert(0, data.TABLE_ROWS_TITLES)

        if show_subtotal:
            rows_data.append(['', '', data.SUBTOTAL_TEXT, data.metadata.subtotal])
            return self._rows_with_subtotal_table(rows_data)

        return self._rows_without_subtotal_table(rows_data)

    def create_invoice_footer(self, data, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text

        invoice_footer_a = self.create_table([data.INVOICE_FOOTER_SECTION_A_TITLES, data.footer_a])
        invoice_footer_b = self.create_table([data.INVOICE_FOOTER_SECTION_B_TITLES, data.footer_b])

        return generators.chapter('spacer[0|14]', invoice_footer_a, 'spacer[0|14]', invoice_footer_b, 'spacer[0|14]')

    def create_header(self, data, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text
        return generators.chapter('image[%s|113.38]' % data.HEADER_LOGO, 'framebreak',
                                  'paragraph[%s]' % data.HEADER_TEXT, 'framebreak', 'spacer[0|14.17]')

    def create_footer(self, data, paragraph_style=None):
        Paragraph.next_style = paragraph_style or self.styling.invoice_text
        return generators.chapter('framebreak', 'simpleline[524|0.28]', 'paragraph[%s]' % data.FOOTER_TEXT)
