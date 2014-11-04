import os
import unittest
from facturapdf import InvoiceGenerator
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


class CreateInvoiceTest(TestCase):
    def setUp(self):
        self.file = os.path.join(get_output_folder(), "output.pdf")
        self.initios_logo = get_initios_logo_path()
        self.invoice_generator = InvoiceGenerator()

    def test_can_create_a_invoice(self):
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
        header_text = 'Calle de la empresa 2, bajo - oficina 3'

        self.invoice_generator.generate(self.file, self.initios_logo, rows, customer, metadata, header_text)
        self.assertIsFile(self.file)
        self.assertExtension(self.file, 'pdf')