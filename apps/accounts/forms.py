from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from apps.accounts.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'bio',
        )

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

        #for fieldname in ['username', 'password1', 'password2']:
        self.fields['password2'].help_text = 'custom message about password confirm'
       

