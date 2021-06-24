import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from .modules import user_utils


""" define get_prep_value on usernamefield and useremailfield to convert all username and email to lowercas
before they are saved, thus ensuring that uniqueness on a case-insensitivity basis for these fields.
technique from here https://stackoverflow.com/questions/36330677/django-model-set-default-charfield-in-lowercase"""
class UserNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UserNameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class UserEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        super(UserEmailField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):    
        print(value)
        return str(value).lower()


""" custom user class, with clean() method overriden to run checkDomainExists (custom method imported from custom module) on self.email"""
class User(AbstractUser):

    bio = models.TextField(blank=True, null=True)
    username = UserNameField(max_length=200, unique=True)
    email = UserEmailField(unique=True)
  

    def gravatar(self, size=None):
        GRAVATAR_URL = 'https://gravatar.com/avatar/%s?d=identicon%s'
        email = str(self.email).strip().lower()
        digest = hashlib.md5(email.encode('utf-8')).hexdigest()

        if size:
            size_str = '&s=%i' % size
        else:
            size_str = ''

        return GRAVATAR_URL % (digest, size_str)

    

    def clean(self):
        # custom checkDomainExists method which will perform model-level validation based on domain lookup, only passes validator if domain exists
        user_utils.checkDomainExists(self.email)
      
        
       
