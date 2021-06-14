from user.models import Address, PROVINCES
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django_countries.conf import Settings
from phonenumber_field.formfields import PhoneNumberField


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150,help_text='Must be between 4 to 150 characters')
    email = forms.EmailField(label='Enter Email')
    phone = PhoneNumberField(label='Enter Mobile Number')
    password1 = forms.CharField(label='Enter Password',widget=forms.PasswordInput,help_text='Your password must contain at least 8 characters.')
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput,help_text='Enter the same password as before, for verification.')
    profile_pic = forms.ImageField(allow_empty_file=True, required=False,label='Upload Profile Pic')
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        repeat = User.objects.filter(username=username)
        if repeat.count():
            raise ValidationError("Username Already Exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        repeat = User.objects.filter(email=email)
        if repeat.count():
            raise ValidationError("Email Already Exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password Don't Match")
        return password2
    
    def save(self,commit=True):
        # create_user will create user with password hashing and other usefull features
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password1'],
        )
        # user.profile.profile_pic = self.cleaned_data['password1']
        return user


Settings.COUNTRIES_FIRST = ['PK']
class AddAddressForm(forms.Form):
    country = CountryField(blank=False,blank_label='(Select country)').formfield()
    province = forms.ChoiceField(choices=PROVINCES, required=True)
    city = forms.CharField(max_length=150,required=True)
    street_address = forms.CharField(max_length=250,required=False)
    zip = forms.IntegerField(required=False,)

    def save(self,commit=True):
        # create_user will create user with password hashing and other usefull features]
        address = Address.objects.create(
            country = self.cleaned_data.get('country'),
            province = self.cleaned_data.get('province'),
            city = self.cleaned_data.get('city'),
            street_address = self.cleaned_data.get('street_address'),
            zip = self.cleaned_data.get('zip')
        )
        # user.profile.profile_pic = self.cleaned_data['password1']
        return address