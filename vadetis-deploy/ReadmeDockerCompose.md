Cheatsheet Docker Compose

```
docker-compose up --build web

docker-compose exec web python manage.py makemigrations vadetisweb --settings vadetis.settings.production
docker-compose exec web python manage.py makemigrations --settings vadetis.settings.production
docker-compose exec web python manage.py migrate --settings vadetis.settings.production
docker-compose exec web python manage.py createsuperuser --settings vadetis.settings.production
docker-compose exec web python manage.py collectstatic --settings vadetis.settings.production

docker-compose logs -f
```

To inspect the runnig container:
```bash
docker-compose exec web bash
```

Production
-----------

```bash
docker context create srv-exascale --docker "host=ssh://user@hostname"
docker --context srv-exascale ps
```
Update the running production server

```bash
docker-compose --context srv-exascale build web
docker-compose --context srv-exascale up --no-deps -d web
```


Resources
----------

* https://medium.com/swlh/django-deployed-docker-compose-1446909a0df9
