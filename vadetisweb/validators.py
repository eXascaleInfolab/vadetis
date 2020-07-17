import re

from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import EmailValidator, RegexValidator

#alphabetic_validator = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
alphabetic_validator = RegexValidator(re.compile('[^\W\d_]+$', re.UNICODE), 'Only characters are allowed.')
alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


username_validators = [ASCIIUsernameValidator()]
email_validators = [EmailValidator()]