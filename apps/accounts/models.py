import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from django.utils.translation import gettext as _
# Note: we need dnspython for this to work
import dns.resolver, dns.exception
from django.utils.safestring import mark_safe
# Custom User class which extends built-in User. Presently, just adds a "bio"
# and a gravatar method. Feel free to add your own new fields here!
#https://stackoverflow.com/questions/36330677/django-model-set-default-charfield-in-lowercase
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


# checks if domain user enters for email field is a real functioning domain
# source for cheking domain is here
# https://gist.github.com/dokterbob/876648/22fe8830c7beb419c02060ffa2658749d94d4b6d
# https://pypi.org/project/email-validator/
# https://stackoverflow.com/questions/47076555/check-email-validation-django
# https://stackoverflow.com/questions/11653471/newline-in-label-for-django-form-field
# https://stackoverflow.com/questions/12995888/name-is-not-defined/12995923
# https://github.com/pennersr/django-allauth
# https://stackoverflow.com/questions/654380/modify-value-of-a-django-form-field-during-clean



class User(AbstractUser):

    bio = models.TextField()
    #username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
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
        # running this check before any other validations
        def checkDomainExists(email):
            print(email)
            print(email.__class__)
            try:
                domain = email.split('@')[1]
            except:
                domain = ''
            
            try:
                logger.debug('Checking domain %s', domain)

                results = dns.resolver.query(domain, 'MX')

            except dns.exception.DNSException as e:
                logger.debug('Domain %s does not exist.', e)
                raise \
                    ValidationError(mark_safe("Email domain %s could not be found. <br/> Please enter a real email address."
                                          % domain))
            return email
        checkDomainExists(self.email)
        # Make sure the domain exists
        
       
