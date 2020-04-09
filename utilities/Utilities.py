import os
import shutil
import xml.etree.ElementTree as ET

"""
    utility class
"""
class Utilities:

    """
        utility for creating a directory
    """
    def mkdir(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
            #print("making directory : " + path)
        else:
            print(path+ " already exists")

    """
        utility for copying a file
    """
    def cpy(self,srcpath,destpath):
        if not os.path.exists(destpath):
            shutil.copy(srcpath,destpath)
           # print("copying file from : " + srcpath + " to : " + destpath)
        else:
            print(destpath+ " already exists")

    """
        utility to make a Java name from a database name
    """
    def makejavanames(self,dbname):
        javaname = ''
        gettername = ''
        if (dbname.find("_") > -1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(dbname))
            for n in x:
                if (toUpper == True):
                    convertedjavaname += dbname[n].upper()
                    toUpper = False
                elif (dbname[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += dbname[n]
                    gettername = self.capitalize(convertedjavaname)
                    javaname = convertedjavaname
        else:
            gettername = self.capitalize(dbname)
            javaname = dbname
        print("making javaname = " + javaname + " getter name = " + gettername + " from db name = " + dbname)
        return (javaname, gettername)

    """
    
    """
    def parse_source_pom(self,sourceprojectfolder):
        pomfile = open(sourceprojectfolder + "/demo/pom.xml")
        tree = ET.parse(pomfile)
        root = tree.getroot()
        artifactId = ''
        for child in root:
            childitem = str(child.tag)
            if (childitem.find('artifactId') > -1):
                print("sorce POM artifact ID = " + child.text)
                artifactId = child.text
        pomfile.close()
        return artifactId

    """
        small function to capitalize the first letter of the javaname
    """
    def capitalize(self,word):
        letter = word[0].upper()
        restofword = word[1:len(word)]
        totalword = letter + restofword
        return totalword

    """
       see below 
    """
    def handleFieldsWithCommas(self,inputstring):
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

    """
       see below 
    """
    def handleFieldsWithCommasAndParens(self, inputstring):
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
        temp_array = outputstr.split(',')
        for i in range(0, len(temp_array)):
            item = str(temp_array[i])
            if item.find("@#$") > -1:
                item = item.replace("@#$", ",").replace('"', '')
                temp_array[i] = item
        return temp_array
