from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'phone']
        widgets = {
            'image': forms.FileInput(),
            'full_name' : forms.TextInput(attrs={'placeholder': 'Nombre  Completo'}),
            'phone' : forms.TextInput(attrs={'placeholder': 'Numero de Telefono'}),
        }
        labels = {
            'image': '',
            'full_name': '',
            'phone': '',
        }
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']