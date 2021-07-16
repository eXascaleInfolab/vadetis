# Vadetis

[**Prerequisites**](#prerequisites) | [**Auto Deployment**](#auto-deployment)  | [**Manual Depolyment**](#manual-deployment)

___

## Prerequisites
- Working Python 3 environment (for development)
- Docker and Docker-Compose installed (for production)
- Cloned this repository.
___

## Development Setup

With this setup Vadetis uses a SQLite Database and prints e-mails on the console.

To work with timeserie with spatial data you will need to add your mapbox credentials to *vadetis/settings/.env*.

### Setup

### Python 3
Install python 3.7 or later along with pip3 and virtualenv. For Ubuntu:
```
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
```

### venv
Make a virtual env for development and install all requirements:
```bash
python3 -m venv /path/to/new/virtual/environment
cd /path/to/new/virtual/environment
source bin/activate
pip3 install -r /path/to/vadetis/slow_requirements.txt
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

```
Domain Name: http://localhost:8000
Display Name: Vadetis
```

Under Users, enable the e-mail verified flag.

### Useful Links

* Swagger REST Interface http://localhost:8000/swagger
* Django Admin Backend http://localhost:8000/admin 

### Jupyter Notebook
To start Jupyter notebook with Django shell execute from started venv in the main application folder:
```bash
env DJANGO_ALLOW_ASYNC_UNSAFE=true ./manage.py shell_plus --notebook --settings vadetis.settings.development
```
___


## Production Deployment

With this setup Vadetis uses a PostgreSQL Database and sends out e-mail with the configured SMTP server. We use docker-compose to orchastrate 3 containers: web (django), db (postgres) and nginx (nginx).
We provide a prebuilt version of the container on [dockerhub](https://hub.docker.com/r/exascalelab/vadetis) which is also used in docker-compose.yml by default. This means that if you want to deploy a unmodified version of Vadetis, you can skip the next step (build image). Otherwise you will have to build the image, upload this image to a docker registry and change the "image" field in docker-compose.yml to the location of the uploaded image.


### Build Image

```bash
docker build -t username/vadetis:version .
docker login
docker push username/vadetis:version
```
### Deploy remotly

Copy \[db|web\]-variables_template.env to \[db|web\]-variables.env and fill in the db credentials (which can be freely choosen) and the email, recaptcha and mapbox credentials (given to you by the corresponding vendor).
By default the built-in webserver will listen on port 12006, if no other webserver is running on the host, you might want to simply change this to 80, avoiding having to run another webserver in front of it.

```bash
docker-compose up -d
```

We setup the database
```bash
docker-compose exec web python manage.py makemigrations vadetisweb --settings vadetis.settings.production
docker-compose exec web python manage.py makemigrations --settings vadetis.settings.production
docker-compose exec web python manage.py migrate --settings vadetis.settings.production
```

We create a superuser

```bash
docker-compose exec web python manage.py createsuperuser --settings vadetis.settings.production
docker-compose exec web python manage.py collectstatic --settings vadetis.settings.production
```
To enable login into Vadetis with your superuser, make sure that you login via the admin interface (/admin) and set the verified flag for the email address.

With Vadetis in production mode running, login into the Django admin backend.

Under Sites, add an entry with your domain name, e.g.:

* Domain Name: http://vadetis.exascale.info (or https://vadetis.exascale.info if SSL is configured)
* Display Name: Vadetis

