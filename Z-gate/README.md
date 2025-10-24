
Create,CREATE DATABASE MyDBName;,  
"Creates a new, empty database named MyDBName."

Use,USE MyDBName;,  
Selects the newly created database as the current context for subsequent commands.

Verify,SHOW DATABASES;, 
Lists all databases on the server to confirm creation.

Example,CREATE DATABASE CompanyDB;,  
Creates a database for a company's data.


Switch,use MyNoSQLDB;,  
"Switches to the database named MyNoSQLDB. 
If it doesn't exist, MongoDB will create it implicitly upon first data insertion."

Insert,"db.employees.insertOne({ name: ""Alice"", dept: ""HR"" });",  
"This command creates the database MyNoSQLDB (if it didn't exist) and the employees collection, and inserts the first document."

Verify,show dbs or db.getName(),  
Lists all databases or shows the name of the current database.

Example,use CustomerData;, 
Switches to or creates the CustomerData database.
