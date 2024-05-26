from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='',
                                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                                         required=True)
    shipping_email = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                                     required=True)
    shipping_phone_number = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone'}),
                                            required=True)
    shipping_address_1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address'}),
                                         required=True)
    shipping_address_2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address'}),
                                         required=False)
    shipping_city = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                                    required=True)
    shipping_postal_code = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
                                           required=True)
    shipping_country = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Country'}),
                                       required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_phone_number', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'shipping_postal_code', 'shipping_country']
        exclude = ['user']
