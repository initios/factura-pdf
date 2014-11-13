# coding=utf-8
class Data(object):
    HEADER_LOGO = None
    HEADER_TEXT = 'Calle de la empresa 2, bajo - oficina 3'
    FOOTER_TEXT = 'Footer text with company legal information'
    CUSTOMER_SECTION_A_TITLES = ['Código de cliente', 'Nombre', 'CIF/NIF']
    CUSTOMER_SECTION_B_TITLES = ['Dirección', 'Localidad']
    CUSTOMER_SECTION_C_TITLES = ['Cód. postal', 'Provincia', 'País']
    CUSTOMER_SECTION_D_TITLES = ['Persona de contacto', 'Teléfono', 'E-mail']
    METADATA_TITLES = ['DOCUMENTO', 'CÓDIGO', 'SERIE', 'FECHA', 'PÁGINA']
    TABLE_ROWS_TITLES = ['Descripción', 'Unitario', 'Unidades', 'Total']
    SUBTOTAL_TEXT = 'Subtotal'
    INVOICE_FOOTER_SECTION_A_TITLES = ['Base imponible', 'Impuestos aplicados', '% impuestos',
                                       'Importe impuestos', 'Total factura']
    INVOICE_FOOTER_SECTION_B_TITLES = ['Tipo de pago', 'Entidad', 'Cuenta', 'Vencimiento']

    customer = None
    metadata = None
    footer_a = None
    footer_b = None
    rows = None


class Customer(object):
    def __init__(self, **kwargs):
        self.code = kwargs.get('code', None)
        self.name = kwargs.get('name', None)
        self.vat = kwargs.get('vat', None)
        self.address = kwargs.get('address', None)
        self.city = kwargs.get('city', None)
        self.postal_code = kwargs.get('postal_code', None)
        self.province = kwargs.get('province', None)
        self.country = kwargs.get('country', None)
        self.contact_name = kwargs.get('contact_name', None)
        self.contact_phone = kwargs.get('contact_phone', None)
        self.contact_email = kwargs.get('contact_email', None)


class Metadata(object):
    def __init__(self, **kwargs):
        self.doc_type = kwargs.get('doc_type', None)
        self.code = kwargs.get('code', None)
        self.serie = kwargs.get('serie', None)
        self.date = kwargs.get('date', None)
        self.subtotal = kwargs.get('subtotal', 0)

    def as_list(self):
        return [self.doc_type, self.code, self.serie, self.date]