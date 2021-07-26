# Donation Application In Python Django
![screenshot](https://github.com/jkyalo-go/pesapal-demo/blob/master/webapp/static/webapp/donate.png)
#### Table of contents

1. [ Introduction ](#intro)
2. [ Requirements ](#req)
3. [ Installation ](#install)
4. [ Configuration ](#conf)
5. [ Usage tips. ](#usage)

## 1. Introduction

This application allows a donor to enter his name, email or phone number, amount and set a period of time for their donation as: One-off, Monthly and Annual. It uses the PesaPal live APIs to complete payments. The application has an administrative panel where an admin can login and set their PesaPal consumer key and consumer secret needed for authenticating requests.

## 2. Requirements

* Here is a list of python libraries that are project dependencies.
>asgiref

>certifi

>charset-normalizer

>Django

>idna

>pesapal

>pytz

>requests

>sqlparse

>urllib3

also included in [requirements.txt](https://github.com/jkyalo-go/pesapal-demo/blob/master/requirements.txt) in the project root directory.


## 3. Installation
* Start the installation by creating a virtual environment in your computer along with the listed requirements with `pip install <package-name>`
* Ensure you are running install commands with the virtual environment activate.

>**pip install Django**

* You may specify the python version when creating the virtual environment as follows `virtualenv -p <python-version> <virtualenv-name>`

## 4. Configuration

* Navigate to the project root folder and launch your terminal within the directory.

* Activate the virtual environment using the command `source ./<venv/bin/activate`

* Run `python manage.py makemigrations` to allow Django to propagate changes.

* In order for database and schema creation run the following command `python manage.py migrate`

* At this point you need a to create a super user on the terminal by issuing the following commands. `python manage.py craetesuperuser`. Here you will prompted to  enter an admin username, optional email and a password.

* Run the Django development server with the following command `python manage.py runserver` **Nb: Do not close this terminal as the django test server process is running in it.**

* You also need to collect static assets with `python manage.py collectstatic`

* Open your browser at [http://localhost:8000/admin](http://localhost:8000/admin) and use tha admin credentials that you just set up.

* After login set up your pesapal consumer key and  consumer secret along with email credentials needed to set up a session for the purpose of emailing users who have set to an annual or monthly billing plan.

## 5. Usage tips

* Open your browser at [http://localhost:8000](http://localhost:8000) and the application should load.

