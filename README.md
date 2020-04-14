<h2>Welcome to the SpringBootProjectGenerator!</h2>

This program will generate a series of templated SpringBoot microservices for you, based
off of a MySQL schema.

<strong>Here is how it works:</strong><br/>

<strong>Basic premise</strong> - the basic functionality that this program offers is to create some basic
				CRUD REST microservices for each of your tables. It can generate a seperate
				service for each table, 1 service for all of the tables, or you can use a file
				called files/grouping.txt to specify groupings of tables into services. Each 
				service will also have <strong>Junit</strong> test cases created within it, and will also generate
				json file that can be imported into <strong>Postman</strong> as a collection for testing as well.

<strong>A couple of assumptions:</strong><br/>
	1. Only works with <strong>MySQL</strong> database at the moment, I use version 5.7<br/>
	2. Every table must have a primary key in it that is auto generated(auto_generated)<br/>
	3. Does not generate any foreign key functionality in the Java code<br/>

1. In a file called <strong>files/SQL_file.sql</strong>, you want to put in your MySQL definitions. These
will be table creation statements.<br/>There can be other stuff in there, but the program will only
look for the words "create table" to figure out all of your tables.
2. in a file called <strong>configuration/Configuration.py</strong> : this file really just a configuration file.
Here you will specify what you want the program to generate for you.<br/>

Some options currently available are:

<strong>use_sonar_jacoco</strong> : gives your program sonarQube analysis and jacoco code coverage functionality.

<strong>use_config_server</strong> : if you know how to use Spring cloud configuration server, this will alter your 
					services to use a config server
					
<strong>use_naming_server</strong> : if you know how to use Spring cloud naming server, this will alter your 
					services to use openFeign, Ribbon, and Eureka to use a Eureka naming server
			
more details can be found in this Configuration.py file

The main class that kicks off the program is <strong>SpringBootProjectGenerator.py</strong>

More functionality to come!

 