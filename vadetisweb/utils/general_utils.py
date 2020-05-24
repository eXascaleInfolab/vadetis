from vadetisweb.parameters import *
from vadetisweb.models import UserSetting

def strToBool(v):
    s = str(v).lower()
    if s in ('true', 'yes', '1'):
         return True
    elif s in ('false', 'no', '0'):
         return False
    else:
         raise ValueError
