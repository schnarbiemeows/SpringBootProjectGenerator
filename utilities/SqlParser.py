from popos.Table import *
from popos.View import View
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
    mysqlstringtypes = set(["varchar" , "char" , "binary" , "varbinary" , "tinyblob", "blob" , "text" , "enum" , "set"])
    mysqlboolean = set(["boolean"])
    pound_sign = "#"
    semi_quote = ";"
    sq_repl = "@!&"
    comma_repl = "&!@"
    tick_repl = "^%+"
    tick_space_repl = "~|*"
    dash_dash = "--"
    backtick = "`"
    dblquote = "\""
    singlquote = "'"
    comment = "comment"

    def __init__(self,tablenames,tabledata):
        """
        initialization
        :param tablenames:
        :param tabledata:
        """
        self.tablenames = tablenames
        self.tabledata = tabledata

    def processSQL(self, filelocation):
        """
        this master method calls other methods to
        passOne - just read in the text file into an array
        passTwo - mapper/reducer method to count
        :param fullfilename:
        :return:
        """
        inputfile = open(filelocation,"r")

        cleanedSql = self.removeComments(inputfile)  # read in the file to a single string and lowercase it
        sqlCommandList = self.joinAndResplit(cleanedSql)  # join and then resplit by ";" - each line is a separate SQL command

        # filter out everything other than any "create table" and "alter table" statements into separate lists
        createTableList = list(filter(lambda x: self.filterStringByLambda(x,"create table",True),sqlCommandList))
        possiblePrimaryKeyList = list(filter(lambda x: self.filterStringByLambda(x, "primary key", False), sqlCommandList))
        possibleForeignKeyList = list(filter(lambda x: self.filterStringByLambda(x, "foreign key", False), sqlCommandList))
        possibleUniqueKeyList = list(filter(lambda x: self.filterStringByLambda(x, "unique", False), sqlCommandList))
        possibleUniqueDropList = list(filter(lambda x: self.filterStringByLambda(x, "drop index", False), sqlCommandList))
        self.tablenames, self.tabledata = self.parseCreateCommandsToExtractTableData(createTableList)
        for table in self.tablenames:
            currenttable = Table(table, self.tabledata[table])
            self.tabledata[table] = self.getFields(currenttable)
        primaryKeysList = list(map(lambda x: self.parseOutPrimaryKeyByLambda(x), possiblePrimaryKeyList))
        foreignKeysList = []
        uniqueKeysList = []
        for line in possibleForeignKeyList:
            tempForeignKeysList = self.parseOutForeignKeys(line)
            for item in tempForeignKeysList:
                foreignKeysList.append(item)
        for line in possibleUniqueKeyList:
            tempUniqueKeysList = self.parseOutUniqueKeys(line)
            for item in tempUniqueKeysList:
                uniqueKeysList.append(item)
        uniqueKeyDrops = list(map(lambda x: self.parseOutUniqueDropsByLambda(x), possibleUniqueDropList))
        primaryKeysList = self.reconcilePrimaryKeys(self.tabledata,primaryKeysList)
        uniqueKeysList = self.reconcileUniqueKeys(self.tabledata, uniqueKeysList)
        uniqueKeyDrops = self.reconcileUniqueDrops(self.tabledata, uniqueKeysList, uniqueKeyDrops)
        foreignKeysList = self.reconcileForeignKeys(self.tabledata,foreignKeysList)
        self.applyPrimaryKeysToTables(self.tabledata,primaryKeysList)
        self.applyForeignKeysToTables(self.tabledata,foreignKeysList)
        self.applyUniqueKeysToTables(self.tabledata, uniqueKeysList, uniqueKeyDrops)
        inputfile.close()
        return (self.tablenames,self.tabledata)

    def removeComments(self, inputfile):
        """
                                            REMOVE COMMENTS METHOD
        2 types of comments:
        1. user comments - 2 types of these:
            1. end of line comments - start with # or --
            2. inline comments - surrounded by /* ... */
        2. field comments: we do NOT want to remove these
            surrounded by either single quotes or double quotes
        Both the inline comments and the field comments can wrap around mutliple lines
        so, we need to track of both of these scenarios:
        3 scenarios:
        1. inside_comment - disregard anything inside these
        2. inside_quote - retain anything inside these, but convert any ";" and "," into "@!&" and "&!@"
                            because later, we will resplit according to these symbols and then later convert back
        3. neither of these scenarios
        :param inputfile:
        :return:
        """
        outputlist = []
        inside_comment = False  # are we currently inside a pair of /* ... */?
        multiline_comment = False
        inside_quote = False  # are we inbetween quotes?
        quote_char = ""  # are we in between "" or ''?
        for line in inputfile:
            prepender = ""
            linestr = str(line)
            previous_char = ""
            for c in linestr:
                if inside_comment == True:
                    if c == "/" and previous_char == "*":
                        inside_comment = False
                        if multiline_comment == False:
                            prepender = prepender[0:-1]  # gotta remember to remove the initial "/"
                        multiline_comment = False
                        previous_char = ""  # reset previous char, may not need this
                    else:
                        previous_char = c
                elif inside_quote == True:
                    if c == quote_char and previous_char != "\\":
                        # TODO - this does not handle the case where the " may be prepended by an even # of \
                        # but the risk is low enough that I will worry about this later
                        inside_quote = False
                        quote_char = ""
                        prepender += c
                    elif c == ";":
                        prepender += SqlParser.sq_repl
                        previous_char = ""
                    elif c == ",":
                        prepender += SqlParser.comma_repl
                        previous_char = ""
                    elif c == "`":
                        prepender += SqlParser.tick_repl
                        previous_char = ""
                    else:
                        prepender += c
                        previous_char = c
                else:
                    if c == "#" or c == "-" and previous_char == "-":
                        if c == "-":
                            prepender = prepender[0:-1] + "\n"
                        break
                    elif c == "*" and previous_char == "/":
                        inside_comment = True
                        previous_char = ""
                    elif c == "'" or c == "\"":
                        inside_quote = True
                        prepender += c
                        previous_char = c
                        quote_char = c
                    else:
                        prepender += c
                        previous_char = c
            if inside_comment == True:
                prepender = prepender[0:-1]
                multiline_comment = True
            outputlist.append(prepender.strip())
        return outputlist

    def joinAndResplit(self, inputfile):
        """
        read the entire file into 1 string
        remove extra whitespace
        remove leading and trailing whitespaces after rejoining
        replace any spaces that occur between backticks:
        split by "`" - there should ALWAYS be an ODD number of items; 1 item if there are no backticks
        for the odd # items, replace " " with "~|*"
        :param inputfile:
        :return:
        """
        inputfilestring = " ".join(inputfile)
        ticklist = inputfilestring.split("`")
        for i in range(0, len(ticklist)):
            if i % 2 != 0:
                ticklist[i] = str(ticklist[i]).strip().replace(" ", SqlParser.tick_space_repl)
        inputfilestring = "`".join(ticklist)
        outputfile = inputfilestring.split(";")
        for i in range(0, len(outputfile)):
            outputfile[i] = str(outputfile[i]).strip()
        return outputfile

    def filterStringByLambda(self, input, predicate, startsWith):
        if startsWith == True:
            if input.lower().startswith(predicate):
                return True
            else:
                return False
        else:
            if input.lower().find(predicate) > -1:
                return True
            else:
                return False

    def parseOutPrimaryKeyByLambda(self, input):
        """
        this method will return a tuple list item of (<table name>,<primary key field name list>)
        if "drop primary key" is encountered, add the word "drop" to the list, later when we find it,
        we will clear the Table primary key list(self.primarykeys = [])
        :param input:
        :return:
        """
        primarykeynameList = []
        tablename = self.getTableName(input)
        """
            complicated algorithm:
            if this line is an "alter table" statement, then there are 2 possibilities:
            - if the first non-whitespace character after the words "primary key" == "(" , then
                the primary key field name(s) will be between this "(" and the next ")"
              else --> we have a "drop primary key" statement, so return "drop"
            if this is a "create table" statement, then we need to:
            - get the index of the words "primary key" (there can only be 1 of these)
            - get the index of the first ","
            - for this item:
                substring everything after the words "primary key", and lstrip()
                if the first non-whitespace character of this substring == "(" , then
                    the primary key field name(s) will be between this "(" and the next ")"
                else:
                if the index of the "," > the index of "primary key", that means the table's first field is the primary key, which we get by:
                    - split by "(", take the 2nd item and .strip()
                    - split that item by " ", take the first item
                    - ex.: "create table child_3(child_id mediumint not null auto_increment primary key," -> child_id
                else --> just split by " ", take the first item and strip()         
        """
        fieldnames = []
        if input.lower().find("alter table") > -1:
            substring = input[input.lower().find("primary key") + 11:].strip()
            if substring[0:1] == "(":
                fieldnames = substring[1:substring.find(")")].strip().split(",")
                for i in range(0, len(fieldnames)):
                    fieldnames[i] = fieldnames[i].strip()
            else:
                fieldnames = ["drop"]
        elif input.lower().find("create table") > -1:
            commaindex = input.find(",")
            pkindex = input.lower().find("primary key")
            wordsafterpk = input[input.lower().find("primary key") + 11:].lstrip()
            if wordsafterpk[0:1] == "(":
                # only instance of where a compound PK could occur, and where the field name is after the words "primary key"
                fieldnames = wordsafterpk.split(")")[0].replace("(", "").split(",")
            elif commaindex > pkindex:
                # the primary key is the first field
                fieldnames.append(input.split("(")[1].strip().split(" ")[0].strip())
            else:
                # the primary key is a later field but can't be compound, so we can split by comma
                temparray = input.split(",")
                for item in temparray:
                    if item.lower().find("primary key") > -1:
                        fieldnames.append(item.strip().split(" ")[0].strip())
        print("returning primary keys for table: " + tablename)
        for i in range(0, len(fieldnames)):
            fieldnames[i] = fieldnames[i].strip()
        for item in fieldnames:
            print("pk = " + item)
        return (tablename, fieldnames)

    def parseCreateCommandsToExtractTableData(self, sqlCreateStatements):
        """
        this main method will parse the SQL file and return a list of the tablenames, as well as
            the entire "create table" statement for each table
            @self.tablesnames = list of the table names
            @self.tabledata = Map("tablename" ->  "String of the entire create table statement"
        :param sqlCreateStatements:
        :return:
        """
        tablenames = []
        tabledata = {}
        tablestring = ''
        tablename = ''
        for line in sqlCreateStatements:
            linestr = str(line).strip().replace("\n", "")
            tablestring += linestr.rstrip() + " "
            # the words "create table" will always be at the beginning of the line
            # so we can split by "(", take the first item, then split by " "
            # and take the last item, and this should be the table name
            # tables may be surrounded with backticks(`), in which case we need to retain these
            tablename = self.getCreateTableTableName(linestr)
            # print("adding table : " + tablename + " to the tablename list")
            tablenames.append(tablename)
            # add tablestring to self.tabledata
            # print("adding : " + tablename + " ----> " + tablestring + " to the table data map")
            tabledata[tablename] = tablestring.rstrip()
            tablestring = ''
        # print("\n")
        return tablenames, tabledata

    def getFields(self, table):
        """
        this method will parse the "create table" statement for a given table into a list of field names and a HashMap of
        these names as keys with FieldProperties objects as values.
        The FieldProperties objects will have the info inside then needed to create the POJO object for that table
        :param table:
        :return:
        """
        utilities = Utilities()
        # some lines in our statement wont be fields
        lines_that_arenot_fields = []
        # pull out the beginning "create table" part, and remove any instances of the word "precision"
        tempsqlstring = table.createtablestring[table.createtablestring.lower().find("create table ") + 1:]
        tempsqlstring = tempsqlstring[table.createtablestring.find("("):]\
            .replace(" precision", "")\
            .replace(" PRECISION", "")\
            .replace(" Precision", "")
        # print("new create table statement is: " + tempsqlstring)
        # split the string by commas , whilst handling any commas inside quotes
        fieldarray = utilities.handleFieldsWithCommasAndParens(tempsqlstring)

        # problem with foreign keys here if they are compound keys

        # print("at field array")
        for item in fieldarray:
            # each one of these items could be a column in the table
            itemstr = str(item).strip()
            # print("item string --->: " + itemstr)
            innerarray = itemstr.replace("\t"," ").split(" ")
            if (len(innerarray) > 1):
                # if the second field is found in one of the field sets, that means this actually a column definition
                possiblefield = str(innerarray[1])
                if (possiblefield.find("(") > -1):
                    possiblefield = possiblefield[0:possiblefield.find("(")]
                # print("possible field is: " + str(innerarray[1]))
                if (possiblefield.lower() in SqlParser.mysqlnumberset or possiblefield.lower() in SqlParser.mysqldatetypes or
                        possiblefield.lower() in SqlParser.mysqlstringtypes or possiblefield.lower() in SqlParser.mysqlboolean):
                    print("found field : " + innerarray[0])
                    # initialize a FieldProperties object
                    newfield = FieldProperties(innerarray[0].strip())
                    datatypefull = innerarray[1]
                    datatype = None
                    datatyperest = None
                    # if the data type has a length limit specified
                    if (datatypefull.find("(") > -1):
                        datatype = datatypefull[0:datatypefull.find("(")]
                        datatyperest = datatypefull[datatypefull.find("(") + 1:]
                        if datatype.lower().find("varchar") > -1:
                            newfield.lengthreq = True
                            newfield.set_length(datatyperest)
                        elif datatype.lower().find("decimal") > -1:
                            numarr = datatyperest[0:datatyperest.find(")")].split("ZYX")
                            newfield.set_length(numarr[0])
                            if len(numarr)>1:
                                newfield.decimals =  int(numarr[1])

                    else:
                        datatype = datatypefull.lower()
                    signedorno = itemstr.lower().find("unsigned") > -1
                    # figure out certain other properties of the field
                    newfield.extract_field_properties(innerarray)
                    # translate the sql data type to java data type
                    newfield.translate_datatype(datatype.lower(), signedorno)


                    table.fieldnames.append(newfield.name)
                    table.fielddata[newfield.name] = newfield
                else:
                    # discard the line for now
                    lines_that_arenot_fields.append(item)
                    # print("discarded line = " + item)
            else:
                # discard the line for now
                lines_that_arenot_fields.append(item)
                # print("discarded line = " + item)
        return table

    def parseOutForeignKeys(self, input):
        """
        this method will add entries into foreignKeyMap: (<table name> -> <primary key field name list>)
        :param input:
        :return:
        """
        """
            complicated algorithm:
    #1:     if this line is an "alter table" statement: 
    ex.: add constraint fkchild34 foreign key noway (`fkchild3`,`fkchild4`) references `fkparent`(`fkparent4`,`fkparent5`)
            the optional words in this statement above are: "constraint" "fkchild34" "noway"
            "noway" actually has NO meaning, but could be there!

            - split the line by the words "foreign key" into beforefk and afterfk
            1. beforefk:
                remove the words: "alter","table","add","constraint",<tablename> -> 
                whats left could be : drop,<symbol>, or neither of these 
                if "drop" can be found, it's a drop 
                if <symbol> then 
            - pick afterfk. 
                - if it is a drop, then the first word is the <symbol> to drop, split by " "
                    and take the 1st item and .strip()
                    return : (tablename,"drop",<symbol>,null,null)
                - if it is not a drop, then take everything after the first "(" as a substring,
                    strip() the item, split by ")", take the 1st item, finally split by "," and strip
                    the get a list of fieldnames

                    then:
                    - take the substring and split by "references", take the 2nd item
                    - take everything before the first "(" and strip, this is the parent tablename
                    - take everything after the "(" , strip(), split by ")", strip(), finally 
                      split by "," and strip() the get a list of parentfieldnames

    #2      if this is a "create table" statement:
                - while there is still an instance of "foreign key" to be found:
                for each "foreign key" that we find:
                - substring to take everything after the word "foreign key"
                - fieldnames = split(")").replace("(","").strip().split(",").strip()
                - take everything after the word "references" and lstrip()
                - tablename = substring.split("(")[0].strip()
                - parentfieldnames = substring.split(")")[1].replace("(","").strip().split(",").strip()
            return (tablename,fieldname[],symbolname,parenttablename,parentfieldname[])
        """
        symbolname = ''
        drop = False
        fieldname = []
        symbolname = ''
        tablename = self.getTableName(input)
        parenttablename = ''
        parentfieldname = []
        totalforeignkeys = []
        if input.lower().find("alter table") > -1:
            beforefk = input[0:self.findIndexOfGivenPhrase(input,"foreign key")]
            afterfk = input[self.findIndexOfGivenPhrase(input,"foreign key")+11:]
            # beforefk
            words = ["alter","table","add","constraint"]
            beforefk = self.replaceBunchOfWords(beforefk,words)\
                .replace(tablename, "")
            if beforefk.lower().find("drop") > -1:
                fieldname.append("drop")
                drop = True
            else:
                symbolname = beforefk.strip()
            # afterfk
            if drop == True:
                symbolname = afterfk.replace(";", "").strip()
                totalforeignkeys.append((tablename, fieldname, symbolname, parenttablename, [""]))

            else:
                fieldname = afterfk.split("(")[1].strip().split(")")[0].split(",")
                if symbolname == '':
                    symbolname = fieldname[0]
                for i in range(0, len(fieldname)):
                    fieldname[i] = fieldname[i].strip()
                referencesindex = afterfk.lower().find("references")+10
                parenttablename = afterfk[referencesindex:].split("(")[0].strip()
                parentfieldname = afterfk[referencesindex:].split("(")[1].strip().split(")")[0].split(",")
                for i in range(0, len(parentfieldname)):
                    parentfieldname[i] = parentfieldname[i].strip()
                totalforeignkeys.append((tablename, fieldname, symbolname, parenttablename, parentfieldname))

        else:
            while input.lower().find("foreign key") > -1:
                input = input[input.lower().find("foreign key") + 11:]
                symbolname = input.split("(")[0].strip()  # if there is a symbol
                fieldname = input.split("(")[1].strip().split(")")[0].split(",")
                for i in range(0, len(fieldname)):
                    fieldname[i] = fieldname[i].strip()
                if symbolname == '':
                    symbolname = fieldname[0]
                referencesindex = input.lower().find("references") + 10
                substring = input[referencesindex:]
                parenttablename = substring.split("(")[0].strip()
                parentfieldname = substring.split("(")[1].split(")")[0].strip().split(",")
                for i in range(0, len(parentfieldname)):
                    parentfieldname[i] = parentfieldname[i].strip()
                totalforeignkeys.append((tablename, fieldname, symbolname, parenttablename, parentfieldname))

        print("returning foreign keys for table: " + tablename)
        for i in range(0, len(totalforeignkeys[0][1])):
            print("table: " + totalforeignkeys[0][0] + " , fk name: " + totalforeignkeys[0][1][i] + " , symbol = " +
                  totalforeignkeys[0][2] +
                  " , parent table: " + totalforeignkeys[0][3] + " , parent key: " + totalforeignkeys[0][4][i])

        return totalforeignkeys

    def findIndexOfGivenPhrase(self, input, word):
        """
        this method is needed to find the location of a given phrase, like foreign key or primary key
        :param input:
        :return:
        """
        return input.lower().find(word)

    def replaceBunchOfWords(self,input,words):
        """
        this method will remove all possible cases of a list of words from a given input string
        :param input:
        :param words:
        :return:
        """
        for i in words:
            first = i[0].upper()
            rest = i[1:]
            camelcase = first+rest.lower()
            input = input.replace(i.upper,"").replace(i.lower(),"").replace(camelcase,"")
        return input

    def parseOutUniqueKeys(self, input):
        """
        this method will search for the word "unique" to locate any unique keys
        TODO - if the word unique is in a comment, this will cause an error
        :param input:
        :return:
        """
        totaluniquekeys = []
        tablename = self.getTableName(input)
        if input.lower().find("alter table") > -1:
            # [0:self.findIndexOfGivenPhrase(input,"foreign key")]
            beforeuk = input[0:self.findIndexOfGivenPhrase(input,"unique")]
            afteruk = input[self.findIndexOfGivenPhrase(input,"unique")+6:]
            # beforeuk
            words = ["alter", "table", "add", "constraint"]
            beforeuk = self.replaceBunchOfWords(beforeuk, words) \
                .replace(tablename, "")
            symbolname = beforeuk.strip()
            # afteruk
            fieldnames = afteruk.split("(")[1].strip().split(")")[0].split(",")
            if symbolname == '':
                symbolname = "".join(fieldnames)
            for i in range(0, len(fieldnames)):
                fieldnames[i] = fieldnames[i].strip()
            totaluniquekeys.append((tablename, fieldnames, symbolname))
        elif input.lower().find("create table") > -1:
            while input.lower().find("unique") > -1:
                fieldnames = []
                symbolname = ''
                # we have to first find any comma right before the next instance of "unique"
                commaindex = input.find(",")
                ukindex = input.lower().find("unique")
                while commaindex > -1 and commaindex < ukindex:
                    input = input[input.find(",") + 1:]
                    commaindex = input.find(",")
                    ukindex = input.lower().find("unique")
                # at this point, we have to figure out
                wordsbeforeuk = input[0:input.lower().find("unique")].strip()
                wordsafteruk = input.replace("UNIQUE KEY","UNIQUE")\
                    .replace("unique key","unique")\
                    .replace("UNIQUE key","UNIQUE")\
                    .replace("unique KEY","unique")[input.lower().find("unique") + 6:].lstrip()
                if wordsafteruk[0:1] == "(":
                    # scenarios 2 and 3
                    fieldnames = wordsafteruk.split(")")[0].replace("(", "").split(",")
                    for i in range(0, len(fieldnames)):
                        fieldnames[i] = fieldnames[i].strip()
                    symbolname = "".join(fieldnames)
                    if wordsbeforeuk.lower().find("constraint") > -1:
                        tempsymbolname = wordsbeforeuk[wordsbeforeuk.lower().find("constraint") + 10:].strip()
                        if len(tempsymbolname)>0:
                            symbolname = tempsymbolname
                else:
                    # the unique key is the first word in wordsbeforeuk
                    fieldnames.append(wordsbeforeuk.split(" ")[0].strip())
                    symbolname = fieldnames[0]
                totaluniquekeys.append((tablename, fieldnames, symbolname))
                input = input[input.lower().find("unique") + 6:]
        return totaluniquekeys

    def parseOutUniqueDropsByLambda(self, input):
        """
        this method is very simple because the input only contains lines that le <tablename> drop index <index name>
        :param input:
        :return:
        """
        tablename = self.getTableName(input)
        indexname = input[input.lower().find("index")+5:].strip()
        return tablename, indexname

    def getTableName(self, input):
        if input.lower().find("create table") > -1:
            tablename = self.getCreateTableTableName(input)
        elif input.lower().find("alter table") > -1:
            if input.find("`") > -1:
                tablename = "`" + input.split("`")[1].strip() + "`"
            else:
                tablename = input.split(" ")[2].strip()
        return tablename

    def getCreateTableTableName(self, linestr):
        tablename = ''
        createstatement = linestr[linestr.find("("):]
        tablenametemp = linestr.split("(")[0].strip().replace("\n", "")
        if tablenametemp.find("`") > -1:
            tablename = "`" + tablenametemp.split("`")[1].strip() + "`"
        else:
            tablenametemp = linestr.split("(")[0].strip().replace("\n", "").split(" ")
            tbllen = len(tablenametemp)
            tablename = tablenametemp[tbllen - 1].strip()
        return tablename

    def reconcilePrimaryKeys(self, tabledata, primaryKeysList):
        """
        because primary key definitions are not case sensitive, we need to check
        each primary key field name against all of the fields in the table, and adjust it
        if needed
        :param tabledata:
        :param primaryKeysList:
        :return:
        """
        newPrimaryKeysList = []
        for primakry_key_definition in primaryKeysList:
            tablename = primakry_key_definition[0]
            keys = primakry_key_definition[1]   # this is a list
            if len(keys)==1 and keys[0] == "drop":
                newPrimaryKeysList.append((tablename,keys))
            else:
                # what we have to do here is compare each key name to each fieldname and when we
                # find a match, replace the keyname with the fieldname
                newkeys = []
                for key in keys:
                    for fieldname in tabledata[tablename].fieldnames:
                        if fieldname.lower() == key.lower():
                            newkeys.append(fieldname)
                            break
                newPrimaryKeysList.append((tablename, newkeys))
        return newPrimaryKeysList

    def reconcileUniqueKeys(self, tabledata, uniqueKeysList):
        """
        because unique key definitions are not case sensitive, we need to check
        each unique key field name against all of the fields in the table, and adjust it
        if needed
        :param tabledata:
        :param uniqueKeysList:
        :return:
        """
        # totaluniquekeys.append((tablename, fieldnames, symbolname))
        newUniqueKeyList = []
        for newUniqueKey in uniqueKeysList:
            tablename = newUniqueKey[0]
            fieldKeyname = newUniqueKey[1]
            symbolname = newUniqueKey[2]
            newFieldKeyNames = []
            for uniqueKeyFieldName in fieldKeyname:
                for fieldname in tabledata[tablename].fieldnames:
                    if fieldname.lower() == uniqueKeyFieldName.lower():
                        uniqueKeyFieldName = fieldname
                        newFieldKeyNames.append(uniqueKeyFieldName)
            newUniqueKeyList.append((tablename, newFieldKeyNames, symbolname))
        return newUniqueKeyList


    def reconcileUniqueDrops(self, tabledata, uniqueKeysList, uniqueKeyDrops):
        """
        because unique drops definitions are not case sensitive, we need to check
        each symbolname against all of the symbolnames in the uniqueKeysList, and adjust it
        if needed
        :param tabledata:
        :param uniqueKeysList:
        :param uniqueKeyDrops:
        :return:
        """
        # drops are : return tablename, indexname
        # keys are : totaluniquekeys.append((tablename, fieldnames, symbolname))
        newUniqueKeyDrops = []
        for unique_drop_definition in uniqueKeyDrops:
            tablename = unique_drop_definition[0]
            symbolname = unique_drop_definition[1]
            for key in uniqueKeysList:
                keysymbolname = key[2]
                if keysymbolname.lower() == symbolname.lower():
                    symbolname = keysymbolname
                    break
            newUniqueKeyDrops.append((tablename,symbolname))
        return newUniqueKeyDrops

    def reconcileForeignKeys(self, tabledata, foreignKeysList):
        """
        because foreign key definitions are not case sensitive, we need to:
        1. check the child field name against the field names in the child table,
        and adjust it if needed
        2. check the parent field name against the field names in the parent table,
        and adjust it if needed
        :param tabledata:
        :param foreignKeysList:
        :return:
        """
        # totalforeignkeys.append((tablename, fieldname, symbolname, parenttablename, parentfieldname))
        newForeignKeysList = []
        for foreignKeyDefinition in foreignKeysList:
            childtable = foreignKeyDefinition[0]
            childfields = foreignKeyDefinition[1]    # a list of fields
            symbolname = foreignKeyDefinition[2]
            parenttable = foreignKeyDefinition[3]
            parentfields = foreignKeyDefinition[4]   # a list of fields
            newchildfieldlist = []
            newparentfieldlist = []
            for childfield in childfields:
                for fieldname in tabledata[childtable].fieldnames:
                    if fieldname.lower() == childfield.lower():
                        newchildfieldlist.append(fieldname)
                        break
            for parentfield in parentfields:
                for fieldname in tabledata[parenttable].fieldnames:
                    if fieldname.lower() == parentfield.lower():
                        newparentfieldlist.append(fieldname)
                        break
            newForeignKeysList.append((childtable,newchildfieldlist,symbolname,parenttable,newparentfieldlist))
        return newForeignKeysList

    def applyPrimaryKeysToTables(self, tabledata, primaryKeysList):
        """
        iterate through all of the items in the primaryKeysList, and apply this information to
        the data in the tabledata
        :param tabledata:
        :param primaryKeysList:
        :return:
        """
        pkfields = {}  # Map[ tablename -> List[field]
        pkcounts = {}  # Map[ tablename -> count ]
        for item in primaryKeysList:
            if item[1][0].lower() != "drop":
                tablename = item[0]
                pknamelist = item[1]
                if tablename not in pkfields:
                    pkfields[tablename] = []
                    pkcounts[tablename] = 0
                pkcounts[tablename] += 1
                pkfields[tablename] = pknamelist
        for item in primaryKeysList:
            if item[1][0] == "drop":
                tablename = item[0]
                pkcounts[tablename] -= 1
        for table in pkcounts.keys():
            if pkcounts[table] > 0:
                tabledata[table].hasprimary = True
                tabledata[table].primarykeys = pkfields[table]
                for item in pkfields[table]:
                    tabledata[table].fielddata[item].isprimary = True
                    tabledata[table].fielddata[item].unique = True
        print("DONE adding Primary Key Information")

    def applyForeignKeysToTables(self, tabledata, foreignKeysList):
        """
        iterate through all of the items in the foreignKeysList, and apply this information to
        the data in the tabledata
        :param tabledata:   Map[ tablename -> Table Object ]
        :param foreignKeysList: List[ Tuple(String,List[String],String,String,List[String] ],
                    Tuple is: (tablename,fieldname,symbolname,parenttablename,parentfieldname)
        :return:
        """
        symboldata = {}  # Map[ tablename -> Map[ symbol : List[(field,table,field)]]
        symbolcounts = {}  # Map[ tablename -> Map[ symbol : count ]]
        for item in foreignKeysList:
            if item[1][0].lower() != "drop":
                tablename = item[0]
                fknamelist = item[1]
                symbol = item[2]
                parenttable = item[3]
                parentkeyList = item[4]
                if tablename not in symboldata:
                    symboldata[tablename] = {}
                    symbolcounts[tablename] = {}
                if symbol not in symboldata[tablename]:
                    symboldata[tablename][symbol] = []
                    symbolcounts[tablename][symbol] = 0
                # clear anything that may have been there before for that (table,symbol)
                symboldata[tablename][symbol] = []
                for i in range(0, len(fknamelist)):
                    field = fknamelist[i]
                    parentfield = parentkeyList[i]
                    symboldata[tablename][symbol].append((field, parenttable, parentfield))
                symbolcounts[tablename][symbol] += 1
        for item in foreignKeysList:
            if item[1][0].lower() == "drop":
                symbol = item[2]
                symbolcounts[tablename][symbol] -= 1
        for table in symbolcounts.keys():
            for symbol in symbolcounts[table].keys():
                if symbolcounts[table][symbol] > 0:
                    tabledata[table].fksymbolnames.append(symbol)
                    tabledata[table].fksymboldata[symbol] = []
                    count = 0
                    for item in symboldata[table][symbol]:
                        if count == 0:
                            tabledata[item[1]].parentkeysymbolnames.append(symbol)
                            tabledata[item[1]].parentkeysymboldata[symbol] = []
                        tabledata[table].fielddata[item[0]].isforeignkey = True
                        tabledata[item[1]].fielddata[item[2]].isparentkey = True
                        tabledata[table].fielddata[item[0]].fksymbol = symbol   # not doing for parent field cause it could be parent to many FKs
                        tabledata[table].fksymboldata[symbol].append((item[0], item[1], item[2]))
                        tabledata[item[1]].parentkeysymboldata[symbol].append((item[2], table, item[0]))
                        count +=1
                    # symbolcounts[table][symbol] -= 1
        print("DONE adding Foreign Key Information")

    def applyUniqueKeysToTables(self, tabledata, listOfUniqueKeys, listOfDrops):
        """

        :param tabledata:
        :param listOfUniqueKeys:
        :param listOfDrops:
        :return:
        """
        symboldata = {}  # Map[ tablename -> Map[symbol -> List[(field)]]]
        symbolcounts = {}  # Map[ tablename -> Map[ symbol : count ]]
        for item in listOfUniqueKeys:
            tablename = item[0]
            fieldnames = item[1]
            symbol = item[2]
            if tablename not in symboldata:
                symboldata[tablename] = {}
                symbolcounts[tablename] = {}
            if symbol not in symboldata[tablename]:
                symboldata[tablename][symbol] = []
                symbolcounts[tablename][symbol] = 0
            # clear anything that may have been there before for that (table,symbol)
            symboldata[tablename][symbol] = []
            for i in range(0, len(fieldnames)):
                field = fieldnames[i]
                symboldata[tablename][symbol].append((field))
            symbolcounts[tablename][symbol] += 1
        for item in listOfDrops:
            tablename = item[0]
            symbol = item[1]
            if symbol not in symboldata[tablename]:
                symboldata[tablename][symbol] = []
                symbolcounts[tablename][symbol] = 0
            symbolcounts[tablename][symbol] -= 1
        for table in symbolcounts.keys():
            for symbol in symbolcounts[table].keys():
                if symbolcounts[table][symbol] > 0:
                    keyslist = symboldata[table][symbol]
                    tabledata[table].uniquekeys.append(keyslist)
                    for item in keyslist:
                        tabledata[table].fielddata[item].unique = True
        print("DONE adding Unique Key Information")
