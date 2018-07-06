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

