Welcome to the SpringBootProjectGenerator!

This program will generate a series of templated SpringBoot microservices for you, based
off of a MySQL schema.

Here is how it works:

Basic premise - the basic functionality that this program offers is to create some basic
				CRUD REST microservices for each of your tables. It can generate a seperate
				service for each table, 1 service for all of the tables, or you can use a file
				called files/grouping.txt to specify groupings of tables into services. Each 
				service will also have Junit test cases created within it.

1. In a file called files/SQL_file.sql, you want to put in your MySQL definitions. These
will be table creation statements. There can be other stuff in there, but the program will only
look for the words "create table" to figure out all of your tables.
2. in a file called configuration/Configuration.py : this file really just a configuration file.
Here you will specify what you want the program to generate for you. Some options currently 
avaiable are:

use_sonar_jacoco : gives your program sonarQube analysis and jacoco code coverage functionality.

use_config_server : if you know how to use Spring cloud configuration server, this will alter your 
					services to use a config server
					
use_naming_server : if you know how to use Spring cloud naming server, this will alter your 
					services to use openFeign, Ribbon, and Eureka to use a Eureka naming server
			
more details can be found in this Configuration.py file

The main class that kicks off the program is SpringBootProjectGenerator.py

More functionality to come!

 