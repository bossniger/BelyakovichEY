from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from ..orders.models import Order
from .views import client_profile as client_profile_view
from ..shop.forms import SupplierForm


class TestClientProfile(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        Order.objects.create(
                pk=1,
                first_name='fname',
                last_name='lname',
                email='test@mail.com',
            )

    def test__client_profile_get_order(self):
        order = Order.objects.get(pk=1)
        assert order.pk == 1
        assert order.first_name == 'fname'
        assert order.last_name == 'lname'
        assert order.email == 'test@mail.com'

    def test__client_profile_get_response_status_code(self):
        # request = self.factory.get('clientprofile//1/')
        # request.user = AnonymousUser()
        # response = client_profile_view(request, client_id=1)

        response = self.client.get('/clientprofile/1/', client_id=1)
        self.assertEqual(response.status_code, 200)


class TestUserRegister(TestCase):
    def test_user_register(self):
        data = {
            'username': 'admin',
            'first_name': 'Egor',
            'last_name': 'Belyakovich',
            'email': 'shef228@mail.ru',
            'password1': 'admin',
            'password2': 'admin',
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, 200)


class TestSupplierAddForm(TestCase):
    def test_supplier_add_form(self):
        data={
            'name':'testname',
               'agent':'testagent',
            'address':'testaddress',
            'city': 'testcity',
            'country': 'testcountry',
            'phone': 'testphone',
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())
