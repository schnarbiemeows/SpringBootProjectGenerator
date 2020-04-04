
class Constants:


# general constants
    tab = "\t"

# general java imports

    import_serializeable = "import java.io.Serializable;"
    import_arraylist = "import java.util.ArrayList;"
    import_list = "import java.util.List;"
    import_utils = "import java.util.*;"
    import_optional = "import java.util.Optional;"
    import_valid = "import javax.validation.Valid;"
    import_uri = "import java.net.URI;"
    import_date = "import java.util.Date;"
    import_ts = "import java.sql.Timestamp;"
    import_bd = "import java.math.BigDecimal;"
    import_bi = "import java.math.BigInteger;"


# javadoc constants

    doc_main_class = "/**\n *\n * @author ^\n *\n */"
    doc_opn = "/**"
    doc_ret = " * @return ^"
    doc_param = " * @param ^"
    doc_cls = " */"
    doc_str = " *"
    doc_emp = "/**\n * ^\n */\n"
    doc_get_all = "/**\n\t * get all ^ records\n\t * @return Iterable<^>\n\t */\n"
    doc_get_pk = "/**\n\t * get ^ by primary key\n\t * @param id\n\t * @return ^\n\t */\n"
    doc_create = "/**\n\t * create a new ^\n\t * @param ^\n\t * @return ^\n\t */\n"
    doc_update = "/**\n\t * update a ^\n\t * @param ^\n\t * @return ^\n\t */\n"
    doc_delete = "/**\n\t * delete a ^ by primary key\n\t * @param id\n\t */\n"

# pom file
    xml_grp = "<groupId>*</groupId>"
    xml_art = "<artifactId>*</artifactId>"
    xml_name = "<name>*</name>"
    xml_desc = "<description>CRUD application for the * table</description>"

# main application file
# Swagger file
# application.properties

    prop_log = "logging.level.org.springframework = info"
    prop_actuator = "management.endpoints.web.exposure.include=*"
    prop_sec_usr = "spring.security.user.name=username"
    prop_sec_pwd = "spring.security.user.password=password"
    prop_jpa_true = "spring.jpa.show-sql=true"

# pojos

    pckg_pojos = "pojos"
    import_entity = "import javax.persistence.Entity;"
    import_genval = "import javax.persistence.GeneratedValue;"
    import_gentype = "import javax.persistence.GenerationType;"
    import_id = "import javax.persistence.Id;"
    import_past = "import javax.validation.constraints.Past;"
    import_size = "import javax.validation.constraints.Size;"
    import_notnull = "import javax.validation.constraints.NotNull"
    ann_entity = "@Entity"
    ann_table = '@Table(name = "*")'
    ann_id = "@Id"
    ann_autogen = "@GeneratedValue(strategy=GenerationType.AUTO)"
    ann_column = '@Column(name = "*")'
    ann_override = "@Override"
    ann_sizemin = '@Size(min = *, message = "* must be at least * characters")'
    ann_sizemax = '@Size(max = *, message = "* can be no more than * characters")'
    ann_notnull = '@NotNull(message = "* may not be null")'
    str_tostring = "public String toString() "
    str_super = "super();"

# controllers

    pckg_contr = "controllers"
    import_ctrl_anns = "import org.springframework.web.bind.annotation.*;"
    import_autowired = "import org.springframework.beans.factory.annotation.Autowired;"
    import_getmapping = "import org.springframework.web.bind.annotation.GetMapping;"
    import_postmapping = "import org.springframework.web.bind.annotation.PostMapping;"
    import_reqbdy = "import org.springframework.web.bind.annotation.RequestBody;"
    import_delmapping = "import org.springframework.web.bind.annotation.DeleteMapping;"
    import_putmapping = "import org.springframework.web.bind.annotation.PutMapping;"
    import_pathvar = "import org.springframework.web.bind.annotation.PathVariable;"
    import_rstctrlr = "import org.springframework.web.bind.annotation.RestController;"
    import_respentity = "import org.springframework.http.ResponseEntity;"
    import_https_status = "import org.springframework.http.HttpStatus;"
    ann_restctrlr = "@RestController"
    ann_root_mapping = '@RequestMapping(path="/*")'
    ann_autowired = "@Autowired"
    ann_getmapping = '@GetMapping(path = "/*")'
    ann_getsinglemapping = '@GetMapping(path = "/findById/{id}")'
    ann_postmapping = '@PostMapping(path = "/*")'
    ann_delmapping = '@DeleteMapping(path = "/*/{id})'
    ann_pathvar = "@PathVariable"
    ann_reqbody = "@RequestBody"

# repository

    pckg_repo = "services"
    import_repo = "import org.springframework.data.repository.CrudRepository;"
    import_pojo = "import %;"
    class_decl_repo = "public interface *Repository extends CrudRepository<*, Integer>{\n\n}"