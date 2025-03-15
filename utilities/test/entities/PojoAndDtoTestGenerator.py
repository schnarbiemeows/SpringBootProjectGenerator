from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *

class PojoAndDtoTestGenerator:
    
    def __init__(self):
        None

    @staticmethod
    def create_pojo_test_class(table,src, tabledata):
        """
        create the POJO and DTO test classes
        :param table: 
        :param src: 
        :param tabledata: 
        :return: 

        # create the file and open
        filename = ''
        if src == "pojo":
            filename = table.toptestpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + "Test.java"
        else:
            filename = table.toptestpackage + "/" + Constants.pckg_dtos + "/" + table.dtoname + "Test.java"
        resources_file = open(filename, "w")
        test_pojo = open("files/pojo_and_dto_test.txt")
        if src == "pojo":
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
            for line in test_pojo:
                linestr = str(line)
                if (linestr.find("XXX")) > -1:
                    PojoAndDtoTestGeneratorcreate_pojo_setters_stmt(table, resources_file, "Y", tabledata)
                elif linestr.find("YYY") > -1:
                    PojoAndDtoTestGeneratorcreate_pojo_setters_stmt(table, resources_file, "N", tabledata)
                else:
                    resources_file.write(
                            linestr.replace("&", table.camelcasejavaname).replace("%", table.tablename).replace("^",
                            Configuration.author).replace("XXX", "POJO"))
            resources_file.close()
        else:
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_dtos + ";\n\n")
            for line in test_pojo:
                linestr = str(line)
                if(linestr.find("XXX"))>-1:
                    PojoAndDtoTestGeneratorcreate_dto_setters_stmt(table, resources_file, "Y",tabledata)
                elif linestr.find("YYY")>-1:
                    PojoAndDtoTestGeneratorcreate_dto_setters_stmt(table, resources_file, "N",tabledata)
                else:
                    resources_file.write(linestr.replace("&", table.dtoname).replace("%", table.tablename).replace("^",Configuration.author).replace("XXX", "DTO"))
            resources_file.close()
        """
        # create the file and open
        filename = ''
        if src == "pojo":
            filename = table.toptestpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + "Test.java"
        else:
            filename = table.toptestpackage + "/" + Constants.pckg_dtos + "/" + table.dtoname + "Test.java"
        resources_file = open(filename, "w")
        test_pojo = open("files/entities/pojo_and_dto_test.txt")
        if src == "pojo":
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
        else:
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_dtos + ";\n\n")
        resources_file.write("import " + table.rootpackage + "." + Constants.pckg_util + ".Randomizer;\n")
        for line in test_pojo:
            linestr = str(line)
            if (linestr.find("SETTER_STMT")) > -1:
                PojoAndDtoTestGenerator.create_pojo_setters_stmt(table, resources_file, "Y",tabledata)
            elif linestr.find("GETTER_STMT") > -1:
                PojoAndDtoTestGenerator.create_pojo_setters_stmt(table, resources_file, "N",tabledata)
            else:
                if src == "pojo":
                    resources_file.write(
                        linestr.replace("&", table.camelcasejavaname).replace("%", Constants.cut)
                            .replace("^",Configuration.author))
                else:
                    resources_file.write(linestr.replace("&", table.dtoname).replace("%", Constants.cut)
                        .replace("^",Configuration.author))
        resources_file.close()

    """
    @staticmethod
    def get_str_from_datatype(datatype):
        
        get the string from the data type
        :param datatype: 
        :return: 
        
        if (datatype == "BigDecimal"):
            return "new BigDecimal(1.00));\n"
        elif (datatype == "BigInteger"):
            return "new BigInteger(1));\n"
        elif (datatype == "Integer"):
            return "new Integer(1));\n"
        elif (datatype == "Float"):
            return "1.0f);\n"
        elif (datatype == "Double"):
            return "1.0);\n"
        elif (datatype == "Date"):
            return "new Date());\n"
        elif (datatype == "boolean"):
            return 'true);\n'
        elif (datatype == "Timestamp"):
            return "new Timestamp(1000));\n"
        elif (datatype == "Time"):
            return "new java.sql.Time(1000));\n"
        elif (datatype == "byte[]"):
            return '"a".getBytes());\n'
        elif (datatype == "String"):
            return '"a");\n'
        elif (datatype == "Long"):
            return "new Long(1));\n"
    """

    @staticmethod
    def create_pojo_setters_stmt( table, file, setter, tabledata):
        """
        generate the getters and setters statement for the test class
        :param table: 
        :param file: 
        :param setter:
        :param tabledata: 
        :return: 

        tabs = Constants.tab
        text = ''
        if setter == "Y":
            # do the PRIMARY KEYS first
            if len(table.primarykeys) > 1:
                file.write(
                    tabs * 2 + table.camelcasejavaname + "PK " + table.lowercasename + "PK = new " + table.camelcasejavaname + "PK;\n")
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == True:
                        file.write(tabs * 2 + table.lowercasename + "PK.set" + fielddata.gettername + "(" +
                            PojoAndDtoTestGenerator.get_str_from_datatype(fielddata.datatype))
                file.write(tabs *2 + Constants.cut + ".set" + table.camelcasejavaname + "PK(" + table.lowercasename + "PK);\n")
            else:
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == True:
                        file.write(tabs*2 + Constants.cut + ".set" + fielddata.gettername+"("+
                            PojoAndDtoTestGenerator.get_str_from_datatype(fielddata.datatype))
            # now do any FOREIGN KEYS
            parentset = set()
            for symbolname in table.fksymbolnames:
                fksymboldata = table.fksymboldata[symbolname]
                firstitem = fksymboldata[0]
                childfield = table.fielddata[firstitem[0]]
                parenttable = tabledata[firstitem[1]]
                if not parenttable.camelcasejavaname in parentset:
                    file.write(tabs * 2 + Constants.cut + ".set" + parenttable.camelcasejavaname + "( new " +
                           parenttable.camelcasejavaname + "());\n")
                    parentset.add(parenttable.camelcasejavaname)
            # now do any PARENT KEYS
            childset = set()
            for symbolname in table.parentkeysymbolnames:
                pksymboldata = table.parentkeysymboldata[symbolname]
                firstitem = pksymboldata[0]
                childtable = tabledata[firstitem[1]]
                childfield = childtable.fielddata[firstitem[2]]
                if not childtable.camelcasejavaname in childset:
                    if childfield.unique:
                        file.write(tabs * 2 + Constants.cut + ".set" + childtable.camelcasejavaname + "(null);\n")
                    else:
                        file.write(tabs * 2 + Constants.cut + ".set" + childtable.camelcasejavaname + "s(null);\n")
                    childset.add(childtable.camelcasejavaname)
            # finally do all the rest of the fields
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == False and fielddata.isforeignkey == False and fielddata.isparentkey == False:
                    file.write(tabs * 2 + Constants.cut + ".set" + fielddata.gettername + "(" +
                               PojoAndDtoTestGenerator.get_str_from_datatype(fielddata.datatype))
        else:
            # do the PRIMARY KEYS first
            if len(table.primarykeys) > 1:
                text += tabs * 2 + Constants.cut + ".get" + table.camelcasejavaname + "(),\n"
                #for field in table.fieldnames:
                #    fielddata = table.fielddata[field]
                #    if fielddata.isprimary == True:
                #        text +=tabs * 2 + table.lowercasename + "PK.set" + fielddata.gettername + "(" +
                #                   PojoAndDtoTestGenerator.get_str_from_datatype(fielddata.datatype)
                #text +=
                #    tabs * 2 + Constants.cut + ".set" + table.camelcasejavaname + "PK(" + table.lowercasename + "PK);\n"
            else:
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == True:
                        text +=tabs * 2 + Constants.cut + ".get" + fielddata.gettername + "(),\n"
            # now do any FOREIGN KEYS
            for symbolname in table.fksymbolnames:
                fksymboldata = table.fksymboldata[symbolname]
                firstitem = fksymboldata[0]
                childfield = table.fielddata[firstitem[0]]
                parenttable = tabledata[firstitem[1]]
                text +=tabs * 2 + Constants.cut + ".get" + parenttable.camelcasejavaname + "().get" + childfield.gettername + "(),\n"

            # now do any PARENT KEYS
            childset = set()
            for symbolname in table.parentkeysymbolnames:
                pksymboldata = table.parentkeysymboldata[symbolname]
                firstitem = pksymboldata[0]
                childtable = tabledata[firstitem[1]]
                childfield = childtable.fielddata[firstitem[2]]
                if not childtable.camelcasejavaname in childset:
                    if childfield.unique:
                        text +=tabs * 2 + Constants.cut + ".get" + childtable.camelcasejavaname + "(),\n"
                    else:
                        text +=tabs * 2 + Constants.cut + ".get" + childtable.camelcasejavaname + "s(),\n"
                    childset.add(childtable.camelcasejavaname)

            # finally do all the rest of the fields
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == False and fielddata.isforeignkey == False and fielddata.isparentkey == False:
                    text +=tabs * 2 + Constants.cut + ".get" + fielddata.gettername + "(),\n"
        if setter == 'N':
            text = text[0:-2]+");\n"
            file.write(text)
        """
        tabs = Constants.tab
        text = ''
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if setter == "Y":
                if fielddata.datatype == "String[]":
                    file.write(tabs*2 +'String[] stringarray = new String[1];\n')
                    file.write(tabs*2 +'stringarray[0] = Randomizer.randomString(3);\n')
                    file.write(tabs*2 + Constants.cut + ".set" + fielddata.gettername + "(stringarray);\n")
                else:
                    print(str(tabs + tabs + Constants.cut + ".set" + fielddata.gettername + "("))
                    file.write(tabs + tabs + Constants.cut + ".set" + fielddata.gettername + "(")
                    if (fielddata.datatype == "BigDecimal"):
                        file.write("new BigDecimal(1.00));\n")
                    elif (fielddata.datatype == "BigInteger"):
                        file.write("new BigInteger(1));\n")
                    elif (fielddata.datatype == "Integer"):
                        file.write("1);\n")
                    elif (fielddata.datatype == "Float"):
                        file.write("1.0f);\n")
                    elif (fielddata.datatype == "Double"):
                        file.write("1.0);\n")
                    elif (fielddata.datatype == "Date"):
                        file.write("new Date());\n")
                    elif (fielddata.datatype == "Timestamp"):
                        file.write("new Timestamp(1000));\n")
                    elif (fielddata.datatype == "Time"):
                        file.write("new java.sql.Time(1000));\n")
                    elif (fielddata.datatype == "byte[]"):
                        file.write('"a".getBytes());\n')
                    elif (fielddata.datatype == "String"):
                        file.write('"a");\n')
                    elif (fielddata.datatype == "Long"):
                        file.write("new Long(1));\n")
                    elif fielddata.datatype == "boolean":
                        file.write("true);\n")
            else:
                text += tabs + tabs + Constants.cut + ".get" + fielddata.gettername + "(),\n"
        if setter == 'N':
            text = text[0:-2] + ");\n"
            file.write(text)

    @staticmethod
    def create_dto_setters_stmt( table, file, set, tabledata):
        """
        generate the getters and setters statement for the test class
        :param table: 
        :param file: 
        :param set: 
        :param tabledata: 
        :return: 
        """
        tabs = Constants.tab
        text = ''
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if set == "Y":
                if fielddata.datatype == "String[]":
                    file.write(tabs * 2 + 'String[] stringarray = new String[1];\n')
                    file.write(tabs * 2 + 'stringarray[0] = Randomizer.randomString(3);\n')
                    file.write(tabs * 2 + Constants.cut + ".set" + fielddata.gettername + "(stringarray);\n")
                else:
                    file.write(tabs*2 + Constants.cut + ".set" + fielddata.gettername+"(")
                    if (fielddata.datatype == "BigDecimal"):
                        file.write("new BigDecimal(1.00));\n")
                    elif (fielddata.datatype == "BigInteger"):
                        file.write("new BigInteger(1));\n")
                    elif (fielddata.datatype == "Integer"):
                        file.write("1);\n")
                    elif (fielddata.datatype == "Float"):
                        file.write("1.0f);\n")
                    elif (fielddata.datatype == "Double"):
                        file.write("1.0);\n")
                    elif (fielddata.datatype == "Date"):
                        file.write("new Date());\n")
                    elif (fielddata.datatype == "boolean"):
                        file.write('true);\n')
                    elif (fielddata.datatype == "Timestamp"):
                        file.write("new Timestamp(1000));\n")
                    elif (fielddata.datatype == "Time"):
                        file.write("new java.sql.Time(1000));\n")
                    elif (fielddata.datatype == "byte[]"):
                        file.write('"a".getBytes());\n')
                    elif (fielddata.datatype == "String"):
                        file.write('"a");\n')
                    elif (fielddata.datatype == "Long"):
                        file.write("1l);\n")
                    elif fielddata.datatype == "boolean":
                        file.write("true);\n")
            else:
                text += tabs*2 + Constants.cut + ".get" + fielddata.gettername + "(),\n"
        if set == 'N':
            text = text[0:-2]+");\n"
            file.write(text)

    @staticmethod
    def create_pojo_and_dto_rand_gen_code(table, file, src, businessTest=False):
        """
        this
        :param table:
        :param file:
        :param src:
        :return:
        """
        tabs = Constants.tab
        text = ''
        if src == "pojo":
            file.write(tabs + tabs + table.camelcasejavaname + " " + Constants.record + " = new " + table.camelcasejavaname + "();\n")
        else:
            file.write(tabs + tabs + table.dtoname + " " + Constants.record + " = new " + table.dtoname + "();\n")
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == False:
                if fielddata.datatype == "String[]":
                    file.write(tabs*2 +'String[] stringarray = new String[1];\n')
                    file.write(tabs*2 +'stringarray[0] = Randomizer.randomString(3);\n')
                    file.write(tabs*2 + Constants.record + ".set" + fielddata.gettername + "(stringarray);\n")
                else:
                    file.write(tabs + tabs + Constants.record + ".set" + fielddata.gettername+"(")
                    if (fielddata.datatype == "BigDecimal"):
                        file.write('Randomizer.randomBigDecimal("1000"));\n')
                    elif (fielddata.datatype == "BigInteger"):
                        file.write('Randomizer.randomBigInteger("1000"));\n')
                    elif (fielddata.datatype == "Integer"):
                        file.write('Randomizer.randomInt(1000));\n')
                    elif (fielddata.datatype == "Long"):
                        file.write('Randomizer.randomLong(1000L));\n')
                    elif (fielddata.datatype == "Float"):
                        file.write('Randomizer.randomFloat(1000F));\n')
                    elif (fielddata.datatype == "Double"):
                        file.write('Randomizer.randomDouble(1000D));\n')
                    elif (fielddata.datatype == "Date"):
                        file.write('Randomizer.randomDate());\n')
                    elif (fielddata.datatype == "boolean"):
                        file.write('Randomizer.randomBoolean());\n')
                    elif (fielddata.datatype == "Timestamp"):
                        file.write('Randomizer.randomTimestamp(1000));\n')
                    elif (fielddata.datatype == "Time"):
                        file.write('Randomizer.randomTime(1000));\n')
                    elif (fielddata.datatype == "byte[]"):
                        file.write('Randomizer.randomBytes(20));\n')
                    elif (fielddata.datatype == "String"):
                        if fielddata.lengthreq == True:
                            if fielddata.length<20:
                                file.write('Randomizer.randomString('+str(fielddata.length)+'));\n')
                            else:
                                file.write('Randomizer.randomString(20));\n')
                        else:
                            file.write('Randomizer.randomString(20));\n')
            else:
                if businessTest:
                    file.write(tabs + tabs + Constants.record + ".set" + fielddata.gettername + "(1);\n")
        file.write(tabs + tabs + "return " + Constants.record + ";\n")
    