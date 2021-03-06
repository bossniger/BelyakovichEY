from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from apps.common.models import Clients
from apps.orders.models import Order
from apps.shop.models import Product
from apps.userprofile.models import Profile


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'birth_date',
            'profile_image'
        ]


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'price', 'stock', 'available', )
        readonly_fields = ['created']


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'price', 'stock', 'available',)
        readonly_fields = ['created']


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'supply', 'supplier', 'name', 'description', 'price', 'stock', 'available',)


class ClientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'amount_orders', 'orders_cost', 'city')


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        readonly_field = ['first_name', 'last_name', 'email']
