from django import forms
from .models import Delivery

class CourierServiceForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            'pickup_name', 'pickup_location', 'pickup_number', 
            'dropoff_location', 'dropoff_name', 'dropoff_number', 
            'items_worth', 'item_parcel_name', 'delivery_type', 'weight'
        ]
        widgets = {
            'pickup_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter pickup name'
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter pickup address'
            }),
            'pickup_number': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter pickup phone number'
            }),
            'dropoff_location': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter drop-off address'
            }),
            'dropoff_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter dropoff name'
            }),
            'dropoff_number': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter dropoff phone number'
            }),
            'items_worth': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter item worth in Naira'
            }),
            'item_parcel_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter parcel name'
            }),
            'delivery_type': forms.RadioSelect(attrs={'class': 'peer'}),
        }
        help_texts = {
            'pickup_name': 'Full name of the person at the pickup location.',
            'pickup_location': 'Complete address where the parcel will be picked up.',
            'pickup_number': 'Phone number for contact at the pickup location.',
            'dropoff_location': 'Complete address where the parcel will be delivered.',
            'dropoff_name': 'Full name of the person receiving the parcel at the dropoff location.',
            'dropoff_number': 'Phone number for contact at the dropoff location.',
            'items_worth': 'Estimated worth of the items in Naira.',
            'item_parcel_name': 'Brief name or description of the item(s) being delivered.',
            'delivery_type': 'Choose the preferred delivery type for this service.',
        }

class ShippingCalculatorForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['items_worth', 'weight', 'delivery_type']
        
        widgets = {
            'items_worth': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter item worth in Naira'
            }),
            'weight': forms.TextInput(attrs={
                'class': 'input input-bordered w-full p-4 rounded-4 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter weight in Kg'
            }),
            'delivery_type': forms.RadioSelect(attrs={'class': 'peer'}),
        }