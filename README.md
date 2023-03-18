# ParseRx
Medication sig parser.


## Getting started

python3 -m venv venv
source venv/bin/activate
pip install django
pip install djangorestframework
pip install "djangorestframework-api-key==2.*"
pip install django-cors-headers
pip install djoser
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient


## Initialize the database

How to initially setup MySQL: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
Info on MySQLClient: https://pypi.org/project/mysqlclient/
Gunicorn/Nginx: https://realpython.com/django-nginx-gunicorn/#replacing-wsgiserver-with-gunicorn

sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'mynewpassword';
GRANT ALL PRIVILEGES ON parserx.* TO 'parserx'@'localhost' WITH GRANT OPTION;

Terminal

mysql -u parserx -p
<enter password>
drop database parserx;
create database parserx;
quit
source venv/bin/activate
python manage.py makemigrations
python manage.py makemigrations sig
python manage.py migrate
python manage.py createsuperuser
<follow createsuperuser prompts>
python manage.py runserver 0.0.0.0:8000

Postman

1.) Authenticate with superuser
POST localhost:8000/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "jrlegrand",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}

2.) Run ParseRx on csv file via API
POST localhost:8000/csv_sig/
Headers
Content-Type application/json
Authorization Token <auth token>

NOTE: to change the csv file that the API runs:
    - Go to parserx/sig/views
    - Edit filepath in the create method of CsvSigCreateViewSet
    - The csv file is stored in parserx/parsers/csv


## Authenticate and parse a sig via the API

1.) Authenticate with user
POST localhost:8000/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}

2.) Run query via API
POST localhost:8000/sig/
Headers
Content-Type    application/json
Authorization   Token <auth token>


## Parsing / reparsing an entire CSV of sigs

Edit the name of the csv file in parserx.io/sig/views.py to be the csv you want to parse.
***NOTE: ensure you have converted it to just one column full of sigs with no header.

Postman

1.) Authenticate with superuser
POST localhost:8000/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}

2.) Run ParseRx on csv file via API
POST localhost:8000/csv_sig/
Headers
Content-Type	application/json
Authorization	Token <auth token>


## Submiting batch sig reviews to ParseRx via API (feedback loop)

1.) Get auth token from ParseRx
POST api.parserx.io/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}

2.) Sumbit batch reviews to ParseRx
POST api.parserx.io/sig_reviewed/
Headers
Content-Type application/json
Authorization Token <auth token>
Body
[
    {
        "owner": <user_id>,
        "sig_parsed": <sig_parsed_id>,
        "sig_correct": "<true|false>",
        "sig_corrected": "<sig_corrected>"        
    }
]
