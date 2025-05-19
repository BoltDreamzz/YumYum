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


# forms.py

from django import forms
from .models import Review, ReviewReply

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control review-input',
                'rows': 4,
                'placeholder': 'Share your experience...',
            }),
                'rating': forms.RadioSelect(choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)]),

        }

class ReviewReplyForm(forms.ModelForm):
    class Meta:
        model = ReviewReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control reply-input',
                'rows': 2,
                'placeholder': 'Write your reply...',
            })
        }