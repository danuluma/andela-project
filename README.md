# andela-project
[![Build Status](https://travis-ci.com/danuluma/andela-project.svg?branch=develop)](https://travis-ci.com/danuluma/andela-project)  [![Coverage Status](https://coveralls.io/repos/github/danuluma/andela-project/badge.svg?branch=ch-configure-badges-160759291)](https://coveralls.io/github/danuluma/andela-project?branch=ch-configure-badges-160759291)

[![Maintainability](https://api.codeclimate.com/v1/badges/76222adb39c1ccdc0a94/maintainability)](https://codeclimate.com/github/danuluma/andela-project/maintainability)   <!-- [![Test Coverage](https://api.codeclimate.com/v1/badges/76222adb39c1ccdc0a94/test_coverage)](https://codeclimate.com/github/danuluma/andela-project/test_coverage) -->



# WIP


# Dann's fast foods api

This is the api backend for dann's fast foods.

## Local Installation Guide

## Requirements
This project is written in python hence requires python 2 or 3 to be installed on your local environment. Download and install the latest version for your OS from https://www.python.org/downloads/

It best to install this project in a virtual environment. Please first install virtualenv package to create a virtual environment later by running
```pip install virtualenv```.

You may also install virtual environment wraper to easily work with virtual environments.
```pip install virtualenvwrapper```
For windows users, please use ```pip install virtualenvwrapper-win```


## Installation

* Clone this repo to your local computer using ```git clone https://github.com/danuluma/andela-project.git```
* Switch into the project directory ```cd andela-project```
* Create a virtual environment ```mkvirtualenv dannvenv```.
* Install the project's dependency by running ```pip install -r requirements.txt```
* Run the app locally with ```python run.py``` or ```python3 run.py```

## Usage

There are currently six working endpoints in version 1:
* ```GET ~/dann/api/v1/orders``` --> This endpoint retrieves a list of all the available orders
* ```POST ~/dann/api/v1/orders``` --> This endpoint creates a new order
* ```GET ~/dann/api/v1/order/<int:order_id>``` --> This endpoint retrieves a specific order
* ```POST ~/dann/api/v1/order/<int:order_id>``` --> This endpoint updates a specific order
* ```POST ~/dann/api/v1/reg``` --> This endpoint registers a new user
* ```POST ~/dann/api/v1/login``` --> This endpoint authenticates a new user


## Testing
* Ensure the app is running locally before testing. Start by typing ```python run.py``` or ```python3 run.py```
* To run automatic tests on the project, simply run ```python -m unittest``` or ```python3 -m unittest```
* Check on the output for the test results

You can manually test using curl or postman
* To use curl, open another terminal window and signup by sending a POST request to ```~/dann/api/v1/reg```:
~~~~
curl -X POST \
  http://localhost:5000/dann/api/v1/reg \
  -H 'Content-Type: application/json' \
  -d '{ "username": "test", "password": "test"}'
 ~~~~

* Send a POST request to ```~/dann/api/v1/login``` with the previous details in json format to log in:
```
curl -X POST \
  http://localhost:5000/dann/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "test", "password":"test"}'
  ```

You will get a json containing an access token eg.
```
{
    "message": "Logged in as Test",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzc4OTc5NjQsIm5iZiI6MTUzNzg5Nzk2NCwianRpIjoiMGQ4MmU3YTYtNzVmZC00NzRmLWEzOGItZTMwZjg2YjYzODAyIiwiZXhwIjoxNTM3ODk4ODY0LCJpZGVudGl0eSI6ImRhbiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.Dk0VRCCpt5l3qht03VLyOVksmbszdMw9mV2QIvUf33M",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzc4OTc5NjQsIm5iZiI6MTUzNzg5Nzk2NCwianRpIjoiY2Q0NzhmNDEtNzk5Yi00MDZhLThhZGMtODA4N2NkMzRlODQzIiwiZXhwIjoxNTQwNDg5OTY0LCJpZGVudGl0eSI6ImRhbiIsInR5cGUiOiJyZWZyZXNoIn0.Z09ZxpwGuYe7d-0rGkNQl1UvRFVCP5gPsnzzxKu7VhY"
}
```

You can now access protected endpoints by attachind your valid access_token to the request's header with the format of ```'Authorization: Bearer <access_token>'```
Please note there's a space between "Bearer" and "access_token"
```
curl -X GET \
  http://localhost:5000/dann/api/v1/home \
  -H 'Authorization: Bearer <your access_token here>' \
  -H 'Content-Type: application/json' \
  ```
Alternatively, you may use postman or any other gui tool for testing apis
If using postman, please Bearer Token as the authorization type and insert the acess_token as the token

![Postman example](https://res.cloudinary.com/danuluma/image/upload/v1537900187/postmanex.png)
![Postman example](https://res.cloudinary.com/danuluma/image/upload/v1537900242/postmanex2.png)

## Credits



## License

MIT