from abc import ABCMeta, abstractmethod
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import Table, Paragraph, Spacer, FrameBreak
from facturapdf import SimpleLine
from facturapdf.helper import get_image


class Strategy:
    """
    This class pretends to be an overridable
    strategy generator to create, tables, headers,
    and the differents components of the pdf
    so you can swap easily the stuff you want
    """
    __metaclass__ = ABCMeta

    UNITS = mm

    CUSTOMER_SECTION_A_TITLES = ['Código de cliente', 'Nombre', 'CIF/NIF']
    CUSTOMER_SECTION_B_TITLES = ['Dirección', 'Localidad']
    CUSTOMER_SECTION_C_TITLES = ['Cód. postal', 'Provincia', 'País']
    CUSTOMER_SECTION_D_TITLES = ['Persona de contacto', 'Teléfono', 'E-mail']
    METADATA_TITLES = ['DOCUMENTO', 'CÓDIGO', 'SERIE', 'FECHA', 'PÁGINA']
    TABLE_ROWS_TITLES = ['Descripción', 'Unitario', 'Unidades', 'Total']
    SUBTOTAL_TEXT = 'Subtotal'
    INVOICE_FOOTER_SECTION_A_TITLES = ['Base imponible', 'Impuestos aplicados', '% impuestos', 'Importe impuestos', 'Total factura']
    INVOICE_FOOTER_SECTION_B_TITLES = ['Tipo de pago', 'Entidad', 'Cuenta', 'Vencimiento']

    @abstractmethod
    def create_table(self, data, col_widths='*', row_heights=None, style=None):
        pass

    @abstractmethod
    def create_customer_table(self, customer, style):
        pass

    @abstractmethod
    def create_metadata_table(self, current_page, total_pages, metadata):
        pass

    @abstractmethod
    def create_rows_table(self, rows_data, style, sbutotal, max_items=10, fill_with=[]):
        pass

    @abstractmethod
    def create_invoice_footer(self):
        pass

    @abstractmethod
    def create_header(self, header_logo, header_text, style):
        pass

    @abstractmethod
    def create_footer(self, text, units, style, footer_a_data, footer_b_data):
        pass


class DefaultStrategy(Strategy):
    def create_table(self, data, col_widths='*', row_heights=None, style=None):
        return Table(
            data=data,
            colWidths=col_widths, rowHeights=row_heights,
            style=style or (
                [
                    ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor(0x0096FF)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ]
            )
        )

    def create_customer_table(self, customer, style):
        section_a = self.create_table([
                                          self.CUSTOMER_SECTION_A_TITLES,
                                          [
                                              Paragraph(customer.code, style),
                                              Paragraph(customer.name, style), customer.vat],
                                          ], col_widths=[35 * self.UNITS, 110 * self.UNITS, '*']
        )

        section_b = self.create_table([
                                          self.CUSTOMER_SECTION_B_TITLES,
                                          [Paragraph(customer.address, style),
                                           Paragraph(customer.city, style)]
                                      ], col_widths=[135 * self.UNITS, '*'])

        section_c = self.create_table([
                                          self.CUSTOMER_SECTION_C_TITLES,
                                          [customer.postal_code, Paragraph(customer.province, style),
                                           Paragraph(customer.country, style)]
                                      ], col_widths=[25 * self.UNITS, '*', '*'])

        section_d = self.create_table([
            self.CUSTOMER_SECTION_D_TITLES,
            [Paragraph(customer.contact_name, style), Paragraph(customer.contact_phone, style),
             Paragraph(customer.contact_name, style)]
        ])

        return [section_a] + [section_b] + [section_c] + \
               [Spacer(0, 5 * self.UNITS)] + [section_d] + [Spacer(0, 5 * self.UNITS)]

    def create_metadata_table(self, current_page, total_pages, metadata):
        return [
            self.create_table([
                self.METADATA_TITLES,
                metadata.as_list() + ['%i de %i' % (current_page, total_pages,)]],
                col_widths=['*', '*', '*', 25 * self.UNITS, 20 * self.UNITS],
                ), Spacer(0 * self.UNITS, 5 * self.UNITS)
        ]

    def create_rows_table(self, rows_data, style, subtotal, max_items=10, fill_with=[], show_subtotal=False):
        for row in rows_data:
            row[0] = Paragraph(row[0], style)

        # Fill rows with the fill_with if applies
        while len(rows_data) < max_items:
            rows_data.append(fill_with)

        rows_data.insert(0, self.TABLE_ROWS_TITLES)

        if show_subtotal:
            # todo Remove hardcoded value!
            rows_data.append(['', '', self.SUBTOTAL_TEXT, subtotal])
            table_style = [
                ('TEXTCOLOR', (2, -1), (-2, -1), colors.white),
                ('BACKGROUND', (2, -1), (-2, -1), HexColor(0x0096FF)),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('GRID', (2, -1), (-1, -1), 0.6, colors.black),
            ]
            box_limit = -2
        else:
            table_style = []
            box_limit = -1

        table_style.extend([
            ('GRID', (0, 0), (-1, 0), 0.6, colors.black),
            ('BOX', (0, 1), (-1, box_limit), 0.6, colors.black),
            # Titles
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(0x0096FF)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            # Alinear precios a la derecha
            ('ALIGN', (1, 1), (-1, -2), 'RIGHT'),
            ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),

        ])

        return self.create_table(
            rows_data, col_widths=[110 * self.UNITS, '*', '*', '*',], style=table_style
        )

    def create_invoice_footer(self, footer_a_data, footer_b_data):
        # todo Remove hardcoded data
        invoice_footer_a = self.create_table([self.INVOICE_FOOTER_SECTION_A_TITLES, footer_a_data])

        invoice_footer_b = self.create_table([self.INVOICE_FOOTER_SECTION_B_TITLES, footer_b_data])

        return [Spacer(0, 5 * self.UNITS)] + [invoice_footer_a] + [Spacer(0, 5 * self.UNITS)] \
                         + [invoice_footer_b] + [Spacer(0, 5 * self.UNITS)]

    def create_header(self, header_logo, header_text, style):
        return [
            get_image(header_logo, 40 * self.UNITS),
            FrameBreak(),
            Paragraph(header_text, style),
            FrameBreak(),
            Spacer(0, 5 * self.UNITS),
        ]

    def create_footer(self, text, units, style):
        return [
            FrameBreak(),
            SimpleLine(185 * units, 0.1 * units),
            Paragraph(text, style)
        ]