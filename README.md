# Earthquake information webapp 🌎

Earthquakes occur all over the world everyday.

Recently, a huge earthquake occurred in Turkey.
I was born in Japan, where earthquakes occur frequently, often two or three times a week. I was shocked by this news, as I had lived without earthquakes since I left Japan.

The reason why I chose this data for the development of data-driven web app was because I wanted to find out how often and in which regions of the world earthquakes occur. And I want to warn people who have never experienced an earthquake that this disaster could happen at any moment.

Due to data size regulations, the earthquake data is limited to the period 1st to 19th February 2023. Data is taken from [USGS Earthquake Hazards Program.](https://earthquake.usgs.gov/earthquakes/feed/) which is open source.

## Heroku URL
This webapp is hosting on `Heroku`.

https://earthquake-info-app.herokuapp.com/

## About project

### Used frameworks, libraries and services

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
     * Python web application framework, suitable for creating simple web applications for small.
     
* [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
     * A front-end web application framework for creating websites and web applications which provides parts such as buttons to help UI implementation.
     
* [pytest](https://docs.pytest.org/en/7.2.x/)
     * A python testing framework primarily to support unit testing. It enables efficient creation and execution of tests.
     
* [Font Awesome](https://fontawesome.com/)
     * Popular icon toolkit; can be used by loading CDNs.
     
* [Heroku](https://dashboard.heroku.com/apps)
     * Paas cloud service to help develop and publish applications.
     * The integration between Heroku and Github is already set up, so a push to the main branch of this repogitory is triggered and deployed automatically.

### Directory structure

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
     └─ earthquake_table.html - table template 

```

## For setup

### Prerequisites

The following commands have already been installed.

* Python3 (with greather v.3.9)
* pip
* sqlite3
* Heroku CLI


### Setup guide

Install dependencies using `pip`.

```commandline
pip install Flask gunicorn flask-bootstrap pytest
```

Start python application with this command.

```commandline
python3 app.py

# In codio
python3 -m flask run -h 0.0.0.0
```

Run `pytest` to ensure that the application works.

```commandline
cd ./test
python3 -m pytest
```

---

### Deploy to Heroku

Create setting files for `Heroku`.
`Requirement.txt` must be re-created each time new library is installed by pip. 

The integration between Heroku and Github is already set up, so a push to the main branch of this repogitory is triggered and deployed automatically.

```commandline
echo "web: gunicorn app:app --log-file=-" > Procfile

python3 -m pip freeze > requirements.txt
```

### Restore earthquaked database

If data is lost or the database is corrupted, execute sqlite command with `earthquakes.db` to restore the database.

```commandline
cd ./data
sqlite3 earthquake_data.db < ./backup/earthquakes.sql
```
### ⚠️ Attention
Please check the Python verssion is greater than `v3.9` because `fromisoformat` is not available in older than `v3.7` and `removesuffix` is not available in older than `v3.9`.
