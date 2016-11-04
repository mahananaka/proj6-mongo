# Proj6-mongo
This is a class project. It uses mongodb to store text memos. Memos are created using a web
forum. The webpage is created with Flask and Jinja2

## Author
Jared Paeschke, paeschke@cs.uoregon.edu

## Overview
This project has two pages the first is used to display memos. It lists them in ascending order of date. Each memo has a checkbox next to it which if selected will be deleted when the user hits the “Delete Selected” button at the top.

The second page of the Flask app allows creation of memos. When creating you must specify a date and then a message that will be stored into the database.

## Installation
When writing and testing this program, the test machine was a Raspberry Pi 3 running
Raspian Jesse. This is the best sure fire way that the install will go smoothly. 
However you should have success as long as you have bash and make on your server machine. You will also need to have MongoDB installed and setup. Setup and use of MongoDB will not be covered here, see the MongoDB documentation if you need assistance.

1. git clone https://github.com/mahananaka/proj5-mongo.git < install directory >
2. cd < install directory >
3. bash ./configure
4. You will need to create a a folder called secrets. Inside of secrets folder you will need two files
  * client_secrets.py which will need 3 lines, the quotes must be included.
    * db = “dbname”  			//this is the name of the database you created
    * db_user = “username”		//a username with readWrite access to db
    * db_user_pw = “pwd”		//pwd for db_user on db
  * admin_secrets.py which will need 3 lines, the quotes must be included.
    * port = “number”  		//port mongo is listening for connections on
	  * host = “address”		//address of mongodb, for example localhost
	  * admin_user = “username”	//optional, required to run create_db.py and destroy_db.py
	  * admin_pw = “pwd			//optional, required to run create_db.py and destroy_db.py
5. make run

The program should then sit idle and wait for page requests. The default port is
port 5000, to get the main page surf to http://yourserverip:5000/ or if you're on 
the server machine http://localhost:5000/. To stop the program at any time use ctrl+c.

## Usage
Usage is pretty self explanatory, error messages will pop up if there is an issue. It is a simple web forum otherwise

## Testing
A few test cases have been created. If you would like to run the tests yourself this can be done with the command `make test`. This will use nose to run all tests that have been written. These tests are located in the test_flask_main.py file. Write now it tests date time formatting as well as insertion, retrieval, and deletion from the database.
