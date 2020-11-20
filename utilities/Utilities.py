import os
import shutil
#import xml.etree.ElementTree as ET
from configuration.Constants import Constants

"""
    utility class
"""
class Utilities:

    @staticmethod
    def mkdir(path):
        """
        utility for creating a directory
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.mkdir(path)
            #print("making directory : " + path)
        else:
            print(path+ " already exists")

    @staticmethod
    def cpy(srcpath,destpath):
        """
        utility for copying a file
        :param srcpath:
        :param destpath:
        :return:
        """
        if not os.path.exists(destpath):
            shutil.copy(srcpath,destpath)
           # print("copying file from : " + srcpath + " to : " + destpath)
        else:
            print(destpath+ " already exists")

    @staticmethod
    def makejavanames(dbname):
        """
        utility to make a Java name from a database name
        :param dbname:
        :return:
        """
        javaname = ''
        gettername = ''
        if (dbname.find("_") > -1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(dbname))
            for n in x:
                if (toUpper == True):
                    if(dbname[n].isnumeric == False):
                        convertedjavaname += dbname[n].upper()
                    else:
                        convertedjavaname += dbname[n]
                    toUpper = False
                elif (dbname[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += dbname[n]
            gettername = Utilities.capitalize(convertedjavaname)
            javaname = convertedjavaname
        else:
            gettername = Utilities.capitalize(dbname)
            javaname = dbname
        print("making javaname = " + javaname + " getter name = " + gettername + " from db name = " + dbname)
        return (javaname, gettername)

    @staticmethod
    def capitalize(word):
        """
        small function to capitalize the first letter of the javaname
        :param word:
        :return:
        """
        letter = word[0].upper()
        restofword = word[1:len(word)]
        totalword = letter + restofword
        return totalword

    @staticmethod
    def handleFieldsWithCommas(inputstring):
        """
        the input file tha we get may include records that have fields with commas in them
        in this case, the field will be surrounded by double quotes
        this method will check the record for double quotes, and then it will parse through it
        according to double quotes, and, when it finds a pair, it will replace any commas with @#$
        finally, it will recombine the string, split it by comma again, and then replace any items in the
        array that have @#$ in them with a comma
        :param inputstring:
        :return: array of strings
        """
        if inputstring.count('"') == 0:
            return inputstring.split(',')
        elif inputstring.count('"') % 2 > 0:
            raise Exception("# of double quote characters in this file is an odd #: therefore the file is invalid!")
        else:
            leftstring = ''
            rightstring = ''
            middlestring = inputstring
            while middlestring.find('"') > -1:
                leftstring += middlestring[0:middlestring.find(
                    '"') + 1]  # leftstring equals everything up to and including the odd quote
                middlestring = middlestring[
                               middlestring.find('"') + 1:]  # middle string now equals everything after the odd quote
                if middlestring.find('"') < len(middlestring) - 1:  # if the even quote is not at the end of the string
                    rightstring = middlestring[middlestring.find(
                        '"') + 1:]  # the right string equals everything that is after the even quote
                else:
                    rightstring = ''
                middlestring = middlestring[:middlestring.find('"') + 1].replace(",",
                                                                                 "@#$")  # now make the middle string everything before and including
                # the even quote, and replace all commas with @#$
                leftstring += middlestring  # now add the middlestring to the leftstring
                middlestring = rightstring  # and make the right string the new middle string
            leftstring += middlestring
            # print(leftstring)
            temp_array = leftstring.split(',')
            for i in range(0, len(temp_array)):
                item = str(temp_array[i])
                if item.find("@#$") > -1:
                    item = item.replace("@#$", ",").replace('"', '')
                    temp_array[i] = item
            return temp_array

    @staticmethod
    def handleFieldsWithCommasAndParens(inputstring):
        """
        the input file that we get may include records that have fields with commas in them
        in this case, the field will be surrounded by double quotes
        this method will check the record for double quotes, and then it will parse through it
        according to double quotes, and, when it finds a pair, it will replace any commas with @#$
        finally, it will recombine the string, split it by comma again, and then replace any items in the
        array that have @#$ in them with a comma
        :param inputstring:
        :return: array of strings

        quotesfound = False
        parenfound = False
        strlen = len(inputstring)
        outputstr = ''
        counter = 0
        leftstring = ''
        rightstring = ''
        middlestring = inputstring
        while counter < strlen:
            character = inputstring[counter]
            if character == '"':
                outputstr += character
                quotesfound = not quotesfound
            elif character == "(":
                outputstr += character
                parenfound = True
            elif character == ")":
                outputstr += character
                parenfound = False
            elif character == ",":
                if (quotesfound == True or parenfound == True):
                    outputstr += "@#$"
                else:
                    outputstr += character
            elif character == " ":
                if quotesfound == True:
                    outputstr += "^&%"
                else:
                    outputstr += character
            else:
                outputstr += character
            counter +=1
        """
        temp_array = inputstring.split("decimal")
        if len(temp_array)>1:
            for i in range(0, len(temp_array)):
                if i>0:
                    item = str(temp_array[i])
                    if item.find(",") > -1:
                        item = item.replace(",", "ZYX",1)
                        temp_array[i] = item
        inputstring = "decimal".join(temp_array)
        temp_array = inputstring.split(',')
        for i in range(0, len(temp_array)):
            item = str(temp_array[i])
            if item.find("@#$") > -1:
                item = item.replace("@#$", ",").replace('"', '')
                temp_array[i] = item
        return temp_array

    @staticmethod
    def parseGroupingsTextFile(filename):
        inputfile = open(filename)
        projectnames = []
        projecttables = {}
        for line in inputfile:
            linestr = str(line)
            if linestr.find("#")==-1:
                projectname = linestr.split(":")[0].strip()
                tablesstr = linestr.split(":")[1].strip()
                tables = tablesstr.split(",")
                projectnames.append(projectname)
                projecttables[projectname] = tables
        return (projectnames,projecttables)

    @staticmethod
    def remove_datatypes_from_string( inputstring):
        """
        this method is for the mid-level business classes; it will remove the data types from an input parameter string
        :param inputstring:
        :return:
        """
        tempstring = inputstring[inputstring.find("public ResponseEntity<Object>") + 30:]
        methodname = tempstring[0:tempstring.find("(")]
        parameterlist = tempstring[tempstring.find("("):tempstring.find(")")]
        paramsstring = ''
        if(len(parameterlist)==0):
            return methodname+"()"
        if(parameterlist.find(",") > -1):
            parameterpairs = parameterlist.split(",")
            for pair in parameterpairs:
                items = pair.split(" ")
                oddfield = True
                for item in items:
                    if(len(item)>0):
                        if(item.find("@")>-1):
                            None
                        elif(oddfield == False):
                            paramsstring += item + ","
                            oddfield = True
                        else:
                            oddfield = False
            return methodname+"("+paramsstring[:-1]+")"
        else:
            items = parameterlist.split(" ")
            oddfield = True
            for item in items:
                if (len(item) > 0):
                    if (item.find("@") > -1):
                        None
                    elif (oddfield == False):
                        paramsstring += item + ","
                        oddfield = True
                    else:
                        oddfield = False
            return methodname + "(" + paramsstring[:-1] + ")"

    @staticmethod
    def remove_annotations_from_string( inputstring):
        """
        this method is for the mid-level proxies, it will remove annotations from the method declarations
        :param inputstring:
        :return:
        """
        stringarray = inputstring.split("(")
        outputstring = stringarray[0]+'('
        remaining = stringarray[1].split(" ")
        for word in remaining:
            wordstr = str(word)
            if wordstr.find('@') == -1:
                outputstring += wordstr + " "
        return outputstring.rstrip()

    @staticmethod
    def translateDataType(type):
        """
        this method needs to translate Boxed primitives to primitives
        :param type:
        :return:
        """
        if type == "BigDecimal" or type == "Float" or type == "Double":
            return "double"
        elif type == "BigInteger" or type == "Integer":
            return "int"
        elif type == "String":
            return "String"
        elif type == "Boolean":
            return "boolean"
        else:
            return "None"

    @staticmethod
    def translateAngularDataType(type):
        """
        this method needs to translate Boxed primitives to javascript data types
        :param type:
        :return:
        """
        if type == "BigDecimal" or type == "Float" or type == "Double":
            return "number"
        elif type == "BigInteger" or type == "Integer":
            return "number"
        elif type == "String":
            return "string"
        elif type == "Boolean":
            return "boolean"
        else:
            return "None"

    @staticmethod
    def create_get_pk_stmt(table, test=False):
        """
        finds the primary key and adds it into the script
        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                if test == True:
                    return fielddata.gettername
                else:
                    return "get" + fielddata.gettername+"()"