# Item Catalog
## Project Overview
>To develop a web-application that includes the functionality to view a list of items in particular category, where authorised and authenticated users only can add, update and delete the items they have created.

***

## Learning Outcomes
  * >Creating a RESTful web-application using the `Python3` and its `Flask` framework.
  * >Implementing `CRUD` (create, read, update and delete) functionality.
  * >Implementing third-party `OAuth authentication` eg. Google SignIn.

***

## Pre-Requisites

- >Any Linux System (Ubuntu Prefered) with:

- >`PostGreSQL` installed

- >[`Python3`](https://www.python.org/) with below given modules installed

      flask
      passlib
      httpauth
      oauth2client
      psycopg2
      requests
      sqlalchemy

***
  
## Setting up the Project

  >1. Install the necessary python modules along with `python3`.
    
  - >For installing python3 use command
    
    ```bash
    sudo apt-get install python3
    ```

  - >For installing the python3 modules use command

    ```bash
    sudo apt-get install python3-<MODULE-NAME>
    ```
    replace <MODULE-NAME> with eg. flask and repeat this till all the modules are installed

  >2. Install `PostGreSQL`.

  - >The command to install `'postgresql' is
  
    ```bash
    sudo apt-get install postgresql
    ```
  
  >3. Setting up the `PostGreSQL`.

  - >Open up psql as admin

    ```bash
    sudo -u postgres psql
    ```

  - >Create a user named 'abc' in 'psql' or 'postgresql' with superuser and login rights.
    
    ```bash
    create role abc superuser;
    ```
    ```bash
    alter role abc login;
    ```
  
  - >Add password 'cba' to the user 'abc'
    ```bash
    \password abc;
    ```
    Type `cba` + `<enter>` twice when prompted.

  - >Now exit from psql as admin using psql `\q` meta and connect as user 'abc'
    
    To quit
    ```bash
    \q
    ```
  - >To connect to 'postgres' database as user 'abc'.
    ```bash
    psql -U abc -h localhost postgres
    ```
    Type `cba` + `<enter>` when prompted.

  - >Create a database named 'mazak'.
    ```bash
    create database mazak;
    ```
  
  - >Now exit the psql using psql meta `\q`.

    ```bash
    \q
    ```
  
  >4. Now run the files to create tables and populate database.

  - `dbSetup.py` to create tables in database 'mazak'.

    ```bash
    python3 dbSetup.py
    ```

  - `dbFill.py` to populate the database created in terminal.

    ```bash
    python3 dbFill.py
    ```

***

## Running the project
  >1. Run the file `pyServer.py`
  
  ```bash
    python3 pyServer.py
  ```
  >2. Run the application by visiting url [http://localhost:8001](http://localhost:8001).

***

## References
>The credit for the code for oauth integration and the basic implementation of the project goes to the [Udacity](http://udacity.com)'s Full Stack Nanodegree Term-II coursework without whom the implementation would have been difficult.
