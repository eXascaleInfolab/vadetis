"""
WSGI config for vadetis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application

"""#Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/vadetis.exascale.info/venv/lib/python3.7/site-packages/')
#Add the app's directory to the python path
sys.path.append('/var/www/vadetis.exascale.info/vadetis')
sys.path.append('/var/www/vadetis.exascale.info/vadetis/vadetisweb')"""

#Activate your virtualenv
"""activate_env =         os.path.expanduser('/var/www/.virtualenvs/projectenv/bin/activate_this.py'    )
execfile(activate_env, dict(__file__=activate_env))"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vadetis.settings_prod')

application = get_wsgi_application()
