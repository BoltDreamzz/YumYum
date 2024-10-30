# shop/forms.py
from django import forms
from .models import DeliveryAddress

class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1, widget=forms.NumberInput(attrs={'class': 'quantity-input'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CheckoutForm(forms.Form):
    payment_reference = forms.CharField(label='Payment Reference', max_length=100, required=True)
    payment_screenshot = forms.ImageField(label='Proof of Payment', required=False)


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'phone_number', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
