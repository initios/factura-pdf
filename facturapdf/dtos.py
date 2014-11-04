class Customer:
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


class Metadata:
    def __init__(self, **kwargs):
        self.doc_type = kwargs.get('doc_type', None)
        self.code = kwargs.get('code', None)
        self.serie = kwargs.get('serie', None)
        self.date = kwargs.get('date', None)

    def as_list(self):
        return [self.doc_type, self.code, self.serie, self.date]