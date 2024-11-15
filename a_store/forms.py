from django.forms import ModelForm
from django import forms
from .models import *


# class AddressForm(ModelForm):
    
#     class Meta:
#         model = Address
#         fields = ['full_name', 'email', 'address', 'street', 'zipcode', 'city', 'mobile', 'status']
#         exclude = ['user']
#         widgets = {
#             'full_name': forms.TextInput(attrs={'placeholder': 'Lionel Messi'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'lionelmessi@gmail.com'}),
#             'address': forms.Textarea(attrs={'rows': '1', 'placeholder': 'Barrio Champions, Rosario'}),
#             'street': forms.TextInput(attrs={'placeholder': '9 de julio 231'}),
#             'zipcode': forms.TextInput(attrs={'placeholder': '4122'}),
#             'city': forms.TextInput(attrs={'placeholder': 'Santa Fe'}),
#             'mobile': forms.TextInput(attrs={'placeholder': '+54 3193214'}),
#             'status': forms.CheckboxInput(),
#         }
#         labels = {
#             'full_name': 'Nombre completo',
#             'email': 'Correo Electrónico',
#             'address': 'Dirección',
#             'street': 'Calle y número',
#             'zipcode': 'Condigo Postal',
#             'city': 'Provincia',
#             'mobile': 'Celular',
#             'status': 'Estado',
            
#         }
        
        
class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Agrega un comentario...',
            'class': 'w-full p-3 bg-gray-50 border border-gray-300 rounded-md text-gray-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none',
            'rows': 4
        }),
        label=''
    )
    
    rating = forms.ChoiceField(
        choices=[(str(i), f"{i} estrellas") for i in range(1, 6)],
        widget=forms.Select(attrs={
            'class': 'w-full md:w-auto p-2 bg-gray-50 border border-gray-300 rounded-md text-gray-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
        }),
        label='Calificación'
    )

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']