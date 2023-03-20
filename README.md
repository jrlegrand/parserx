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

## API documentation

### Request authentication

All requests must have an API key.

Create your own API key at http://localhost:8000/admin

**To authenticate:**

Headers of your request must include:

```
Authorization: Api-Key <your API key here>
Content-Type: application/json
```

Invalid API keys will result in an HTTP 401, Unauthorized error.

### API resources

The ParseRx API expects HTTP URL request parameters and returns JSON responses. All requests must include your API key.

**Request**

`POST /sig/` = Generate / return a parsed sig and information on review status.

URL = http://localhost:8000/sig/

Format = JSON

Body

- `sig_text` (REQUIRED) string - your sig text here
- `ndc` (optional) numeric ndc11 string - if you want to infer sig elements by ndc
- `rxcui` (optional) numeric rxcui string - if you want to infer sig elements by rxcui

Example:

```
{
    "sig_text": "tk 1-2 tab po qid x10d prn pain",
    "ndc": "12345678911", 
    "rxcui": "123456"
}
```

NOTE: Depending on whether you submit a sig that ParseRx has parsed before, you will receive two different server responses.

- HTTP 200, OK - ParseRx has parsed this sig before, so it is just returning that previously parsed sig from the database.
- HTTP 201, Created - ParseRx has not parsed this sig before, so it is dynamically parsing it, saving it to the database, and returning the result.

**Response**

`sig_text`

A string containing the modified sig_text from the request, converted to lower case, extraneous characters removed, and duplicate spaces converted to single spaces.

`sig_parsed`

A JSON object containing all the parsed components of the free text sig. See details of each component below.

`sig_inferred`

A JSON object containing all the inferred sig components if the request included an ndc or rxcui parameter. See details of each component below.

This entire object will only appear if a valid ndc or rxcui are included as a request parameter. If both are included, ndc will take precedence over rxcui.

`original_sig_text`

A string containing the original, un-modified sig_text from the request.

**Parsed sig components**

`method`

How the medication is administered (i.e. take, inject, inhale).

`dose`

`dose_max`

`dose_unit`

How much medication patient is instructed to take based on dosage (i.e. 2 tablets, 30 units, 1-2 puffs).

Numbers represented as words in the sig will be converted to integers (i.e. “one” will be converted to 1).

`strength`

`strength_max`

`strength_unit`

How much medication the patient is instructed to take based on strength (i.e. 500 mg, 15 mL, 17 g).

NOTE: ParseRx intentionally does not parse multiple ingredient strengths (i.e. if 5/325 mg is in a sig, it will return null for strength).

`route`

Route of administration of the medication (i.e. by mouth, via inhalation, in left eye).

`frequency`

`frequency_max`

`period`

`period_max`

`period_unit`

`time_duration`

`time_duration_unit`

`day_of_week`

`time_of_day`

`when`

`offset`

`bounds`

`count`

`frequency_readable`

How often medication should be administered (i.e. every 4-6 hours, three times daily, once daily in the morning with meal).

Due to the complexity and variety of medication instructions, these elements are based off of an existing standard - FHIR Timing.

For convenience, a frequency_readable is generated to represent a human-readable representation of the sig frequency.

`duration`

`duration_max`

`duration_unit`

How long the patient is instructed to take the medication (i.e. for 7 days, for 7-10 days, for 28 days).

NOTE: this is different from days’ supply, which represents how long a given supply of medication should last.

`as_needed`

`indication`

Whether the medication should be taken “as needed” (i.e. PRN), and the specific reason the patient is taking the medication (i.e. for pain, for wheezing and shortness of breath, for insomnia).

NOTE: indication may be populated even if as_needed is false. There are chronic indications represented in sigs as well (i.e. for cholesterol, for high blood pressure, for diabetes).

`sig_reviewed_status`

This is an indicator that a pharmacist / pharmacy resident has reviewed the sig.

Depending on the review status of the sig, it will return either unreviewed, correct, incorrect, or unknown.

`sig_reviewed`

If sig_reviewed_status is unreviewed or unknown, this will be null.
Otherwise, this will return an object containing the reviewed components of the parsed sig. See details of each component below.

NOTE: ParseRx will be constantly improving, and as such, there may be multiple different versions of parsing a given sig. Each of these parsing versions will be reviewed by a pharmacist or pharmacy resident in time. If there exists a version that has a sig_reviewed_status of correct, this is the version that will be returned. Otherwise, the most recently parsed version of the sig will be returned.

IMPORTANT: Pay close attention to the sig_reviewed_status and sig_reviewed object. It is your responsibility to use this information safely.

**Reviewed sig components**

`sig_correct`

Whether the sig is considered to be parsed correctly overall or not.

`method_status`

`dose_status`

`strength_status`

`route_status`

`frequency_status`

`duration_status`

`indication_status`

If the sig is not considered to be parsed correctly overall, there may be values in these fields representing what the specific issue(s) are.

- 0 = incorrect - ParseRx returned something for this component, but it was not correct
- 1 = missing - ParseRx did not return anything for this component, when it should have
- 2 = optimize - ParseRx returned something for this component, but it could be improved

**Inferred sig components**

`method`

`dose_unit`

`route`

This entire object will only appear if a valid ndc or rxcui are included as a request parameter. If both are included, ndc will take precedence over rxcui.

Any or all of the inferred sig components may be null if it is not possible to infer them.
