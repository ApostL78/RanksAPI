[![Django CI](https://github.com/ApostL78/RanksAPI/actions/workflows/django.yml/badge.svg)](https://github.com/ApostL78/RanksAPI/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/ApostL78/RanksAPI/graph/badge.svg?token=MBFC9OE5B7)](https://codecov.io/gh/ApostL78/RanksAPI)
# Touch it without cloning

https://apostl78.pythonanywhere.com/admin/
login: test    password: test
# How To Run
To start this app you need to:
1. Clone this repo and move to project
```sh
git clone https://github.com/ApostL78/RanksAPI.git && cd RanksAPI
```
2. Create and activate `venv`
```sh
python3 -m venv venv && source ./venv/bin/activate
```
3. Create environment variables
```sh
cp .env.example .env
```
and then put your values
4. Run with docker-compose
```sh
docker-compose up --build -d
```
After the application starts, navigate to `http://localhost:8000` in your web browser.
5. For best usage go inside web app container
```sh
docker-compose exec -it web bash
``` 
then run command and create super user to manage data in admin page
```sh
python3 manage.py createsuperuser
```
Login in admin panel, create instances and check endpoints `item/<int:pk>` and `order/<int:pk>`
