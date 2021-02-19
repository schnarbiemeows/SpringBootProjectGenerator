from utilities.Utilities import *
from configuration.Constants import *

"""
    this class represents all of the properties that a given column of a table could have
    used to create the POJOs in our SB projects
"""
class FieldProperties:

    """
        conversion are coming from : https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-type-conversions.html
    """
    mysql_to_java_conv_signed = { "numeric" : "BigDecimal",
                           "decimal" : "BigDecimal",
                           "integer" : "Integer",
                           "bigint" : "Long",
                           "smallint" : "Integer",
                           "mediumint" : "Integer",
                           "float" : "Float",
                           "real" : "Float",
                           "dec" : "BigDecimal",
                           "int" : "Integer",
                           "fixed" : "BigDecimal",
                           "double" : "Double",
                           "bit" : "boolean",
                           "date" : "Date",
                           "datetime" : "Date",
                           "timestamp" : "Timestamp",
                           "time" : "Time",
                           "year" : "Date ",
                           "varchar" : "String",
                           "boolean" : "boolean",
                           "char" : "String",
                           "binary" : "byte[]",
                           "varbinary" : "byte[]",
                           "tinyblob": "String[]",
                           "blob" : "String[]",
                           "text" : "String",
                           "enum" : "String",
                           "set" : "String" }

    mysql_to_java_conv_unsigned = {"numeric": "BigDecimal",
                                 "decimal": "BigDecimal",
                                 "integer": "Long",
                                 "bigint": "BigInteger",
                                 "smallint": "Integer",
                                 "mediumint": "Integer",
                                 "float": "Float",
                                 "real": "Float",
                                 "dec": "BigDecimal",
                                 "int": "Integer",
                                 "fixed": "BigDecimal",
                                 "double": "Double",
                                 "bit": "boolean",
                                 "date": "Date",
                                 "datetime": "Date",
                                 "timestamp": "Timestamp",
                                 "time": "Time",
                                 "year": "Date ",
                                 "varchar": "String",
                                 "boolean": "boolean",
                                 "char": "String",
                                 "binary": "byte[]",
                                 "varbinary": "byte[]",
                                 "tinyblob": "String[]",
                                 "blob": "String[]",
                                 "text": "String",
                                 "enum": "String",
                                 "set": "String"}

    number_signed_limits = {
                            "integer" : (-2147483648,2147483647),
                            "bigint" : (-9223372036854775808,9223372036854775807),
                            "smallint" : (-32768,32767),
                            "mediumint" : (-2147483648,2147483647),
                            "int" : (-2147483648,2147483647)
                            }
    number_unsigned_limits = {
                            "integer" : (-2147483648,2147483647),
                            "bigint" : (-9223372036854775808,9223372036854775807),
                            "smallint" : (-2147483648,2147483647),
                            "mediumint" : (-2147483648,2147483647),
                            "int" : (-2147483648,2147483647)
                            }

    def __init__(self, name):
        """
        initialization
        :param name:
        """
        utilities = Utilities()
        # database field name
        self.name = name
        self.correctedtablename = ''
        # camel case name with lower 1st letter, camel case name with upper 1st letter
        self.javaname, self.gettername = self.makejavanames()
        self.datatype = None
        self.comment = ''
        self.canbenull = True
        self.isprimary = False
        self.primarytype = None
        self.isforeignkey = False
        self.isparentkey = False    # is it the reference key for a foreign key
        self.fksymbol = ''  # details are in parent Table object
        self.unique = False
        self.lengthreq = False
        self.length = 0
        self.min = None
        self.max = None
        self.decimals = 0
        self.importset = set()

    def makejavanames(self):
        """
        utility to make a Java name from a database name
        :return:
        """
        javaname = ''
        gettername = ''
        self.correctedtablename = self.name.replace("`","").replace("~|*", "_")
        if (self.correctedtablename.find("_") > -1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(self.correctedtablename))
            for n in x:
                if (toUpper == True):
                    #if(dbname[n].isnumeric == False):
                    #    convertedjavaname += dbname[n].upper()
                    #else:
                    convertedjavaname += self.correctedtablename[n].upper()
                    toUpper = False
                elif (self.correctedtablename[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += self.correctedtablename[n]
            gettername = self.capitalize(convertedjavaname)
            javaname = convertedjavaname
        else:
            gettername = self.capitalize(self.correctedtablename)
            javaname = self.correctedtablename
        print("making javaname = " + javaname + " getter name = " + gettername + " from db name = ")
        return (javaname, gettername)

    def translate_datatype(self,datatype,signed):
        """
        this method sets the objects data type after converting from mysql type to Java type
        :param datatype:
        :param signed:
        :return:
        """
        if(signed == True):
            self.datatype = FieldProperties.mysql_to_java_conv_signed[datatype]
            print("converting data type : " + datatype + " to --> " + self.datatype)
            if (datatype.find("integer") > -1 or datatype.find("mediumint") > -1 or
                datatype.find("bigint") > -1 or datatype.find("smallint") > -1 or
                datatype.find("int") > -1):
                if self.isprimary == True or self.isforeignkey == True:
                    self.min = 0
                else:
                    self.min = FieldProperties.number_signed_limits[datatype][0]
                self.max = FieldProperties.number_signed_limits[datatype][1]
        else:
            self.datatype = FieldProperties.mysql_to_java_conv_unsigned[datatype]
            print("converting data type : " + datatype + " to --> " + self.datatype)
            if (datatype.find("integer") > -1 or datatype.find("mediumint") > -1 or
                    datatype.find("bigint") > -1 or datatype.find("smallint") > -1 or
                    datatype.find("int") > -1):
                if self.isprimary == True or self.isforeignkey == True:
                    self.min = 0
                else:
                    self.min = FieldProperties.number_unsigned_limits[datatype][0]
                self.max = FieldProperties.number_unsigned_limits[datatype][1]

    def extract_field_properties(self, innerarray):
        """
        this method will obviously need some extensive work on it
        in order to truly be able to parse out ALL of a fields properties
        from a "create table" statement
        :param innerarray:
        :return:
        """
        # different possible properties
        comment_section = False
        not_found = False
        null_found = False
        key_found = False
        primary_found = False
        foreign_found = False
        not_null = True
        auto_increment_found = False
        comment = ''
        x = range(2, len(innerarray))
        for n in x:
            itemstr = innerarray[n].replace("^&%"," ").lower()
            if (comment_section == True):
                comment += itemstr + " "
                if (itemstr.endswith("\"")):
                    comment_section = False
            elif (itemstr.find("comment") > -1):
                comment_section = True
            elif (itemstr.find("primary") > -1):
                primary_found = True
            elif (itemstr.find("key") > -1):
                key_found = True
            elif (itemstr.find("foreign") > -1):
                foreign_found = True
            elif (itemstr.find("auto_increment") > -1):
                auto_increment_found = True
            elif itemstr.find("not") > -1:
                not_found = True
            elif itemstr.find("null") > -1:
                null_found = True
        if (not_found == True and null_found == True):
            not_null = False
        if primary_found == True and key_found == True:
            self.isprimary = True
        if foreign_found == True and key_found == True:
            self.isforeignkey = True

        self.canbenull = not_null
        self.comment = comment
        if (auto_increment_found == True):
            self.primarytype = "@GeneratedValue(strategy=GenerationType.AUTO)"
            #self.importset.add(Constants.import_gentype)
            #self.importset.add(Constants.import_genval)

    def set_length(self, lengthstr):
        """
        this method will set the maximum data type length
        :param lengthstr:
        :return:
        """
        lengthstr = lengthstr.replace("(","").replace(")","").replace(";","")
        self.length = int(lengthstr)

    def properties(self,outputfile=None):
        """
        #print out the objects fields and properties
        :return:
        """
        #print("field name = " + self.name)
        #print("field javaname = " + self.javaname)
        #print("field gettername = " + self.gettername)
        #print("field datatype = " + self.datatype)
        #print("field comment = " + self.comment)
        #print("field isprimary = " + str(self.isprimary))
        if (outputfile is not None):
            outputfile.write("field name = " + self.name+"\n")
            outputfile.write("field javaname = " + self.javaname+"\n")
            outputfile.write("field gettername = " + self.gettername+"\n")
            outputfile.write("field datatype = " + self.datatype+"\n")
            outputfile.write("field comment = " + self.comment+"\n")
            outputfile.write("field isprimary = " + str(self.isprimary)+"\n")

    def capitalize(self,word):
        """
        small function to capitalize the first letter of the javaname
        :param word:
        :return:
        """
        letter = word[0].upper()
        restofword = word[1:len(word)]
        totalword = letter + restofword
        return totalword
