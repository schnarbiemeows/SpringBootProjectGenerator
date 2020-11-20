from configuration.Configuration import *
from utilities.Utilities import *

class GenerateRepository:
    
    def __init(self):
        None
        
    @staticmethod
    def create_repository_class(table):
        """
        this method will create the Repository class file
        :param table:
        :return:
        """
        filename = table.topmainpackage + "/" + Constants.pckg_services + "/" + table.camelcasejavaname + "Repository.java"
        output_file = open(filename, "w")
        output_file.write("package " + table.rootpackage + "." + Constants.pckg_services + ";\n\n")
        output_file.write(Constants.import_repo + "\n")
        #output_file.write(Constants.import_query + "\n")
        #output_file.write(Constants.import_param + "\n")
        output_file.write(Constants.import_pojo.replace("%",table.rootpackage+".pojos."+table.camelcasejavaname)+"\n")
        output_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        output_file.write(Constants.class_decl_repo.replace("*",table.camelcasejavaname) + "\n")
        GenerateRepository.make_special_queries(table,output_file)
        output_file.write("}\n")
        output_file.close()
        
    @staticmethod
    def make_special_queries(table,output_file):
        """
        this method will make any special queries needed for any tables that have foreign keys
        :param table: 
        :param output_file: 
        :return: 
        """
        tabs = Constants.tab
        compoundFK = []
        inputfields = []
        queryparameters = []
        counter = 0
        for symbolname in table.fksymbolnames:
            fklist = table.fksymboldata[symbolname]
            for item in fklist:
                field = table.fielddata[item[0]]
                compoundFK.append(field.gettername)
                inputfields.append(Utilities.translateDataType(field.datatype) + ' ' + field.javaname)
                output_file.write(tabs + Constants.doc_query_fk.replace("z", field.javaname)
                                  .replace("^", table.camelcasejavaname))
                output_file.write(tabs + 'public Iterable<' + table.camelcasejavaname + '> find' + table.camelcasejavaname + 'By' +
                                  field.gettername + '(' + Utilities.translateDataType(
                    field.datatype) + ' ' + field.javaname + ");\n")
                counter += 1
        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            output_file.write(tabs + Constants.doc_query_all_fk.replace("^", table.camelcasejavaname))
            methodtext = tabs + "public Iterable<" + table.camelcasejavaname + "> find" + table.camelcasejavaname + "By" + compoundFKstr + "("
            methodtext += ",".join(inputfields) + ");\n"
            output_file.write(methodtext)
