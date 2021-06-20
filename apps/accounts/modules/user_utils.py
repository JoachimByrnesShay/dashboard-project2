from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from django.utils.translation import ugettext as _
# Note: we need dnspython for this to work
import dns.resolver, dns.exception
from django.utils.safestring import mark_safe

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