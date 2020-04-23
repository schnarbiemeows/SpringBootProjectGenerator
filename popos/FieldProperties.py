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
                           "bit" : "byte[]",
                           "date" : "Date",
                           "datetime" : "Timestamp",
                           "timestamp" : "Timestamp",
                           "time" : "Time",
                           "year" : "Date ",
                           "varchar" : "String",
                           "char" : "String",
                           "binary" : "byte[]",
                           "varbinary" : "byte[]",
                           "blob" : "byte[]",
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
                                 "int": "Long",
                                 "fixed": "BigDecimal",
                                 "double": "Double",
                                 "bit": "byte[]",
                                 "date": "Date",
                                 "datetime": "Timestamp",
                                 "timestamp": "Timestamp",
                                 "time": "Time",
                                 "year": "Date ",
                                 "varchar": "String",
                                 "char": "String",
                                 "binary": "byte[]",
                                 "varbinary": "byte[]",
                                 "blob": "byte[]",
                                 "text": "String",
                                 "enum": "String",
                                 "set": "String"}

    """
        initialization
    """
    def __init__(self, name):
        utilities = Utilities()
        # database field name
        self.name = name
        # camel case name with lower 1st letter, camel case name with upper 1st letter
        self.javaname, self.gettername = utilities.makejavanames(name)
        self.datatype = None
        self.comment = ''
        self.canbenull = True
        self.isprimary = False
        self.primarytype = None
        self.unique = False
        self.lengthreq = False
        self.length = 0
        self.importset = set()


    """
        this method sets the objects data type after converting from mysql type to Java type
    """
    def translate_datatype(self,datatype,signed):
        if(signed == True):
            self.datatype = FieldProperties.mysql_to_java_conv_signed[datatype]
            print("converting data type : " + datatype + " to --> " + self.datatype)
        else:
            self.datatype = FieldProperties.mysql_to_java_conv_unsigned[datatype]
            print("converting data type : " + datatype + " to --> " + self.datatype)

    """
        this method will obviously need some extensive work on it
        in order to truly be able to parse out ALL of a fields properties
        from a "create table" statement
    """
    def extract_field_properties(self, innerarray):
        # different possible properties
        comment_section = False
        not_found = False
        null_found = False
        not_null = True
        primary_found = False
        unique_found = False
        auto_increment_found = False
        comment = ''
        x = range(2, len(innerarray))
        for n in x:
            itemstr = innerarray[n].replace("^&%"," ")
            if (comment_section == True):
                comment += itemstr
                if (itemstr.endswith("\"")):
                    comment_section = False
            elif (itemstr.find("comment") > -1):
                comment_section = True
            elif (itemstr.find("unique") > -1):
                unique_found = True
            elif (itemstr.find("primary") > -1):
                primary_found = True
            elif (itemstr.find("key") > -1):
                None  # we can ignore this keyword
            elif (itemstr.find("auto_increment") > -1):
                auto_increment_found = True
        if (not_found == True and null_found == True):
            not_null = False
        self.isprimary = primary_found
        if(self.isprimary == True):
            #self.importset.add(Constants.import_id)
            None
        self.unique = unique_found
        self.canbenull = not_null
        self.comment = comment
        if (auto_increment_found == True):
            self.primarytype = Constants.ann_autogen
            #self.importset.add(Constants.import_gentype)
            #self.importset.add(Constants.import_genval)

    """
        this method will set the size for any 
    """
    """
        this method will set the maximum data type length
    """
    def set_length(self, lengthstr):
        lengthstr = lengthstr.replace("(","").replace(")","")
        self.length = int(lengthstr)


