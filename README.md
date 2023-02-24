# Earthquake information webapp using Python and Flask

## Prerequisites

The following commands have already been installed.

* Python3
* pip
* Heroku CLI

## Setup

install dependencies

```
pip install Flask gunicorn flask-bootstrap pytest
```

## Start server

```
python3 app.py
```

## Run test

```
cd ./test
python3 -m pytest
```

## Deploy to Heroku

create setting files for Heroku

```
echo "web: gunicorn app:app --log-file=-" > Procfile

python3 -m pip freeze > requirements.txt
```