# Earthquake information webapp

## Prerequisites

The following commands have already been installed.

* Python3
* pip
* Heroku CLI

## Directory structure

```
data-driven-web-app
│
├─ app.py      - main app file
├─ database.py - database class file
├─ Procfile         - for Heroku
├─ requirement.txt  - for Heroku
├─ runtime.txt      - for Heroku
│
├─ test
│   └─ app_test.py
│
├─ data
│   ├─ earthquake_data.db
│   └─ backup
│      ├─ earthquake_data.csv - open source data
│      └─ earthquakes.sql     - create and insert sql
│
├─ static
│   ├─ css
│   │  ├─ space.css
│   │  └─ style.css
│   └─ image
│
└─templates
     ├─ base.html
     ├─ 404_page.html  - for /404
     ├─ all_page.html  - for /all
     ├─ home_page.html - for /home
     ├─ ranking_page.html - for /ranking
     ├─ search_page.html  - for /search
     ├─ magnitude_type_page.html - for /magnitude_type
     └─ earthquake_table.html - table component 

```

## Setup

Install dependencies using `pip`.

```commandline
pip install Flask gunicorn flask-bootstrap pytest
```

## Start application

Start python application with this command.

```commandline
python3 app.py
```

## Run test

Run `pytest` to ensure that the application works.

```commandline
cd ./test
python3 -m pytest
```

## Deploy to Heroku

Create setting files for `Heroku`. <br/>
`Requirement.txt` must be re-created each time new library is installed by pip.

```commandline
echo "web: gunicorn app:app --log-file=-" > Procfile

python3 -m pip freeze > requirements.txt
```

## Restore earthquaked database

If data is lost or the database is corrupted, execute sqlite command with `earthquakes.db` to restore the database.

```commandline
cd ./data
sqlite3 earthquake_data.db < ./backup/earthquakes.sql
```