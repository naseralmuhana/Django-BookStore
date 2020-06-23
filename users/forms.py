from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput
from users import models


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(max_length=25, )
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class UserUpdeteForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdeteForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = ['phone', 'address', 'zip_code', 'city', 'country', 'image']

