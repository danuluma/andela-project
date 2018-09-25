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

## Credits



## License

MIT