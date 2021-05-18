from django.test import TestCase, RequestFactory
from .models import Supplier


class SupplierModelTest(TestCase):

    def setUp(self):
        Supplier.objects.create(id=2, name='name2', agent='agent2', address='address2', city='city2', country='country2',
                                phone='phone1')

    def test_name_label(self):
        supplier = Supplier.objects.get(id=2)
        assert supplier is not None
