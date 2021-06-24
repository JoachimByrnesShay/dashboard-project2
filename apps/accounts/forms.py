from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
 
from apps.accounts.models import User

from django.core.exceptions import ValidationError
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm



""" require firstname and lastname if user is editing user's account information,
on user myaccount page.  THese are not required at registration.  clean method employed below 
for each name field to accomplish this in usereditform"""
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'bio',
        )
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
       
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


""" user registration form with custom help_texts. reflects user model has been made to treat variations of case for usernames and emails
as the same value (thus raising uniqueness validation errors when case is the only variance), and also reflects some custom validation is applied using domain lookup 
to ensure email entered at registration or update has valid (existing) domain.  logic ensuring case-insensitivity of user info is in accounts.models.py"""

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        help_texts = {
            'username': 'User name is case-insensitive and must be unique',
            'email': 'Email must contain valid domain and be unique',
        }
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['password2'].help_text = 'Enter password a second time.'
       

