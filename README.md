# Project: Item Catalog

In this project, Python and Flask are used to create a generic Item Ctalog. This catalog contains a list of categories and each category can contain a list of items.
Each Item can have a description and a creation date.

## Accessing the project

This project can be found at http://itemcatalog.karthiksankaran.com/
Although you can use http://99.79.36.222/ , Google oAuth will fail due to Google's security restrictions.
The SSH Port has been changed to 2200, only key-based authentication is allowed.

## List of software used

Base Operating System is Ubuntu 16.04 LTS
The following modules are installed:
apache web server (apache2)
Python 3
WSGI
postgresql

## Configuration Summary
The following configurations have been performed on the server:

* UFW has been configured to only allow connections on ports 2200 (SSH), 80 (HTTP), 123 (NTP)
* A new user 'grader' has been created with key-based SSH authentication
* 'grader' has been added to the sudoers list
* The postgres user "catalog" has been created with limited permissions for use in the ItemCatalog appication.


## Usefull resources
The following resources were helpfull in completing this project:

* Amazon Lightsail - https://signin.aws.amazon.com
* mod-wsgi Installation and Configuration - http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/
* WSGIDaemonProcess documentation - https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIDaemonProcess.html
* Creating user, database and adding access on PostgreSQL - https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
* Listing databases and tables in Postgresql - https://dba.stackexchange.com/questions/1285/how-do-i-list-all-databases-and-tables-using-psql
* Connecting Postgresql with SQLAlchemy - https://docs.sqlalchemy.org/en/latest/core/engines.html
* vi text editor usage - https://kb.iu.edu/d/adxz


## API endpoints


The application currently provides 2 API endpoints:

### Get a list of all items


Calling ```http://itemcatalog.karthiksankaran.com/api/item/list``` will generate a list of all the items in the database

### Retrieving a specific item

Calling ```http://itemcatalog.karthiksankaran.com/api/item/<Item-name>``` (e.g. ```http://itemcatalog.karthiksankaran.com/api/item/Harry%20Potter%20and%20the%20Order%20of%20the%20pheonix```) will display the details for a specific item in the catalog.
