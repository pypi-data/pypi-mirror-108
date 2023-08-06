Copyright 2021 JonianPythonDev 



Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:



The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.



THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

=======================================================================================



This Module is very useful and easy to use! What this module does is that makes a folder\database and in database makes folders\tables that you can store data and classify all of them ! This Module is copyrighted as you can see from above and all free to use!

Here is the codes you can use to make database:

"""
#import module
from PyDatabaseModule import *

#define database location
location = r"C:\Users\Local User\Desktop\Project"

#name database
name = "Database"

# create data base
Data(name,location)

#Create table or a class Folder database 
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name in table name
CreateTableData(databaseName,databaseLocation,tableName)

#This creates data file
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name in table name
#Define msgData as the label of data table like -->("hi") = "<--"
#Define msg as value of msgData "-->" = (-->"hi"<--)
InsertDataTable(databaseName,databaseLocation,tableName,TableData)

#This writes in data files
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name in table name
WriteDataTable(databaseName,databaseLocation,tableName,TableData,msgData,msg)

#This reads the datafile
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name that you want to read in table name 
ReadDataTable(databaseName,databaseLocation,tableName,TableData)

#This deletes table data
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name that you want to read in table name
#Define Table data name.
DeleteTableData(databaseName,databaseLocation,tableName,TableData)

#This deletes table
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
#Define Table Name that you want to read in table name
DeleteTable(databaseName,databaseLocation,tableName)

#This deletes Database
# Define Database Name that you want to save table in databaseName
# Define Database location that your database is or just put "location" from above
DeleteDataBase(databaseName,databaseLocation)

"""

If you have a problem with the download code just msg me on my tiktok : JonianPythonDev
Everyone can msg me !