## Start with installing dependencies:
use: pip install -r requirements.txt

## Install Mysql Client and create "restaurant" Database

## Then database imigration
* For the initial migration:
* 1. flask db init
* 2. Then config alembic.ini file add this code "sqlalchemy.url = mysql://root:root@localhost/restaurant" 
* 2. flask db migrate -m "Initial migration"
* 3. flask db upgrade

* For update migration:
* 1. flask db migrate
* 2. flask db upgrade