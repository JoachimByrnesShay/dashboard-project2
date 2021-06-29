from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from django.utils.translation import ugettext as _
import dns.resolver, dns.exception
from django.utils.safestring import mark_safe

""" checkDomainExists is called from the clean() method of custom user model.  upon user registration or update of email address on user account edit page, will
check if email domain exists. if not, will not validate.technique from dokterbob at https://gist.github.com/dokterbob/876648"""
def checkDomainExists(email):
    try:
        domain = email.split('@')[1]
    except:
        domain = ''
    
    try:
        logger.debug('Checking domain %s', domain)

        results = dns.resolver.query(domain, 'MX')

    except dns.exception.DNSException as e:
        logger.debug('Domain %s does not exist.', e)
        raise ValidationError(mark_safe("Email domain %s could not be found. <br/> Please enter a real email address." % domain))
        
    return email