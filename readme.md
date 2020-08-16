# Vadetis

Vadetis is web application to perform, compare and validate various anomaly detection algorithms using different configurations. It allows users to upload their own datasets as well as training data in order to perform outlier detection. The datasets can either be shared with other users or only be used by yourself. 
The datasets can be altered by injecting additional outliers.


## Prerequisites

There are two settings.py configuration files (development.py and production.py). One for development usage and one for productive environment. 
Common settings are defined in the common.py file.

### MySQL 
In order to start, install a MySQL 5.x, create a database and make the necessary configuration in development.py and production.py files. 
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

### Python 3.7
Install python 3.7 along with pip3, then install virtualenv
```
sudo apt install python3.7
sudo apt install python3-pip
sudo apt install python3.7-venv
```

## Development

### Database
In order to setup the database go to the main application folder of Vadetis, where the manage.py file is located and run:
```bash
python3 manage.py makemigrations --settings vadetis.settings.development
python3 manage.py migrate --settings vadetis.settings.development
```
Create an admin user
```bash
python3 manage.py createsuperuser
```

### venv
Make a virtual env for development and install all requirements:
```bash
python3 -m venv /path/to/new/virtual/environment
cd /path/to/new/virtual/environment
source bin/activate
pip3 install -r /path/to/vadetis/requirements.txt
deactivate
```

### PyCharm

In PyCharm configure the newly created virtual environment and make sure you set the correct interpreter. 
To run Django you can use the integrated Django template with the correct settings under the environment variables.
```
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=vadetis.settings.development
```

### Site


### Useful Links
Swagger REST Interface http://localhost:8000/swagger

Django Admin Backend http://localhost:8000/admin 

## Deployment

### Database


```bash
python3 manage.py makemigrations --settings vadetis.settings.production
python3 manage.py migrate --settings vadetis.settings.development
```

### Apache

```bash
sudo apt install apache2
```
On Linux systems, if Apache has been installed from a package repository, you must have installed the corresponding Apache "dev" package as well.
```bash
sudo apt install apache2-dev
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
systemctl restart apache2
```
Afterwards mod_wsgi should be listed in "mods_enabled".

### Directories and venv
Create directory to place the page, e.g.
```
mkdir /var/www/vadetis.exascale.info
mkdir /var/www/vadetis.exascale.info/vadetis
```
Create a virtual python 3.7 environment, e.g.
```
mkdir /var/www/vadetis.exascale.info/venv
python3.7 -m venv /var/www/vadetis.exascale.info/venv
```

Copy contents of vadetis into the folder /var/www/vadetis.exascale.info
Install python requirements in venv
```
cd /var/www/vadetis.exascale.info
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
```


Check if the venv is working
```
cd /var/www/vadetis.exascale.info/venv
source bin/activate
deactivate
```

### Apache Configuration for mod_wsgi
Once you’ve got mod_wsgi installed and activated, edit your Apache server’s httpd.conf or apache2.conf file and add the following.

```
WSGIScriptAlias / /var/www/vadetis.exascale.info/vadetis/wsgi.py
WSGIPythonHome /var/www/vadetis.exascale.info/venv
WSGIPythonPath /var/www/vadetis.exascale.info

<Directory /var/www/vadetis.exascale.info/vadetis>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

Make sure Apache is configured to accept non-ASCII file names:
```
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
```

A common location to put this configuration is /etc/apache2/envvars.


## Jupyter Notebook
To start Jupyter notebook with Django shell execute from started venv in the main application folder:
```bash
env DJANGO_ALLOW_ASYNC_UNSAFE=true ./manage.py shell_plus --notebook --settings vadetis.settings.development
```