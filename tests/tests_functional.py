# coding=utf-8
import os
import unittest
from faker import Factory
from facturapdf import InvoiceGenerator, DefaultStrategy
from tests.helper import get_output_folder, get_initios_logo_path
from os.path import isdir, isfile, splitext
from facturapdf.dtos import Customer, Metadata, Data
import locale


locale.setlocale(locale.LC_ALL, '')
fake = Factory.create('es_ES')


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
        self.invoice_generator = InvoiceGenerator()

    def test_can_create_an_invoice_with_multiple_pages(self):
        rows = []
        subtotal = 0

        for i in range(0, 27):
            description = fake.sentence(nb_words=5, variable_nb_words=True)
            unit_price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
            amount = fake.random_int(min=1, max=15)
            unit_total = unit_price * amount

            subtotal += unit_total

            rows.append([description, unit_price, amount, unit_total])

        vat = subtotal * 21 / 100
        total_invoice = subtotal + vat

        data = CustomData()
        data.customer = Customer(
            code='CUS1', name=fake.name(), vat=fake.bothify(text="#########?").upper(),
            address=fake.address(), city=fake.city(),
            postal_code=fake.postcode(), province=fake.state(), country=fake.country(),
            contact_name=fake.name(), contact_phone=fake.phone_number(), contact_email=fake.free_email()
        )
        data.metadata = Metadata(doc_type='FACTURA', code='FRA SER 14-2014', serie='SER', date='01/12/2014')
        data.footer_a = [locale.currency(subtotal), 'I.V.A.', '21%', locale.currency(vat), locale.currency(total_invoice)]
        data.footer_b = ['TRANSFER', 'MY ENTITY', 'ER 19281 12 1234567889', '30 días']
        data.rows = rows
        data.subtotal = subtotal

        destionation_file = os.path.join(get_output_folder(), "mutiple_pages.pdf")

        self.invoice_generator.data = data
        self.invoice_generator.generate(destionation_file)

        self.assertIsFile(destionation_file)


# Most of the invoice texts are static, only the rows and totals are
# changing from one document to another, so the idea is that you override
# some of the properties of the Data class to use your custom text

# You can also override styles, templates, or anything. They exist to be overrided
# Check the following example that is using the functional test

class CustomData(Data):
        CUSTOMER_SECTION_A_TITLES = ['Customer code', 'Name', 'CIF']
        HEADER_TEXT = 'This is a custom header text for my invoice'
        HEADER_LOGO = get_initios_logo_path()

