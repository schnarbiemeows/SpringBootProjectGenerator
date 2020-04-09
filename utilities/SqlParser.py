from popos.Table import *
from utilities.Utilities import *
from utilities.FileMaker import *
from utilities.JavaFileMaker import *
from utilities.TestFileMaker import *
from popos.FieldProperties import *
import os
import sys
import xml.etree.ElementTree as ET
import shutil

"""
    this class contains utilities that parse the SQL file and extract data from it
"""
class SqlParser:

    mysqlnumberset = set(["numeric", "decimal", "integer", "bigint", "smallint", "mediumint", "float", "real", "dec", "int", "fixed", "double precision", "double", "bit"])
    mysqldatetypes = set(["date" , "datetime" , "timestamp", "time", "year"])
    mysqlstringtypes = set(["varchar" , "char" , "binary" , "varbinary" , "blob" , "text" , "enum" , "set"])

    """
        initialization
    """
    def __init__(self,tablenames,tabledata):
        self.tablenames = tablenames
        self.tabledata = tabledata

    """
        this main method will parse the SQL file and return a list of the tablenames, as well as
        the entire "create table" statement for each table
        @self.tablesnames = list of the table names
        @self.tabledata = Map("tablename" ->  "String of the entire create table statement"
    """
    def parseSqlFile(self, filelocation):
        parsetabledata = False
        tablestring = ''
        tablename = ''
        # open the file
        inputfile = open(filelocation,'r')
        # go through the file line by line
        for line in inputfile:
            linestr = str(line).strip().replace("\n","")
            #print(linestr)
            # if we are in parsing mode or are starting a new "create table" statement
            if(parsetabledata == True or linestr.find("create table")>-1):
                tablestring += linestr.rstrip() + " "
                # if this line has the "create table" words on, it, then we need to get
                # the table name from it
                if(linestr.find("create table") > -1):
                    parsetabledata = True
                    # the words "create table" will always be at the beginning of the line
                    # so we can split by "(", take the first item, then split by " "
                    # and take the last item, and this should be the table name
                    tablenametemp = linestr.split("(")[0].strip().replace("\n","").split(" ")
                    tbllen = len(tablenametemp)
                    tablename = tablenametemp[tbllen-1].strip()
                    print("adding table : " + tablename + " to the tablename list")
                    self.tablenames.append(tablename)
                # if we are at the end of a "create table statement
                if(linestr.endswith(';')):
                    # last line of a "create table" statement
                    # add tablestring to self.tabledata
                    print("adding : " + tablename + " ----> " + tablestring + " to the table data map")
                    self.tabledata[tablename] = tablestring.rstrip()
                    tablestring = ''
                    parsetabledata = False
        print("\n")
        return (self.tablenames,self.tabledata)

    """
        this method will parse the "create table" statement for a given table into a list of field names and a HashMap of
        these names as keys with FieldProperties objects as values.
        The FieldProperties objects will have the info inside then needed to create the POJO object for that table
    """
    def create_table_properties(self,table):
        utilities = Utilities()
        # some lines in our statement wont be fields
        lines_that_arenot_fields = []
        # pull out the beginning "create table" part, and remove any instances of the word "precision"
        tempsqlstring = table.createtablestring.lower()[table.createtablestring.find("create table ")+1:]
        tempsqlstring = tempsqlstring[table.createtablestring.find("("):].replace(" precision","")
        print("new create table statement is: " + tempsqlstring)
        # split the string by commas , whilst handling any commas inside quotes
        fieldarray = utilities.handleFieldsWithCommasAndParens(tempsqlstring)
        print("fieldarray length is: " + str(len(fieldarray)))
        for item in fieldarray:
            # each one of these items could be a column in the table
            itemstr = str(item).strip()
            innerarray = itemstr.split(" ")
            # if the second field is found in one of the field sets, that means this actually a column definition
            possiblefield = str(innerarray[1])
            if (possiblefield.find("(") > -1):
                possiblefield = possiblefield[0:possiblefield.find("(")]
            print("possible field is: " + str(innerarray[1]))
            if(possiblefield in SqlParser.mysqlnumberset or possiblefield in SqlParser.mysqldatetypes  or possiblefield in SqlParser.mysqlstringtypes):
                print("found field : " + innerarray[0])
                # initialize a FieldProperties object
                newfield = FieldProperties(innerarray[0].strip())
                datatypefull = innerarray[1]
                datatype = None
                datatyperest = None
                # if the data type has a length limit specified
                if(datatypefull.find("(")>-1):
                    datatype = datatypefull[0:datatypefull.find("(")]
                    datatyperest = datatypefull[datatypefull.find("(")+1:]
                    if datatype.find("varchar")>-1:
                        newfield.lengthreq = True
                        newfield.set_length(datatyperest)
                else:
                    datatype = datatypefull
                signedorno = itemstr.find("unsigned")>-1
                # translate the sql data type to java data type
                newfield.translate_datatype(datatype,signedorno)
                # figure out certain other properties of the field
                newfield.extract_field_properties(innerarray)
                if newfield.isprimary == True:
                    table.hasprimary = True
                    table.primary_name = newfield.javaname
                table.fieldnames.append(newfield.name)
                table.fielddata[newfield.name] = newfield
            else:
                # discard the line for now
                lines_that_arenot_fields.append(item)
                print("discarded line = " + item)



