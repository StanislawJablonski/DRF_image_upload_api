# Django rest framework image upload app

## Technologies
* Python  3.9.6
* Django 4.2.5


## Urls
PUBLIC URLS
- http://127.0.0.1:8000/api/v1/accounts/register/
- http://127.0.0.1:8000/api/v1/accounts/login/

ADMIN URLS
- http://127.0.0.1:8000/admin/

AUTHENTICATED USERS
- http://127.0.0.1:8000/api/v1/images/
- http://127.0.0.1:8000/api/v1/images/upload/
- http://127.0.0.1:8000/api/v1/images/expiring-links/ 

ADVANCED API DOCS 
- http://127.0.0.1:8000/api/swagger/
- http://127.0.0.1:8000/api/redoc/

## How to run
Run using docker compose
- clone the repository
- open terminal in project folder
- run `docker-compose up -d --build`
- create a test super account with `docker-compose exec backend python manage.py create_test_superuser`
