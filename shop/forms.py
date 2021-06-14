from django import forms
from django.forms.widgets import TextInput, Textarea
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .choices import (CATEGORIES)


class AddProductForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Name of Product'
    }))
    price = forms.IntegerField(initial=0)
    discount_price = forms.IntegerField(initial=0)
    description = forms.CharField(widget=Textarea(attrs={
        'placeholder': 'Enter description for the Product'
    }))
    category = forms.ChoiceField(choices=CATEGORIES, required=True)

