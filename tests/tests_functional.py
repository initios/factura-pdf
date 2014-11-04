import os
import unittest
from facturapdf import InvoiceGenerator, DefaultStrategy
from tests.helper import get_output_folder, get_initios_logo_path
from os.path import isdir, isfile, splitext
from facturapdf.dtos import Customer, Metadata


class TestCase(unittest.TestCase):
    def assertIsFolder(self, folder):
        self.assertTrue(isdir(folder))

    def assertIsFile(self, file):
        self.assertTrue(isfile(file))

    def assertExtension(self, file, ext):
        self.assertTrue(splitext(file)[1] == '.pdf')


# See below the CustomInvoiceGenerator class
class CreateInvoiceTest(TestCase):
    def setUp(self):
        self.file = os.path.join(get_output_folder(), "output.pdf")
        self.invoice_generator = CustomInvoiceGenerator()

    def test_can_create_an_invoice(self):
        customer = Customer(
            code='CUS1', name='Example Customer Name', vat='123456789X',
            address='Long address from our customer', city='Vigo',
            postal_code='309182', province='Pontevedra', country='España',
            contact_name='Customer Name', contact_phone='9876542817', contact_email='mymail@python.com'
        )
        rows = [['Producto de ejemplo %i' % i, i * 10, i * 100, i * 1000] for i in range(0, 27)]
        metadata = Metadata(
            doc_type='FACTURA', code='FRA SER 14-2014', serie='SER', date='01/12/2014'
        )
        subtotal = '5000,00 €'
        footer_a_data = ['475,00 €', 'I.V.A.', '21%', '99,75 €', '574,75 €']
        footer_b_data = ['TRANSFER', 'MY ENTITY', 'ER 19281 12 1234567889', '30 días']

        self.invoice_generator.generate(self.file, rows, customer, metadata, subtotal, footer_a_data, footer_b_data)
        self.assertIsFile(self.file)
        self.assertExtension(self.file, 'pdf')


# Most of the invoice texts are static, only the rows and totals are
# changing from one document to another, so the idea is that you override
# some of the properties of the InvoiceGenerator and use that class
# to create your invoices

# You can also override strategies or templates. They exist to be overrided
# Check the following example that is using the functional test
class CustomInvoiceGenerator(InvoiceGenerator):
    def __init__(self, strategy=None, template=None):
        # Please see that I am using CustomStrategy here
        super().__init__(CustomStrategy(), template)

        self.HEADER_TEXT = 'This is a custom header text for my invoice'
        self.HEADER_LOGO = get_initios_logo_path()


class CustomStrategy(DefaultStrategy):
    def __init__(self):
        super().__init__()

        self.CUSTOMER_SECTION_A_TITLES = ['Customer code', 'Name', 'CIF']
