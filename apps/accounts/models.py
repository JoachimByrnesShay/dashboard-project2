import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Custom User class which extends built-in User. Presently, just adds a "bio"
# and a gravatar method. Feel free to add your own new fields here!
#https://stackoverflow.com/questions/36330677/django-model-set-default-charfield-in-lowercase
class UserNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UserNameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class User(AbstractUser):

    bio = models.TextField()
    #username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
    username = UserNameField(max_length=200, unique=True)

    def gravatar(self, size=None):
        GRAVATAR_URL = 'https://gravatar.com/avatar/%s?d=identicon%s'
        email = str(self.email).strip().lower()
        digest = hashlib.md5(email.encode('utf-8')).hexdigest()

        if size:
            size_str = '&s=%i' % size
        else:
            size_str = ''

        return GRAVATAR_URL % (digest, size_str)

 