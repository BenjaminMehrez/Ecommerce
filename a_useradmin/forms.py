from django import forms
from a_store.models import *

class AddProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = Product
        fields = [
            'title',
            'image',  # Imagen principal
            'description',
            'category',
            'price',
            'old_price',
            'specifications',
            'featured',
            'tags',
            'vendor',
            'product_status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Default styling for most fields
        default_class = "w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500"
        
        # Apply default styling to most fields
        for field_name, field in self.fields.items():
            if field_name not in ['featured', 'image']:
                field.widget.attrs.update({'class': default_class})

        # Custom styling for specific fields
        self.fields['title'].widget.attrs.update({
            'class': default_class + " font-semibold",
            'placeholder': 'Enter product title'
        })

        self.fields['description'].widget.attrs.update({
            'class': default_class + " h-32",
            'placeholder': 'Enter product description'
        })

        self.fields['image'].widget.attrs.update({
            'class': "w-full text-gray-700 px-3 py-2 rounded-lg focus:outline-none",
        })

        self.fields['price'].widget.attrs.update({
            'class': default_class,
            'placeholder': 'Enter price'
        })

        self.fields['old_price'].widget.attrs.update({
            'class': default_class,
            'placeholder': 'Enter old price (optional)'
        })

        self.fields['specifications'].widget.attrs.update({
            'class': default_class + " h-32",
            'placeholder': 'Enter product specifications'
        })

        self.fields['featured'].widget.attrs.update({
            'class': "form-checkbox h-5 w-5 text-blue-600",
        })

        self.fields['tags'].widget.attrs.update({
            'class': default_class,
            'placeholder': 'Enter tags (comma-separated)'
        })

        # Assuming category, vendor, and product_status are choice fields or foreign keys
        select_class = default_class + " bg-white"
        self.fields['category'].widget.attrs.update({'class': select_class})
        self.fields['vendor'].widget.attrs.update({'class': select_class})
        self.fields['product_status'].widget.attrs.update({'class': select_class})