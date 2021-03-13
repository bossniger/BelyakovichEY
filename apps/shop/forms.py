from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ('name', 'agent', 'address', 'city', 'country', 'phone',)