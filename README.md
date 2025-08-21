# PDC Website

Author: Michael Herring <mherring@gmail.com>

## Set Up

```
# Build and start containers
docker-compose up

# Run DB migrations
docker-compose exec web ./manage.py migrate

# Create superuser
docker-compose exec web ./manage.py createsuperuser
```

## Run Tests

The following script will run:
* flake8 - syntax and style checker
* mypy - type checker
* unit tests

```
./check
```

# Deploying

Deploy files:

```
./deploy
```

Restart gunicorn socket:

```
systemctl restart gunicorn.socket
```

If there are changes to nginx

```
cp /srv/pdc/server/nginx/petersburgdemocrats.org /etc/nginx/sites-available/petersburgdemocrats.org
# test config
sudo nginx -t
# restart
sudo service nginx restart
```

If there are changes to static files:

```
cd /srv/pdc
source djangoenv/bin/activate
./manage.py compilescss
./manage.py collectstatic
```

If there are database migrations:

```
cd /srv/pdc
source djangoenv/bin/activate
./manage.py migrate
```
