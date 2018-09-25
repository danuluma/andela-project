# andela-project
[![Build Status](https://travis-ci.com/danuluma/andela-project.svg?branch=master)](https://travis-ci.com/danuluma/andela-project)   [![Coverage Status](https://coveralls.io/repos/github/danuluma/andela-project/badge.svg?branch=master)](https://coveralls.io/github/danuluma/andela-project?branch=master)

[![Maintainability](https://api.codeclimate.com/v1/badges/76222adb39c1ccdc0a94/maintainability)](https://codeclimate.com/github/danuluma/andela-project/maintainability)   [![Test Coverage](https://api.codeclimate.com/v1/badges/76222adb39c1ccdc0a94/test_coverage)](https://codeclimate.com/github/danuluma/andela-project/test_coverage)



# WIP
This is the api backend for dann's fast foods.
There are currently six working endpoints:
```GET ~/dann/api/v1/orders``` --> This endpoint retrieves a list of all the available orders
```POST ~/dann/api/v1/orders``` --> This endpoint creates a new order
```GET dann/api/v1/order/<int:order_id>``` --> This endpoint retrieves a specific order
```POST ~/dann/api/v1/order/<int:order_id>``` --> This endpoint updates a specific order
```POST ~/dann/api/v1/register``` --> This endpoint registers a new user
```POST ~/dann/api/v1/login``` --> This endpoint authenticates a new user

# How To Test
* Clone this repo to your local computer. Navigate to the project's root directory and run ```python3 run.py``` to run the app.
* Use postman to test each of the endpoints