#!/bin/bash

rm db.sqlite3
rm -rf ./tribeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations tribeapi
python3 manage.py migrate tribeapi
python3 manage.py loaddata users
python3 manage.py loaddata tribeUsers
python3 manage.py loaddata tokens
python3 manage.py loaddata tags
python3 manage.py loaddata events
python3 manage.py loaddata status
python3 manage.py loaddata tickets
