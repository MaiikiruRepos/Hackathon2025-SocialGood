# KSU: 2025 Hackathon for Social Good
Everything was built in 40~ hours.

# EcoPulse: A away for any company to get a quick pulse on their unseen carbon emissions and water usage.

## Overview: 
EcoPulse: A away for any company to get a quick pulse on their unseen carbon emissions and water usage.

User flow:
A company uploads a standard BOM containng:  
    - Plant – Identifier for the plant location.  
    - PlantSKUQuantity – Quantity of SKUs produced at the plant.  
    - Process – Name of the process used.  
    - ProcessDefinition – Description or definition of the process.  
    - Sku – Unique identifier for the product SKU.  
    - SkuBom – Bill of materials associated with each SKU.  
    - SkuProcess – Process steps linked to each SKU.  
    - Link – Relationships as defined in the latest ER diagram.  
This information is then processed to solve for unseen carbon emissions and water usage.

A large portion of this project was researching the 'unseen values'.

For example, a KWH of electricity can be valued differently depending on where you are in the world.  
This all depends on how the region you are in makes electricity: Coal? Natural Gas? Solar?

Pulling from various sources such as a few IEEE articles and Government resources we can curently assign 'unseen values' for:
 - Diesel (Gal)
 - Electricity (KWH)
 - Gasoline (Gal)

Taking the ammout of each resource used and depending on where in the globe the source is used we then can generate statistics for the user.

This information can be easily seen in the 'Dashboard' Page on the Web App.

# Documentation: 

## A Quick prelude on Notation:
I will put the shell type before the command.<br>
So if you see \$ before a command, that means it will run on a normal user shell. <br>
I will use ## to denote the fact that the following line is a comment.

So if I say `$ echo Hello World`, I mean ran echo Hello World in a normal shell.


<b>The following instructions will assume that you are at the root of the project repo.</b>
## Backend Instructions:
Assuming that you are on the root of this repo:

### Create an .env file to store secrets
----
You will need to create a .env file at `/backend/.env`
<br> This file needs to be in the following form:
```angular2html
MYSQL_ROOT_PASSWORD="SECRET_HERE"
MYSQL_USER="devuser"
MYSQL_PASSWORD="SECRET_HERE"
MYSQL_DATABASE="mydatabase"
DB_HOST='DB_HOST_HERE'
```

### Run the database using Docker:
You will need to first install docker: You can find installation information here:
 <ul>
  <li><a href="https://docs.docker.com/desktop/setup/install/windows-install/">Windows</a></li>
  <li><a href="https://docs.docker.com/desktop/setup/install/mac-install/">MacOS</a></li>
  <li><a href="https://docs.docker.com/engine/install/">Linux</a></li>
</ul> 

After you have installed docker, run the following command:

`docker compose up -d`

Optionally, you can test that docker is working by going into the container:
<br>

```
## This will put you into the bash shell inside the docker container.
$ docker exec -it hackathon2025-socialgood-mysql-1 /bin/bash

## This will prompt you for the root password of the mysql.
bash-5.1# mysql -p

## Now that you're in the mysql shell, you can show databases.
mysql> SHOW DATABASES;
## Here is a sample output
##+--------------------+
##| Database           |
##+--------------------+
##| information_schema |
##| mydatabase         |
##| mysql              |
##| performance_schema |
##| sys                |
##+--------------------+

mysql> USE mydatabase;
mysql> LIST TABLES;

## Here is a sample output:
##+----------------------+
##| Tables_in_mydatabase |
##+----------------------+
##| EnvTable             |
##| Item                 |
##| ItemProcess          |
##| OverallScore         |
##| PieChartData         |
##| Plant                |
##| PlantSKUQuantity     |
##| Processes            |
##| SkuScore             |
##+----------------------+

## From here, you can do your normal SQL commands e.g.
mysql> SELECT * FROM Plant;
```

### Run the FastAPI Locally:
Once you have confirmed that the MySQL database is running locally, you may run the FastAPI locally by using the following commands:
<br>
If you have not already created a virtual environment and downloaded all dependencies:
```
$ python -mvenv .venv
## On Linux or MacOS:
$ source .venv/bin/activate
## On Windows:
$ venv\Scripts\activate
python -m pip install -r requirements.txt
```
Once you are sure you have all the dependencies, run the following:

`$ fastapi dev backend/Codebase/API/main.py`

You may access the OpenAPI documentation/test interface by going to: <br>
[http://localhost:8000/docs](http://localhost:8000/docs)

## Frontend Instructions
`cd frontend/hack-2025 && npm run dev`

## Documentation:
### ER Diagram:
![ER Diagram](Documentation/ERDiagram.png)

