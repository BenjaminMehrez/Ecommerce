from django.forms import ModelForm
from django import forms
from .models import Address


class AddressForm(ModelForm):
    
    class Meta:
        model = Address
        fields = ['full_name', 'email', 'address', 'street', 'zipcode', 'city', 'mobile', 'status']
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Lionel Messi'}),
            'email': forms.EmailInput(attrs={'placeholder': 'lionelmessi@gmail.com'}),
            'address': forms.Textarea(attrs={'rows': '1', 'placeholder': 'Barrio Champions, Rosario'}),
            'street': forms.TextInput(attrs={'placeholder': '9 de julio 231'}),
            'zipcode': forms.TextInput(attrs={'placeholder': '4122'}),
            'city': forms.TextInput(attrs={'placeholder': 'Santa Fe'}),
            'mobile': forms.TextInput(attrs={'placeholder': '+54 3193214'}),
            'status': forms.CheckboxInput(),
        }
        labels = {
            'full_name': 'Nombre completo',
            'email': 'Correo Electrónico',
            'address': 'Dirección',
            'street': 'Calle y número',
            'zipcode': 'Condigo Postal',
            'city': 'Provincia',
            'mobile': 'Celular',
            'status': 'Estado',
            
        }