from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *

class PojoAndDtoGenerator:
    """
        class for generating the JPA Entity objects and Data Transfer(DTO) objects
    """
    def __init__(self):
        """

        :param self:
        :return:
        """
        None

    @staticmethod
    def create_pojo_and_dto_classes(table, src, tabledata):
        """
        this method will make the POJOs and the DTO objects from each Table object
        :param table:
        :param src:
        :param tabledata:
        :return:
        """
        # create the file and open
        filename = ''
        if src == "pojo":
            filename = table.topmainpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + ".java"
            """
            if len(table.primarykeys)>1:
                pkfilename = table.topmainpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + "PK.java"
                PojoAndDtoGenerator.make_primary_key_class(table,pkfilename,src)
            """
        else:
            filename = table.topmainpackage + "/" + Constants.pckg_dtos + "/" + table.dtoname + ".java"
        resources_file = open(filename, "w")
        # create the package statement
        PojoAndDtoGenerator.create_package_stmt(table,resources_file,src)
        # create the imports
        PojoAndDtoGenerator.create_imports(table,resources_file,src)
        # create the main class declaration with javadoc
        PojoAndDtoGenerator.create_class_decl(table,resources_file,src)
        # create the fields
        PojoAndDtoGenerator.create_the_fields(table, resources_file,src, tabledata)
        # create the default constructor
        PojoAndDtoGenerator.create_def_constr(table, resources_file,src)
        # create the field constructor
        PojoAndDtoGenerator.create_field_constr(table, resources_file,src, False,tabledata)
        # create the getters and setters
        PojoAndDtoGenerator.create_get_n_set(table,resources_file,src)
        # create the toString
        PojoAndDtoGenerator.create_tostring(table, resources_file,src,tabledata)
        # create the GSON json --> object conversion method
        PojoAndDtoGenerator.create_gson_conv(table, resources_file,src)
        # create the static dto <--> pojo conversion method
        PojoAndDtoGenerator.create_dto_pojo_conv(table, resources_file, src,tabledata)
        # finish the class with a trailing }
        resources_file.write("}\n")
        resources_file.close()

    @staticmethod
    def make_primary_key_class(table, pkfilename, src):
        """
        TODO - split this out into smaller methods
        :param table:
        :param pkfilename:
        :param src:
        :return:
        """
        tabs = Constants.tab
        resources_file = open(pkfilename, "w")
        PojoAndDtoGenerator.create_package_stmt(table,resources_file,src)
        PojoAndDtoGenerator.create_imports(table, resources_file, src)
        resources_file.write("import java.io.*;\n")
        resources_file.write("import javax.persistence.Embeddable;\n\n")
        resources_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        resources_file.write("@Embeddable\n")

        adjustedtablename = table.tablename.replace(Constants.tick_space_repl, " ")
        resources_file.write("public class " + table.camelcasejavaname + "PK implements Serializable {\n" +
            tabs + "// default serial version id, required for serializable classes\n" +
            tabs + "private static final long serialVersionUID = 1L;\n\n")
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                # create the field
                PojoAndDtoGenerator.create_field(fielddata, resources_file)
                # make the getter
                resources_file.write(
                    tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
                # make the setter
                resources_file.write(
                    tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")
        # make the constructor
        PojoAndDtoGenerator.create_def_constr(table, resources_file, src)
        PojoAndDtoGenerator.create_field_constr(table, resources_file,src,True)
        PojoAndDtoGenerator.createEqandHashCde(table,resources_file)
        resources_file.write("}\n")
        resources_file.close()

    @staticmethod
    def create_package_stmt(table, file, src):
        """
        create the package statement
        :param table:
        :param file:
        :return:
        """
        if src == "pojo":
            file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
        else:
                    file.write("package " + table.rootpackage + "." + Constants.pckg_dtos + ";\n\n")

    @staticmethod
    def create_imports(table, file, src):
        """
        create the imports
        :param table:
        :param file:
        :return:
        """
        if src == "pojo":
            file.write("import " + table.rootpackage + "." + Constants.pckg_dtos + "." + table.dtoname + ";\n")
            file.write("import javax.persistence.*;\n")
        else:
            file.write("import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ";\n")
            file.write("import javax.validation.constraints.*;\n")
        file.write("import java.io.Serializable;\n")
        file.write("import com.google.gson.Gson;\n")
        file.write("import java.math.*;\n")
        #file.write("import java.sql.*;\n")
        file.write("import java.util.*;\n\n")
        if Configuration.use_logging == True:
            file.write(Constants.import_logger_1 + "\n")
            file.write(Constants.import_logger_2 + "\n")

    @staticmethod
    def create_class_decl(table, file, src):
        """
        create the POJO class declaration
        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        file.write(Constants.doc_main_class.replace("^",Configuration.author)+"\n")
        if src == "pojo":
            adjustedtablename = table.tablename.replace(Constants.tick_space_repl, " ")
            file.write(Constants.ann_entity+"\n")
            uniquekeylist = ''
            if len(table.uniquekeys)>0:
                keylist = []
                for item in table.uniquekeys:
                    # item is a list: could be a compound key
                    itemlist = Constants.ann_unq_id + '","'.join(item)+'"})'
                    keylist.append(itemlist)
                uniquekeylist = ",".join(keylist)
                file.write(Constants.ann_table_with_keys.replace("*", adjustedtablename).replace("XXX",uniquekeylist) + "\n")
            else:
                file.write(Constants.ann_table.replace("*",adjustedtablename)+"\n")
            file.write("public class " + table.camelcasejavaname + " implements Serializable {\n" +
                tabs + "// default serial version id, required for serializable classes\n" +
                tabs + "private static final long serialVersionUID = 1L;\n\n")
            if Configuration.use_logging == True:
                file.write(tabs + Constants.logger_singleton + "\n\n")
        else:
            file.write("public class " + table.dtoname + " implements Serializable {\n" +
                tabs + "// default serial version id, required for serializable classes\n" +
                tabs + "private static final long serialVersionUID = 1L;\n\n")
            if Configuration.use_logging == True:
                file.write(tabs + Constants.logger_singleton + "\n\n")

    @staticmethod
    def create_the_fields(table, file, src, tabledata):
        """
        create the POJO fields
        :param table:
        :param file:
        :return:

        tabs = Constants.tab
        compoundPK = False
        sharedPK = False
        hasFK = False
        hasParKey = False
        fknames = []
        parkeynames = []
        bothnames = []
        neithernames = []
        if src == "pojo":
            if len(table.primarykeys)>1:
                compoundPK = True
            # do the primary keys first
            if compoundPK == True:
                PojoAndDtoGenerator.create_object_javadoc("compound primary key",file)
                file.write(tabs+"@EmbeddedId\n")
                file.write(tabs+"private "+table.camelcasejavaname+"PK compoundKey;\n\n")
                PojoAndDtoGenerator.create_get_n_set_for_pk(table, file, True)
            else:
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == True:
                        fielddata = table.fielddata[field]
                        # create the javadoc comment
                        PojoAndDtoGenerator.create_field_javadoc(fielddata, file)
                        # create the annotations
                        PojoAndDtoGenerator.create_field_ann(fielddata, file, src)
                        # create the field
                        PojoAndDtoGenerator.create_field(fielddata, file)
                        PojoAndDtoGenerator.create_get_n_set_for_pk(table, file, False)
            # then, go through and find all of the foreign keys
            if len(table.fksymbolnames)>0:
                file.write(tabs + "/*\n")
                for symbolname in table.fksymbolnames:
                    fksymboldata = table.fksymboldata[symbolname]
                    firstitem = fksymboldata[0]
                    childfield = table.fielddata[firstitem[0]]
                    parenttable = tabledata[firstitem[1]]
                    relationship = ''
                    # work on the annotations for the foreign key object
                    PojoAndDtoGenerator.create_object_javadoc(parenttable.camelcasejavaname+" foreign key", file)
                    if childfield.isprimary == True:
                        relationship = "@OneToOne"
                        file.write(tabs + relationship + "\n")
                        file.write(tabs + "@MapsId" + "\n")
                    else:
                        if childfield.unique == False:
                            relationship = "@ManyToOne" # (cascade = CascadeType.ALL)
                        else:
                            relationship = "@OneToOne" # (cascade = CascadeType.ALL)
                        file.write(tabs + relationship + "\n")
                        if len(fksymboldata) >1:
                            file.write(tabs + '@JoinColumns({\n')
                            count = 0
                            for item in fksymboldata:
                                if count == len(fksymboldata)-1:
                                    file.write(
                                        tabs*2 + '@JoinColumn(name = "' + item[0].replace(Constants.tick_space_repl, " ") + '", referencedColumnName = "' + item[
                                            2] + '", insertable=false, updatable=false)\n' + tabs + '})\n')
                                else:
                                    file.write(tabs*2 + '@JoinColumn(name = "' + item[0].replace(Constants.tick_space_repl, " ") + '", referencedColumnName = "' + item[2].replace(Constants.tick_space_repl, " ") + '", insertable=false, updatable=false),\n')
                                count += 1
                        else:
                            file.write(
                                tabs + '@JoinColumn(name = "' + fksymboldata[0][0].replace(Constants.tick_space_repl, " ") + '", referencedColumnName = "' + fksymboldata[0][2].replace(Constants.tick_space_repl, " ") + '", insertable=false, updatable=false)\n')
                    file.write(tabs + "private " + parenttable.camelcasejavaname + " " + parenttable.lowercasename + ";\n\n")
                    PojoAndDtoGenerator.create_object_javadoc(parenttable.camelcasejavaname + " foreign key getter", file)
                    file.write(
                        tabs + "public " + parenttable.camelcasejavaname + " get" + parenttable.camelcasejavaname + "() {\n" + tabs + tabs + "return " + parenttable.lowercasename + ";\n" + tabs + "}\n\n")
                    # make the setter
                    PojoAndDtoGenerator.create_object_javadoc(parenttable.camelcasejavaname + " foreign key setter", file)
                    file.write(
                        tabs + "public void set" + parenttable.camelcasejavaname + "(" + parenttable.camelcasejavaname + " " + parenttable.lowercasename + ") {\n" + tabs + tabs + "this." + parenttable.lowercasename + "=" + parenttable.lowercasename + ";\n" + tabs + "}\n\n")
                file.write(tabs + "*/\n")
            # then go through all of the parent keys
            if len(table.parentkeysymbolnames) > 0:
                file.write(tabs + "/*\n")
                for symbolname in table.parentkeysymbolnames:
                    pksymboldata = table.parentkeysymboldata[symbolname]
                    firstitem = pksymboldata[0]
                    childtable = tabledata[firstitem[1]]
                    childfield = childtable.fielddata[firstitem[2]]
                    # RATS, need to pass in all the tables to get the child table to figure out the relationship
                    # AND to figure out if this is a Shared PK, because I gotta look at the field.primarykey property!
                    relationship = ''
                    PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " child key", file)
                    if childfield.isprimary == True:
                        relationship = '@OneToOne(mappedBy = "'+table.lowercasename+'")' # , cascade = CascadeType.ALL
                        file.write(tabs + relationship + "\n")
                    else:
                        if childfield.unique == False:
                            relationship = '@OneToMany(mappedBy = "'+table.lowercasename+'")' # , cascade = CascadeType.ALL
                            file.write(tabs + relationship + "\n")
                            file.write(
                                tabs + "private List<" + childtable.camelcasejavaname + "> " + childtable.lowercasename + "s;\n\n")
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " child key getter", file)
                            file.write(
                                tabs + "public List<" + childtable.camelcasejavaname + "> get" + childtable.camelcasejavaname + "s() {\n" + tabs + tabs + "return " + childtable.lowercasename + "s;\n" + tabs + "}\n\n")
                            # make the setter
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " child key setter", file)
                            file.write(
                                tabs + "public void set" + childtable.camelcasejavaname + "s(List<" + childtable.camelcasejavaname + "> " + childtable.lowercasename + "s) {\n" + tabs + tabs + "this." + childtable.lowercasename + "s=" + childtable.lowercasename + "s;\n" + tabs + "}\n\n")
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " add a child key", file)
                            file.write(
                                tabs + "public " + childtable.camelcasejavaname + " add" + childtable.camelcasejavaname + "("+ childtable.camelcasejavaname +
                                " " + childtable.lowercasename + ") {\n" +
                                tabs + tabs + "get" + childtable.camelcasejavaname + "s().add(" + childtable.lowercasename + ");\n" +
                                tabs*2 + childtable.lowercasename + ".set" + table.camelcasejavaname +"(this);\n" +
                                tabs*2 + "return " + childtable.lowercasename + ";\n"+ tabs + "}\n\n")
                            # make the setter
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " remove a child key", file)
                            file.write(
                                tabs + "public " + childtable.camelcasejavaname + " remove" + childtable.camelcasejavaname + "(" + childtable.camelcasejavaname +
                                " " + childtable.lowercasename + ") {\n" +
                                tabs + tabs + "get" + childtable.camelcasejavaname + "s().remove(" + childtable.lowercasename + ");\n" +
                                tabs * 2 + childtable.lowercasename + ".set" + table.camelcasejavaname + "(null);\n" +
                                tabs * 2 + "return " + childtable.lowercasename + ";\n" + tabs + "}\n\n")
                        else:
                            relationship = '@OneToOne(mappedBy = "'+table.lowercasename+'")' # , cascade = CascadeType.ALL
                            file.write(tabs + relationship + "\n")
                            file.write(tabs + "private " + childtable.camelcasejavaname + " " + childtable.lowercasename + ";\n\n")
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " child key getter", file)
                            file.write(tabs + "public " + childtable.camelcasejavaname + " get" + childtable.camelcasejavaname + "() {\n" + tabs + tabs + "return " + childtable.lowercasename + ";\n" + tabs + "}\n\n")
                            # make the setter
                            PojoAndDtoGenerator.create_object_javadoc(childtable.camelcasejavaname + " child key setter", file)
                            file.write(tabs + "public void set" + childtable.camelcasejavaname + "(" + childtable.camelcasejavaname + " " + childtable.lowercasename + ") {\n" + tabs + tabs + "this." + childtable.lowercasename + "=" + childtable.lowercasename + ";\n" + tabs + "}\n\n")
                file.write(tabs + "*/\n")
            # finally, make the fields only for those fields that are neither PKs, FKs, or Parent keys
            # FOR EACH FIELD:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == False:
                    # create the javadoc comment
                    PojoAndDtoGenerator.create_field_javadoc(fielddata, file)
                    # create the annotations
                    PojoAndDtoGenerator.create_field_ann(fielddata, file, src)
                    # create the field
                    PojoAndDtoGenerator.create_field(fielddata, file)
        else:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                # create the javadoc comment
                PojoAndDtoGenerator.create_field_javadoc(fielddata, file)
                # create the annotations
                PojoAndDtoGenerator.create_field_ann(fielddata, file, src)
                # create the field
                PojoAndDtoGenerator.create_field(fielddata, file)
        """
        # FOR EACH FIELD:
        count = 0
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            # create the javadoc comment
            PojoAndDtoGenerator.create_field_javadoc(fielddata, file)
            # create the annotations
            count = PojoAndDtoGenerator.create_field_ann(fielddata, file, src, count)
            # create the field
            PojoAndDtoGenerator.create_field(fielddata, file)

    @staticmethod
    def create_object_javadoc(msg,file):
        """
        create the javadoc for the compound primary key and foreign key fields
        :param msg:
        :param file:
        :return:
        """
        tabs = Constants.tab
        text = tabs + Constants.doc_opn + "\n" + tabs + Constants.doc_str + " ^\n" + tabs + Constants.doc_cls + "\n"
        file.write(text.replace("^",msg))

    @staticmethod
    def create_field_javadoc(fielddata, file):
        """
        create the field's javadoc
        :param fielddata:
        :param file:
        :return:
        """
        tabs = Constants.tab
        text = tabs + Constants.doc_opn + "\n" + tabs + Constants.doc_str + " ^\n" + tabs + Constants.doc_cls + "\n"
        if(len(fielddata.comment)>0):
            text = text.replace("^",fielddata.comment)
        else:
            text = text.replace("^","")
        file.write(text)

    @staticmethod
    def create_field_ann(fielddata, file, src, count):
        """
        create the field annotations
        :param fielddata:
        :param file:
        :param src:
        :param count:
        :return:
        """
        tabs = Constants.tab
        if src == "pojo":
            # these are the JPA annotations
            file.write(tabs+Constants.ann_column.replace("*",fielddata.name.replace(Constants.tick_space_repl, " "))+"\n")
            if(fielddata.isprimary == True):
                file.write(tabs+Constants.ann_id+"\n")
            #if (fielddata.primarytype != None and fielddata.isforeignkey == False):
            #    file.write(tabs+Constants.ann_autogen + "\n")
            if (fielddata.primarytype != None and count == 0):
                file.write(tabs + Constants.ann_autogen + "\n")
                count +=1   # just in case there is a compound primary key, only the first field is autogenerated
        return count
        #else:
            # these are the possible DTO validation annotations
        #    if(fielddata.canbenull == False):
        #        file.write(tabs+Constants.ann_notnull.replace("*", fielddata.name)+"\n")
        #    if (fielddata.lengthreq == True):
        #        file.write(tabs+Constants.ann_sizemax.replace("*", str(fielddata.length),1).replace("*",fielddata.name,1).replace("*",str(fielddata.length),1)+"\n")

    @staticmethod
    def create_field(fielddata, file):
        """
        create the field declaration
        :param fielddata:
        :param file:
        :return:
        """
        tabs = Constants.tab
        if fielddata.datatype == "Timestamp":
            file.write(tabs + "private java.sql.Timestamp "  + fielddata.javaname + ";\n\n")
        elif fielddata.datatype == "Time":
            file.write(tabs + "private java.sql.Time "  + fielddata.javaname + ";\n\n")
        else:
            file.write(tabs + "private " + fielddata.datatype + " " + fielddata.javaname + ";\n\n")

    @staticmethod
    def create_def_constr(table, file, src):
        """
        create the default constructor
        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        PojoAndDtoGenerator.create_object_javadoc("default constructor", file)
        if src == "pojo":
            file.write(tabs + "public " + table.camelcasejavaname + "() {\n" + tabs + tabs + "super();\n" + tabs + "}\n\n")
        else:
            file.write(
                tabs + "public " + table.dtoname + "() {\n" + tabs + tabs + "super();\n" + tabs + "}\n\n")

    @staticmethod
    def create_field_constr(table, file, src, embeddedPK, tables=None):
        """
        create the field constructor
        :param table:
        :param file:
        :param src:
        :param embeddedPK:
        :param tables:
        :return:

        tabs = Constants.tab
        text = ""
        PojoAndDtoGenerator.create_object_javadoc("field constructor", file)
        if src == "pojo":
            # this piece is for creating the constructor in the PK classes
            if embeddedPK == True:
                text = tabs + "public " + table.camelcasejavaname + "PK("
                # then do the rest of the fields
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == True:
                        text += fielddata.datatype + " " + fielddata.javaname + ", "
                text = text[0:-2]
                text += ") {\n"
                file.write(text)
                # inside the constructor
                file.write(tabs + tabs + Constants.str_super + "\n")
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if (embeddedPK and fielddata.isprimary == True) or not embeddedPK:
                        file.write(tabs + tabs + "this." + fielddata.javaname + " = " + fielddata.javaname + ";\n")
                file.write(tabs + "}\n\n")
            # this is for the regular classes
            else:
                text = tabs + "public " + table.camelcasejavaname + "("
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    text += fielddata.datatype + " " + fielddata.javaname + ", "
                text = text[0:-2]
                text += ") {\n"
                file.write(text)
                # inside the constructor
                file.write(tabs + tabs + Constants.str_super + "\n")
                # first do any regular primary keys
                if len(table.primarykeys) > 1:
                    file.write(
                        tabs + tabs + "this.compoundKey = new " + table.camelcasejavaname + "PK() ;\n")
                    for item in table.primarykeys:
                        fielddata = table.fielddata[item]
                        file.write(
                            tabs + tabs + "this.compoundKey.set" + fielddata.gettername + "(" + fielddata.javaname + ") ;\n")
                else:
                    for field in table.fieldnames:
                        fielddata = table.fielddata[field]
                        if fielddata.isprimary:
                            file.write(
                                tabs + tabs + "this." + fielddata.javaname + " = " + fielddata.javaname + " ;\n")
                # then do any foreign objects
                for symbolname in table.fksymbolnames:
                    fksymboldata = table.fksymboldata[symbolname]
                    firstitem = fksymboldata[0]
                    parenttable = tables[firstitem[1]]
                    file.write(
                        tabs + tabs + "this." + parenttable.lowercasename + " = new " + parenttable.camelcasejavaname + "() ;\n")
                    for item in fksymboldata:
                        fielddata = parenttable.fielddata[item[2]]
                        file.write(
                            tabs + tabs + "this." + parenttable.lowercasename + ".set" + fielddata.gettername + "(" + fielddata.javaname + ") ;\n")
                # then do the rest of the fields
                for field in table.fieldnames:
                    fielddata = table.fielddata[field]
                    if fielddata.isprimary == False and fielddata.isforeignkey == False and fielddata.isparentkey == False:
                        file.write(
                            tabs + tabs + "this." + fielddata.javaname + " = " + fielddata.javaname + " ;\n")
                file.write(tabs + "}\n\n")


        # DTO field constructor
        else:
            text = tabs + "public " + table.dtoname + "("
            # FOR EACH FIELD:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if (embeddedPK and fielddata.isprimary == True) or not embeddedPK:
                    text += fielddata.datatype + " " + fielddata.javaname + ", "
            text = text[0:-2]
            text += ") {\n"
            file.write(text)
            # inside the constructor
            file.write(tabs+tabs+Constants.str_super+"\n")
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if (embeddedPK and fielddata.isprimary == True) or not embeddedPK:
                    file.write(tabs+tabs+"this."+fielddata.javaname+" = "+fielddata.javaname+";\n")
            file.write(tabs+"}\n\n")
        """
        tabs = Constants.tab
        if src == "pojo":
            text = tabs + "public " + table.camelcasejavaname + "("
        else:
            text = tabs + "public " + table.dtoname + "("
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += fielddata.datatype + " " + fielddata.javaname + ", "
        text = text[0:-2]
        text += ") {\n"
        file.write(text)
        file.write(tabs + tabs + Constants.str_super + "\n")
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            file.write(tabs + tabs + "this." + fielddata.javaname + " = " + fielddata.javaname + ";\n")
        file.write(tabs + "}\n\n")

    @staticmethod
    def create_get_n_set_for_pk(table, file, compoundPk=False):
        """
        make the getter and setter for a primary key
        :param table:
        :param compoundPk:
        :return:
        """
        tabs = Constants.tab
        if compoundPk == True:
            PojoAndDtoGenerator.create_object_javadoc("compound primary key getter", file)
            file.write(
                tabs + "public " + table.camelcasejavaname + "PK getCompoundKey() {\n" + tabs + tabs + "return this.compoundKey;\n" + tabs + "}\n\n")
            # make the setter
            PojoAndDtoGenerator.create_object_javadoc("compound primary key setter", file)
            file.write(
                tabs + "public void setCompoundKey(" + table.camelcasejavaname + "PK compoundKey) {\n" + tabs + tabs + "this.compoundKey = compoundKey;\n" + tabs + "}\n\n")
        else:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == True:
                    PojoAndDtoGenerator.create_object_javadoc("primary key getter", file)
                    file.write(
                        tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
                    # make the setter
                    PojoAndDtoGenerator.create_object_javadoc("primary key getter", file)
                    file.write(
                        tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")

    @staticmethod
    def create_get_n_set(table, file, src):
        """
        create the getters and setters
        :param table:
        :param file:
        :param src:
        :return:

        tabs = Constants.tab
        if src == "pojo":
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isforeignkey == False and fielddata.isprimary == False:
                    PojoAndDtoGenerator.create_object_javadoc(fielddata.javaname+" getter",file)
                    file.write(
                        tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
                    PojoAndDtoGenerator.create_object_javadoc(fielddata.javaname+" setter", file)
                    file.write(
                        tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")
        else:
            # FOR EACH FIELD:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                file.write(tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
                file.write(tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")
        """
        tabs = Constants.tab
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            file.write(
                tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
            file.write(
                tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")

    @staticmethod
    def create_tostring(table, file, src, tabledata):
        """
        create the toString method
        :param table:
        :param file:
        :param src:
        :param tabledata:
        :return:

        tabs = Constants.tab
        file.write(tabs + Constants.ann_override + "\n" + tabs + Constants.str_tostring + "{\n")
        if src == "pojo":
            text = 'return "' + table.camelcasejavaname + ' ['
            # primary keys
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary:
                    if len(table.primarykeys) > 1:
                        text += fielddata.javaname + ' = " + this.compoundKey.get' + fielddata.gettername + '() + ", '
                    else:
                        text += fielddata.javaname + ' = " + ' + fielddata.javaname + ' + ", '
            # foreign keys
            for symbolname in table.fksymbolnames:
                fksymboldata = table.fksymboldata[symbolname]
                firstitem = fksymboldata[0]
                parenttable = tabledata[firstitem[1]]
                for item in fksymboldata:
                    childfielddata = table.fielddata[item[0]]
                    fielddata = parenttable.fielddata[item[2]]
                    text += childfielddata.javaname + ' = " + ' + parenttable.lowercasename + ".get" + fielddata.gettername + '() + ", '

            # then do the rest of the fields
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == False and fielddata.isforeignkey == False and fielddata.isparentkey == False:
                    text += fielddata.javaname + '=" + ' + fielddata.javaname + ' + ", '
            text = text[0:-3] + '"]";'
            file.write(tabs + tabs + text + "\n" + tabs + "}\n\n")
        else:
            text = 'return "' + table.dtoname + ' ['
            # FOR EACH FIELD:
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                text += fielddata.javaname + '=" + ' + fielddata.javaname + ' + ", '
            text = text[0:-3] + '"]";'
            file.write(tabs+tabs+text+"\n"+tabs+"}\n\n")
        """
        tabs = Constants.tab
        file.write(tabs + Constants.ann_override + "\n" + tabs + Constants.str_tostring + "{\n")
        if src == "pojo":
            text = 'return "' + table.camelcasejavaname + ' ['
        else:
            text = 'return "' + table.dtoname + ' ['
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += fielddata.javaname + '=" + ' + fielddata.javaname + ' + ", '
        text = text[0:-3] + '"]";'
        file.write(tabs + tabs + text + "\n" + tabs + "}\n\n") \

    @staticmethod
    def create_gson_conv(table, file, src):
        """
        create the static gson json->object converter
        :param table:
        :param file:
        :param src:
        :return:
        """
        tabs = Constants.tab
        name = ""
        if src == "pojo":
            name = table.camelcasejavaname
        else:
            name = table.dtoname
        file.write(tabs + "public static " + name + " fromJson(String input) {\n")
        file.write(tabs + tabs + "Gson gson = new Gson();\n")
        file.write(tabs + tabs +"return gson.fromJson(input, " + name + ".class );\n")
        file.write(tabs + "}\n")

    @staticmethod
    def create_dto_pojo_conv(table, file, src, tabledata):
        """
        this method will create the method to convert from Pojo to DTO or DTO to Pojo
        :param table:
        :param file:
        :param src:
        :param tabledata:
        :return:

        tabs = Constants.tab
        text = ''
        if src == "pojo":
            file.write(tabs + "public " + table.dtoname + " toDTO() {\n")
            file.write(tabs + tabs + "return new " + table.dtoname + "(")

            # primary keys
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary:
                    if len(table.primarykeys) > 1:
                        text += 'this.compoundKey.get' + fielddata.gettername + '(), '
                    else:
                        text += 'this.get' + fielddata.gettername + '(), '
            # foreign keys
            for symbolname in table.fksymbolnames:
                fksymboldata = table.fksymboldata[symbolname]
                firstitem = fksymboldata[0]
                parenttable = tabledata[firstitem[1]]
                for item in fksymboldata:
                    childfielddata = table.fielddata[item[0]]
                    fielddata = parenttable.fielddata[item[2]]
                    text += 'this.' + parenttable.lowercasename + ".get" + fielddata.gettername + '(), '

            # then do the rest of the fields
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                if fielddata.isprimary == False and fielddata.isforeignkey == False and fielddata.isparentkey == False:
                    text += "this.get" + fielddata.gettername + "(),"
            text = text[0:-1] + ");\n"
            file.write(text)
            file.write(tabs + "}\n")
        else:
            file.write(tabs + "public " + table.camelcasejavaname + " toEntity() {\n")
            file.write(tabs + tabs + "return new " + table.camelcasejavaname + "(")
            for field in table.fieldnames:
                fielddata = table.fielddata[field]
                text += "this.get" + fielddata.gettername + "(),"
            text = text[0:-1] + ");\n"
            file.write(text)
            file.write(tabs + "}\n")
        """
        tabs = Constants.tab
        text = ''
        if src == "pojo":
            file.write(tabs + "public " + table.dtoname + " toDTO() {\n")
            file.write(tabs + tabs + "return new " + table.dtoname + "(")
        else:
            file.write(tabs + "public " + table.camelcasejavaname + " toEntity() {\n")
            file.write(tabs + tabs + "return new " + table.camelcasejavaname + "(")
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += "this.get" + fielddata.gettername + "(),"
        text = text[0:-1] + ");\n"
        file.write(text)
        file.write(tabs + "}\n")

    @staticmethod
    def createEqandHashCde(table,file):
        """
        this method will create the equals and hashcode methods for any Primary Key Objects
        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        file.write(tabs + "public boolean equals(Object other) {\n")
        file.write(tabs*2 + "if (this == other) {\n" + tabs*3 + "return true;\n" + tabs*2 + "}\n")
        file.write(tabs*2 + "if (!(other instanceof " + table.camelcasejavaname+"PK)) {\n" + tabs*3 + "return false;\n" + tabs*2 + "}\n")
        file.write(tabs*2 + table.camelcasejavaname+"PK castother = (" + table.camelcasejavaname+"PK)other;\n")
        file.write(tabs*2 + "return\n")
        primarycount = 0
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary:
                primarycount += 1
        count = 0
        # equals
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary:
                if count == 0:
                    file.write(tabs*3 + "this." + fielddata.javaname + ".equals(castother." + fielddata.javaname + ")\n")
                elif count == primarycount-1:
                    file.write(tabs * 3 + "&& this." + fielddata.javaname + ".equals(castother." + fielddata.javaname + ");\n")
                else:
                    file.write(tabs * 3 + "&& this." + fielddata.javaname + ".equals(castother." + fielddata.javaname + ")\n")
                count += 1
        file.write(tabs + "}\n")
        # hashcode
        file.write(tabs + "public int hashcode() {\n")
        file.write(tabs*2 + "final int prime = 31;\n")
        file.write(tabs*2 + "int hash = 17;\n")
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary:
                if fielddata.datatype == "long":
                    file.write(tabs*2 + "hash = hash * prime + ((int) (this." + fielddata.javaname + " ^ (this." + fielddata.javaname + " >>> 32)));\n")
                else:
                    file.write(tabs*2 + "hash = hash * prime + this." + fielddata.javaname + ".hashCode();\n")
        file.write(tabs*2 + "return hash;\n" + tabs + "}\n")