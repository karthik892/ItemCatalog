# Project: Item Catalog

In this project, Python and Flask are used to create a generic Item Ctalog. This catalog contains a list of categories and each category can contain a list of items.
Each Item can have a description and a creation date.

## Requirements
You will need to have Python 3 installed on your system. You will also need to install a number of python modules. You can use the following commands to install the required modules with PIP

```shell
pip3 install flask packaging oauth2client redis passlib flask-httpauth
pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests
```

Alternatively, you can use the accompanying vagrantfile to run the application using vagrant. (NOTE: This file was made available through the Udacity Full Stack Web Developer Nanodegree)

## Setup instructions


Run the following command to launch the flask application:

```shell
python FlaskApp.py
```

And visit the following URL in your web browser: http://localhost:5000

## Rebuilding the database

Delete ItemCatalog.db and run the following command to initialize the database and fill it with sample data:

```shell
python database.py
python SampleData.py
```

## API endpoints


The application currently provides 2 API endpoints:

### Get a list of all items


Calling ```http://localhost:5000/api/item/list``` will generate a list of all the items in the database

### Retrieving a specific item

Calling ```http://localhost:5000/api/item/<Item-name>``` (e.g. ```http://localhost:5000/api/item/Harry%20Potter%20and%20the%20Order%20of%20the%20pheonix```) will display the details for a specific item in the catalog.

## Known issues

The google login will fail if you use the URL http://127.0.0.1/ instead of localhost