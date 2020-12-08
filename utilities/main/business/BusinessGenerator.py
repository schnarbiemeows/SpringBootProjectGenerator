from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *

class BusinessGenerator:

    def __init__(self):
        None

    @staticmethod
    def create_business_class(table):
        """
        this method will create a business class for the project
        :param table:
        :return:
        """
        tabs = Constants.tab
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_bus + "/" + table.camelcasejavaname + \
                   "Business.java"
        resources_file = open(filename, "w")
        business_file = open("files/business/business.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if linestr.find("PRIMARY_KEY")>-1:
                text = Utilities.create_get_pk_stmt(table)
                resources_file.write(linestr.replace("%", table.camelcasejavaname).replace("&",
                                                                                           table.lowercasename)
                                     .replace("PRIMARY_KEY",text))
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            elif linestr.find("FKSECTION")>-1:
                BusinessGenerator.create_fk_section(table,resources_file)
            else:
                resources_file.write(linestr.replace("$", table.rootpackage).replace("%",
                                                                                     table.camelcasejavaname)
                                     .replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        business_file.close()

    @staticmethod
    def create_fk_section(table,output_file,test=False):
        """
        this method will create a search by foreign key method for each foreign key this table has
        as well as one to search by all of its foreign keys at once
        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        compoundFK = []
        datatypes = []
        inputparameters = []
        counter = 0
        for symbolname in table.fksymbolnames:
            fklist = table.fksymboldata[symbolname]
            for item in fklist:
                field = table.fielddata[item[0]]
                compoundFK.append(field.gettername)
                datatypes.append(
                    "@PathVariable " + Utilities.translateDataType(field.datatype) + " id" + str(counter))
                inputparameters.append("id" + str(counter))
                output_file.write(tabs + Constants.doc_get_fk.replace("z", field.javaname)
                                     .replace("^", table.camelcasejavaname))
                output_file.write(tabs + "public List<" + table.camelcasejavaname + "DTO> find" + table.camelcasejavaname + "By" +
                                  field.gettername + "(" + Utilities.translateDataType(
                                    field.datatype) + " id) throws Exception {\n")
                if test == False:
                    output_file.write(
                        tabs * 2 + "Iterable<" + table.camelcasejavaname + "> results = service.find" + table.camelcasejavaname + "By" +
                        field.gettername + "(id);\n")
                    output_file.write(tabs * 2 + "Iterator<" + table.camelcasejavaname +
                                      "> iter = results.iterator();\n")
                output_file.write(tabs * 2 + "List<" + table.camelcasejavaname +
                                  "DTO> resultsdto = new ArrayList();\n")
                if test == False:
                    output_file.write(tabs * 2 + "while(iter.hasNext()) {\n")
                    output_file.write(tabs * 3 + table.camelcasejavaname +" item = iter.next();\n")
                    output_file.write(tabs * 3 + "resultsdto.add(item.toDTO());\n" + tabs*2 + "}\n")
                output_file.write(tabs * 2 + "return resultsdto;\n" + tabs + "}\n\n")
                counter += 1
        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            output_file.write(tabs + Constants.doc_get_fk.replace("z", compoundFKstr)
                                 .replace("^", table.camelcasejavaname))
            text = tabs + "public List<" + table.camelcasejavaname + "DTO> find" + table.camelcasejavaname + "By" + compoundFKstr + "("
            text += ",".join(datatypes)
            text += ") throws Exception {\n"
            output_file.write(text)
            if test == False:
                output_file.write(
                    tabs * 2 + "Iterable<" + table.camelcasejavaname + "> results = service.find" + table.camelcasejavaname + "By" +
                    compoundFKstr + "(" + ", ".join(inputparameters) + ");\n")
                output_file.write(tabs * 2 + "Iterator<" + table.camelcasejavaname +
                                  "> iter = results.iterator();\n")
            output_file.write(tabs * 2 + "List<" + table.camelcasejavaname +
                              "DTO> resultsdto = new ArrayList();\n")
            if test == False:
                output_file.write(tabs * 2 + "while(iter.hasNext()) {\n")
                output_file.write(tabs * 3 + table.camelcasejavaname + " item = iter.next();\n")
                output_file.write(tabs * 3 + "resultsdto.add(item.toDTO());\n" + tabs * 2 + "}\n")
            output_file.write(tabs * 2 + "return resultsdto;\n" + tabs + "}\n\n")

    @staticmethod
    def create_business_class_for_mid_lvl(mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create a business class for the mid-level projects
        :param mid_lvl_proj:
        :return:
        """
        tabs = Constants.tab
        # create the file and open
        filename = mid_lvl_proj.topmainpackage + "/" + Constants.pckg_bus + "/" + \
                   mid_lvl_proj.camelcasejavaname + "Business.java"
        resources_file = open(filename, "w")
        business_file = open("files/business/business_mid_lvl.txt")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if (linestr.find("MAIN_SECTION")) > -1:
                BusinessGenerator.create_business_service_proxy_calls(mid_lvl_proj, crud_proj_names,
                                                                      crud_proj_data,resources_file)
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr.replace("%", mid_lvl_proj.camelcasejavaname)
                                     .replace("&", mid_lvl_proj.lowercasename)
                                     .replace("^", Configuration.author)
                                     .replace("$",mid_lvl_proj.rootpackage))
        resources_file.close()
        business_file.close()

    @staticmethod
    def create_business_service_proxy_calls(mid_lvl_proj, crud_proj_names, crud_proj_data, resources_file):
        """

        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = Constants.tab
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + \
                           "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                resources_file.write(Constants.doc_proxy)
                resources_file.write(tabs+Constants.ann_autowired+"\n")
                service_name = currentproject.lowercasename+"serviceproxy"
                resources_file.write(tabs+currentproject.camelcasejavaname+"ServiceProxy "+
                                     service_name+" ;\n\n")
                source_file = open(filename, "r")
                utilities = Utilities()
                for line in source_file:
                    linestr = str(line)
                    if(linestr.find("public ResponseEntity<Object>")) > -1:
                        method_name = utilities.remove_datatypes_from_string(linestr)
                        resources_file.write(Constants.doc_proxy)
                        resources_file.write(utilities.remove_annotations_from_string(linestr)
                                             .replace(";","{")+"\n")
                        resources_file.write(tabs*2+"return "+service_name+"."+method_name+";\n"+tabs+"}\n\n")
                source_file.close()