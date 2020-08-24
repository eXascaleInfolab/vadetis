# Vadetis

Vadetis is web application to perform, compare and validate various anomaly detection algorithms using different configurations. It allows users to upload their own datasets as well as training data in order to perform outlier detection. The datasets can either be shared with other users or only be used by yourself. 
The datasets can be altered by injecting additional outliers.


## Settings

There are two settings.py configuration files (development.py and production.py template). One for development usage and one for productive environment. 
Common settings are defined in the common.py file.

## Development

### Python 3.7
Install python 3.7 along with pip3, then install virtualenv
```
sudo apt install python3.7
sudo apt install python3-pip
sudo apt install python3.7-venv
```

### MySQL 
In order to start, install a MySQL 5.x, create a database and make the necessary configuration in development.py. 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'database_user',
        'PASSWORD': 'database_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### venv
Make a virtual env for development and install all requirements:
```bash
python3.7 -m venv /path/to/new/virtual/environment
cd /path/to/new/virtual/environment
source bin/activate
pip3 install -r /path/to/vadetis/requirements.txt
```

### Database
In order to setup the database go to the main application folder of Vadetis, where the manage.py file is located and run:
```bash
python3 manage.py makemigrations --settings vadetis.settings.development
python3 manage.py migrate --settings vadetis.settings.development
```

### Admin User 
Create an admin user with:
```bash
python3 manage.py createsuperuser --settings vadetis.settings.development
```

To enable login into Vadetis with your super user, make sure that the super users email address has the verified flag set in table "account_emailaddress".


### PyCharm

In PyCharm configure the newly created virtual environment and make sure you set the correct interpreter. 
To run Django you can use the integrated Django template with the correct settings under the environment variables.
```
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=vadetis.settings.development
```

### Start the tool
Either you can directly start the tool from PyCharm IDE running the Django template or by command line. To start the tool from command line run:
```bash
python3 manage.py runserver --settings vadetis.settings.development
```

### Site
Run Vadetis in development mode from the PyCharm configuration and login into the Django admin backend.

Under Sites, add an entry with:

Domain Name: http://localhost:8000

Display Name: Vadetis

### Useful Links
Swagger REST Interface http://localhost:8000/swagger

Django Admin Backend http://localhost:8000/admin 

### Jupyter Notebook
To start Jupyter notebook with Django shell execute from started venv in the main application folder:
```bash
env DJANGO_ALLOW_ASYNC_UNSAFE=true ./manage.py shell_plus --notebook --settings vadetis.settings.development
```

## Automatic Deployment

Run the vadetis_install.sh script from the main application folder. 
It's tested on Ubuntu 18.04. Changes may be needed if you are running a different OS.

```bash
./vadetis_install.sh
```

## Manual Deployment

### Copy contents
Copy the contents of Vadetis into the sites folder for apache, e.g. /var/www/vadetis.exascale.info

### venv
Make a virtual env for production and install all requirements:
```bash
python3.7 -m venv /usr/local/venvs/venv_vadetis
cd /usr/local/venvs/venv_vadetis
source bin/activate
pip3 install -r /var/www/vadetis.exascale.info/requirements.txt
```

### Database

Similar to development mode, we have to setup the database
```bash
python3 manage.py makemigrations --settings vadetis.settings.production
python3 manage.py migrate --settings vadetis.settings.production
```

Create an admin user
```bash
python3 manage.py createsuperuser
```
To enable login into Vadetis with your super user, make sure that the super users email address has the verified flag set in table "account_emailaddress".

### Apache

```bash
sudo apt install apache2
```
On Linux systems, if Apache has been installed from a package repository, you must have installed the corresponding Apache "dev" package as well.
```bash
sudo apt install apache2-dev
```

Other extensions needed:
```bash
sudo apt install apache2-utils ssl-cert
```

### mod_wsgi
The following steps are described on https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html

