from configuration.Configuration import *
from utilities.test.entities.PojoAndDtoTestGenerator import PojoAndDtoTestGenerator
from utilities.Utilities import *

class RestControllerTestGenerator:

    def __init__(self):
        None

    @staticmethod
    def create_controller_test_class(table):
        """
        create the POJO test class
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_contr + "/" + table.camelcasejavaname + "ControllerTest.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller/controller_test.txt")
        resources_file.write("package " + table.rootpackage + ".controllers;\n\n")
        for line in test_controller:
            linestr = str(line)
            if(linestr.find("IMPORTS_SECTION"))>-1:
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ";\n")
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_dtos + "." + table.dtoname + ";\n")
                resources_file.write(
                    "import " + table.rootpackage + "." + Constants.pckg_bus + "." + table.camelcasejavaname + "Business;\n")
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_util + ".Randomizer;\n")
            elif linestr.find("RANDOM_DTO_GENERATOR")>-1:
                PojoAndDtoTestGenerator.create_pojo_and_dto_rand_gen_code(table, resources_file, "dto")
            # this may not be needed?
            # elif linestr.find("QQQ")>-1:
            #    self.create_get_pk_stmt(table,resources_file)
            elif linestr.find("FKSECTION")>-1:
                RestControllerTestGenerator.createForeignKeyCallsTests(table,resources_file)
            else:
                resources_file.write(linestr.replace("%",table.camelcasejavaname).replace("&",table.lowercasename).replace("^",Configuration.author))
        resources_file.close()

    @staticmethod
    def create_get_pk_stmt(table,file):
        """

        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        file.write(tabs+tabs+"int num = "+table.lowercasename+".get")
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                file.write(fielddata.gettername+"();\n")

    @staticmethod
    def create_controller_test_class_for_mid_level(mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        create the test controller class for mid-level projects
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :return:
        """
        # create the file and open
        filename = mid_lvl_proj.toptestpackage + "/" + Constants.pckg_contr + "/" + mid_lvl_proj.camelcasejavaname + "ControllerTest.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller/controller_mid_lvl_test.txt", "r")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in test_controller:
            linestr = str(line)
            if (linestr.find("XXX")) > -1:
                resources_file.write(
                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + ".*;\n")
                resources_file.write(
                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + ".*;\n")
                resources_file.write(
                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_util + ".Randomizer;\n")
                resources_file.write(
                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_bus + "." + mid_lvl_proj.camelcasejavaname + "Business;\n")
            elif (linestr.find("YYY") > -1):
                RestControllerTestGenerator.create_controller_business_calls_for_mid_level(mid_lvl_proj,
                        crud_proj_names, crud_proj_data,resources_file)
            else:
                resources_file.write(
                    linestr.replace("$", mid_lvl_proj.rootpackage).replace("%", mid_lvl_proj.camelcasejavaname).replace(
                        "&", mid_lvl_proj.lowercasename).replace("^", Configuration.author))
        resources_file.close()
        test_controller.close()

    @staticmethod
    def create_controller_business_calls_for_mid_level(mid_lvl_proj, crud_proj_names, crud_proj_data,
                                                       resources_file):
        """
        this method will create the 5 select, select all, insert, update, and delete test calls for each of the controller methods
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = Constants.tab
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.tablenames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    tabledata = currentproject.tabledata[tablename]
                    tablefile = test_controller = open("files/controller/controller_test_inner.txt", "r")
                    for line in tablefile:
                        linestr = str(line)
                        if linestr.find("IMPORT_SECTION") > -1:
                            PojoAndDtoTestGenerator.create_pojo_and_dto_rand_gen_code(tabledata, resources_file, "dto")
                        else:
                            resources_file.write(
                            linestr.replace("%",tabledata.camelcasejavaname).replace(
                                "&", tabledata.lowercasename).replace("^",mid_lvl_proj.lowercasename))
                    tablefile.close()

    @staticmethod
    def createForeignKeyCallsTests(table, resources_file):
        """
        create the tester methods for the foreign key calls in the RestCOntroler classes
        :param table:
        :param resources_file:
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
                datatypes.append("@PathVariable " + Utilities.translateDataType(field.datatype) + " id" + str(counter))
                inputparameters.append("1")
                resources_file.write(tabs + Constants.doc_test_get_fk.replace("z",field.javaname)
                                     .replace("^",table.camelcasejavaname)+"\n")
                resources_file.write(tabs + "@Test\n")
                resources_file.write(tabs + "public void testGetBy" + field.gettername +
                    "() throws URISyntaxException {\n")
                resources_file.write(tabs*2 + "int num = 1;\n")
                resources_file.write(tabs*2 +
                    'final String baseUrl = "http://localhost:" + randomServerPort + "/' + table.lowercasename + '/findBy' +
                                     field.gettername + '/" + num;\n')
                resources_file.write(tabs * 2 + "URI uri = new URI(baseUrl);\n")
                resources_file.write(tabs * 2 + "HttpEntity<String> request = new HttpEntity<>(new String());\n")
                resources_file.write(tabs * 2 +
                    "ResponseEntity<String> result = restTemplate.exchange(uri, HttpMethod.GET, request, String.class);\n")
                resources_file.write(tabs * 2 + "assertEquals(200, result.getStatusCodeValue());\n")
                resources_file.write(tabs + "}\n\n")
                counter +=1
        if len(compoundFK)>1:
            compoundFKstr = "And".join(compoundFK)
            resources_file.write(tabs + Constants.doc_test_get_by_all_fk.replace("z", compoundFKstr)
                                 .replace("^", table.camelcasejavaname)+"\n")
            resources_file.write(tabs + "@Test\n")
            text = tabs + "public void testGetBy" + compoundFKstr +"() throws URISyntaxException {\n"
            resources_file.write(text)
            # resources_file.write(tabs + Constants.ann_get_mult_fk_maps.replace("^", compoundFKstr)
            # .replace("X", "{" + "}/{".join(inputparameters) + "}") + "\n")
            #
            resources_file.write(tabs * 2 + "int num = 1;\n")
            resources_file.write(tabs * 2 +
                                 'final String baseUrl = "http://localhost:" + randomServerPort + "/' + table.lowercasename +
                                 '/findBy' + compoundFKstr + '/' + '/'.join(inputparameters) + '";\n')
            resources_file.write(tabs * 2 + "URI uri = new URI(baseUrl);\n")
            resources_file.write(tabs * 2 + "HttpEntity<String> request = new HttpEntity<>(new String());\n")
            resources_file.write(tabs * 2 +
                                 "ResponseEntity<String> result = restTemplate.exchange(uri, HttpMethod.GET, request, String.class);\n")
            resources_file.write(tabs * 2 + "assertEquals(200, result.getStatusCodeValue());\n")
            resources_file.write(tabs + "}\n\n")
