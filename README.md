# ParseRx
Medication sig parser.

**Features:**
- Custom Django Rest Framework API built in.
- Custom ReactJS frontend review and demo tool w/ easy documentation reference.
- API and Python module support parsing individual sigs and batch parsing CSV sigs.  
- Supports feedback loop from "customers" via API call.
- Accepts NDCs or RXCUIs via API call to infer things like method, route, or dose form if missing from sig text.
- Version controls sigs that parse differently after code changes. API has logic built in to return the most recent version that is positively reviewed, OR will always return the most recent version if there are no reviews.


## Getting started

Instructions for Linux:

Clone repo and cd into `parserx` directory.

Create virutal environment

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```


## Initialize the database

How to initially setup MySQL: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

Info on MySQLClient: https://pypi.org/project/mysqlclient/

Gunicorn/Nginx: https://realpython.com/django-nginx-gunicorn/#replacing-wsgiserver-with-gunicorn

Inital setup of MySQL

```
sudo mysql_secure_installation
```

Follow prompts to create root user password and accept default settings.

```
sudo mysql
CREATE USER 'parserx'@'localhost' IDENTIFIED BY 'P@ssw0rd';
GRANT ALL PRIVILEGES ON parserx.* TO 'parserx'@'localhost' WITH GRANT OPTION;
quit
```

(back in terminal)

```
mysql -u parserx -p
<enter password = P@ssw0rd>
drop database if exists parserx;
create database parserx;
quit
```

(back in terminal)

```
source venv/bin/activate
python manage.py makemigrations
python manage.py makemigrations sig
python manage.py migrate
python manage.py createsuperuser
<follow createsuperuser prompts>
python manage.py runserver localhost:8000
```


## Authenticate and parse a sig via the API

Recommend using Postman

1.) Authenticate with user

```
POST localhost:8000/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<superuser username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}
```

2.) Run query via API

```
POST localhost:8000/sig/
Headers
Content-Type    application/json
Authorization   Token <auth token>
Body
{
    "sig_text": "take 1-2 tabs po qid prn anxiety x7d"
}
```


## Parsing / reparsing an entire CSV of sigs

NOTE: to change the csv file that the API runs:
    - Go to parserx/sig/views
    - Edit filepath in the create method of CsvSigCreateViewSet
    - The csv file is stored in parserx/parsers/csv

Edit the name of the csv file in parserx.io/sig/views.py to be the csv you want to parse.

***NOTE: ensure you have converted it to just one column full of sigs with no header.

This will create new versions of parsed sigs if code has changed to parse a sig differently.  Old versions will still be visible using the Review tool in the frontend.

Postman

1.) Authenticate with superuser

```
POST localhost:8000/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<superuser username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}
```

2.) Run ParseRx on csv file via API

```
POST localhost:8000/csv_sig/
Headers
Content-Type	application/json
Authorization	Token <auth token>
```


## Submiting batch sig reviews to ParseRx via API (feedback loop)

This would be for a "customer" that is receiving parsed sigs and wants to send back some feedback as a batch every night via the API.

1.) Get auth token from ParseRx

```
POST api.parserx.io/auth/token/login/
Headers
Content-Type application/json
Body
{
	"username": "<customer username>",
	"password": "<password>"
}
Response
{
    "auth_token": "<auth token>"
}
```

2.) Sumbit batch reviews to ParseRx

```
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

    ...

]
```


## Starting the frontend

If your API is hosted somewhere other than localhost:8000, go to frontend/webpack.config.js and change `apiUrl` (near the bottom) to the correct URL.

```
cd frontend
npm install
npm start
```

Go to localhost:8080

Log in with superuser username and password.

Once logged in, you should be taken back to the homepage.  You need to refresh the homepage to see additional options in the nav bar for "Review" and "Demo".

Review - lets you review previously parsed sigs and mark them as correct or incorrect.  If incorrect, you can select which components are incorrect. This also gets stored in the database.

Demo - lets you enter individual free text sigs and shows the parsed response.

Sometimes a malformed parsed sig will prevent the Review page from loading. If this happens, either remove the sig from the database in MySQL phpMyadmin or enter 10 new sigs in the Demo page to clear it out.
