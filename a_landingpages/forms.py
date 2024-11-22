from django import forms


class AccessForm(forms.Form):
    password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa el codigo'}),
        label=False
    )