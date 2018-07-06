# list-paginated-data

Application to list paginated data in JSON format.

## Installation

After cloning, create a virtual environment and install the requirements

```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## DB Setup

MySQL database is used for the backend. After setting up mysql, follow the steps below to load the data:

1. Create a database named `esanjo_test`
2. From the command line, move to directory `db-load-scripts`
3. Run the command: `mysql -u root -p esanjo_test < categories.sql`
This command create two tables : **Users** and **categories** in the `esanjo_test` database and loads the required data into categories table

## Running the application

To run the flask server, move to the directory `src` and execute:
```
(venv) $ python3 paginate.py
 * Serving Flask app "paginate" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Then from a different terminal window you can send requests.

## API Documentation
  * POST /users
  
  Register a new user.
  The body must contain a JSON object that defines username and password fields.
  On success a status code 201 is returned. The body of the response contains a JSON object with a success message.
  On failure status code 400 (bad request) is returned.
  Note: The password is hashed before it is stored in the database. Once hashed, the original password is discarded.
  
  * GET /token
  
  Return an authentication token.
  The request must contain the username and password, using the `-u` option in curl.
  On success a JSON object is returned with a field token set to the authentication token for the user.
  On failure status code 401 (unauthorized) is returned.
  NOTE: Each token is valid for 3600 seconds
  
  * GET /categories/v1/list
  
  Return the list of category objects.
  This request must be authenticated using a auth-token header.
  The query paraters to be used for pagination are `page` and `record`
  On success a paginated list of objects is returned.
  On failure status code 401 (unauthorized) is returned.

## Example
The following curl command registers a new user with username `newuser1` and password `NewSecretPwd1`:
```
$ curl -X POST 'http://35.200.165.93:5000/users' -H 'Content-type: application/json' -d '{"username": "newuser1", "password": "NewSecretPwd1"}'
{"message":"Successfully registered"}
```
These credentials can now be used to obtain auth-token
```
$ curl -u newuser1:NewSecretPwd1 -X GET 'http://35.200.165.93:5000/token'
{"token":"eyJpYXQiOjE1MzA4NzYwNDksImV4cCI6MTUzMDg3OTY0OSwiYWxnIjoiSFMyNTYifQ.eyJ1c2VybmFtZSI6Im5ld3VzZXIxIn0.w2BYSc7zebs7YfPrZ0MEFIjrmlAxiCanGrUwcnKAhmU"}
```
Using the above token, following curl command returns a list of paginated data
```
$ curl -X GET 'http://35.200.165.93:5000/categories/v1/list?page=1&record=2' -H 'x-api-token: eyJpYXQiOjE1MzA4NzYwNDksImV4cCI6MTUzMDg3OTY0OSwiYWxnIjoiSFMyNTYifQ.eyJ1c2VybmFtZSI6Im5ld3VzZXIxIn0.w2BYSc7zebs7YfPrZ0MEFIjrmlAxiCanGrUwcnKAhmU'
{"data":[{"ids":3,"is_active":"True","level":2,"name":"Fashion right now","name_ar":"?????? ????","objectID":3,"parentID":2,"path":"/fashion-right-now","position":1,"product_count":0,"tree":"Fashion right now","tree_ar":"?????? ????"},{"ids":4,"is_active":"True","level":2,"name":"Women","name_ar":"????","objectID":4,"parentID":2,"path":"/women","position":2,"product_count":404,"tree":"Women","tree_ar":"????"}],"pagination":{"page":1,"records":"2"}}
```

## Executing test cases
The unit test cases can be found in `tests` directory. To execute them, use the command:
```
(venv) $ python3 test_paginated_data.py
```