Download [mod_wsgi](https://github.com/GrahamDumpleton/mod_wsgi/releases) from https://github.com/GrahamDumpleton/mod_wsgi/releases
After having downloaded the tar ball for the version you want to use, unpack it with the command:
```
tar xvfz mod_wsgi-X.Y.tar.gz
```
Replace ‘X.Y’ with the actual version number for that being used
To setup the package ready for building run the “configure” script from within the source code directory:
```
./configure
```
The configure script will attempt to identify the Apache installation to use by searching in various standard locations for the Apache build tools included with your distribution called “apxs2” or “apxs”. If not found in any of these standard locations, your PATH will be searched.

Which Python installation to use will be determined by looking for the “python” executable in your PATH.
        
If these programs are not in a standard location, they cannot be found in your PATH, or you wish to use alternate versions to those found, the --with-apxs and --with-python options can be used in conjunction with the “configure” script:
```
./configure --with-apxs=/usr/local/apache/bin/apxs --with-python=/usr/bin/python3.7
```
If makefile succeeded, then the package has been configured, it can be built by running:
```
make
```
If the mod_wsgi source code does not build successfully, see: https://modwsgi.readthedocs.io/en/develop/user-guides/installation-issues.html

To install the Apache module into the standard location for Apache modules as dictated by Apache for your installation, run:
```
sudo make install
```
Once the Apache module has been installed into your Apache installation’s module directory, it is still necessary to configure Apache to actually load the module.
Exactly how this is done and in which of the main Apache configuration files it should be placed, is dependent on which version of Apache you are using and may also be influenced by how your operating system’s Apache distribution has organised the Apache configuration files. You may therefore need to check with any documentation for your operating system to see in what way the procedure may need to be modified.
In the simplest case, all that is required is to add a line of the form:
```
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
```
into the main Apache “httpd.conf” configuration file at the same point that other Apache modules are being loaded. (In Ubuntu, all configuration options have been moved to apache2.conf)
If your apache version uses "mods-enabled/mods-available" with symlinks, add a mod_wsgi.load file in "mods-available" with:
```
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
```
Then enable by 
```
sudo a2enmod mod_wsgi
sudo service apache2 restart
```
Afterwards mod_wsgi should be listed in "mods_enabled".


### Apache Configuration for mod_wsgi
Once you’ve got mod_wsgi installed and activated, add a virtual host file "vadetis.conf" in /etc/apache/sites-available

```
<VirtualHost *:80>
    # This is name based virtual hosting. So place an appropriate server name
    #   here. Example: django.devsrv.local
    ServerName  vadetis.exascale.info
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/vadetis.exascale.info

    # This alias makes serving static files possible.
    #   Please note, that this is geared to our settings/common.py
    #   In production environment, you will propably adjust this!
    Alias /static/  /var/www/vadetis.exascale.info/run/static/

    # This alias makes serving media files possible.
    #   Please note, that this is geared to our settings/common.py
    #   In production environment, you will propably adjust this!
    Alias /media/  /var/www/vadetis.exascale.info/run/media/

    # Insert the full path to the wsgi.py-file here
    WSGIScriptAlias /   /var/www/vadetis.exascale.info/vadetis/wsgi.py

    #Required for extensions that use C, e.g. scipy, numpy (!!!)
    WSGIApplicationGroup %{GLOBAL}

    # PROCESS_NAME specifies a distinct name of this process
    #   see: https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIDaemonProcess
    # PATH/TO/PROJECT_ROOT is the full path to your project's root directory,
    #   containing your project files
    # PATH/TO/VIRTUALENV/ROOT: If you are using a virtualenv specify the full
    #   path to its directory.
    #   Generally you must specify the path to Python's site-packages.
    WSGIDaemonProcess   vadetis     python-home=/usr/local/venvs/venv_vadetis   python-path=/var/www/vadetis.exascale.info

    # PROCESS_GROUP specifies a distinct name for the process group
    #   see: https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIProcessGroup
    WSGIProcessGroup    vadetis

    <Directory /var/www/vadetis.exascale.info/vadetis>
    <Files wsgi.py>
    Require all granted
    </Files>
    </Directory>

    # Serving static files from this directory
    #   Please note, that this is geared to our settings/common.py
    #   In production environment, you will propably adjust this!
    <Directory /var/www/vadetis.exascale.info/run/static>
        Options -Indexes
        Order deny,allow
        Allow from all
    </Directory>

    # Serving media files from this directory
    #   Please note, that this is geared to our settings/common.py
    #   In production environment, you will propably adjust this!
    <Directory /var/www/vadetis.exascale.info/run/media>
        Options -Indexes
        Order deny,allow
        Allow from all
    </Directory>

    LogLevel warn

    # PROJECT_NAME is used to separate the log files of this application
    ErrorLog    /var/log/apache2/vadetis.exascale.info/vadetis_error.log
    CustomLog   /var/log/apache2/vadetis.exascale.info/vadetis_access.log combined
</VirtualHost>
```

Make sure Apache is configured to accept non-ASCII file names:
```
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
```

A common location to put this configuration is /etc/apache2/envvars.

### Collect static files

On the server, run collectstatic to copy all the static files into STATIC_ROOT.
```bash
cd /var/www/vadetis.exascale.info
source /usr/local/venvs/venv_vadetis/bin/activate
python3 manage.py collectstatic --settings vadetis.settings.production
```

### Site

Activate the site with:
```
cd /etc/apache2/sites-available
sudo a2ensite vadetis
sudo service apache2 reload
sudo service apache2 restart
```

You may have to edit /etc/hosts file for the domain.

With Vadetis in production mode running, login into the Django admin backend.

Under Sites, add an entry with your domain name, e.g.:

Domain Name: http://vadetis.exascale.info (or https://vadetis.exascale.info if SSL is configured)

Display Name: Vadetis

### Start and stop the tool

After deployment the tool should be already running. However you can enable Vadetis with:
```
sudo a2ensite vadetis
sudo service apache2 reload
```

to disable Vadetis, run:
```
sudo a2dissite vadetis
sudo service apache2 reload
```