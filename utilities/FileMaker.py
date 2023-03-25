from configuration.Constants import *
from configuration.Configuration import *
from distutils.dir_util import *
import os
from utilities.JsonUtility import JsonUtility, Utilities


class FileMaker:
    
    def __init__(self):
        """
        initilization
        :return: 
        """
   
    @staticmethod 
    def make_postman_for_mid_level( project):
        """
        redirecting to JsonUtility.py make_postman_for_mid_level method
        :param project: 
        :return: 
        """
        JsonUtility.make_postman_for_mid_level(project)

    @staticmethod
    def createPostmanCollection( project):
        """
        redirecting to JsonUtility.py createPostmanCollection method
        :param project:
        :return:
        """
        JsonUtility.createPostmanCollection(project)

    @staticmethod
    def backup_project( project, destinationroot):
        """
        this method will backup a project that has already been generated before, so that the user can retrieve the various files
        that will get overwritten with the current generation
        :param project:
        :param destinationroot:
        :return:
        """
        if os.path.exists(destinationroot+"/"+project.pomname):
            print("backing up project " + project.pomname)
            copy_tree(destinationroot+"/"+project.pomname, destinationroot+"/backup/"+project.pomname)

    @staticmethod
    def make_base_angular_project(project):
        """
        this method will backup a project that has already been generated before, so that the user can retrieve the various files
        that will get overwritten with the current generation
        :param project:
        :param destinationroot:
        :return:
        """
        destination_dir_array = Configuration.angular_dest_directory.split("/")
        directory = ''
        for items in destination_dir_array:
            if len(items)>0:
                directory += "/"+items
            if len(directory) > 1 and not os.path.exists(directory):
                Utilities.mkdir(directory)
        destinationroot = directory
        if not destinationroot.endswith("/"):
            destinationroot += "/"
        if not os.path.exists(destinationroot+project.pomname):
            print("creating Angular project : " + project.pomname)
            Utilities.mkdir(destinationroot+project.pomname)
        return destinationroot+project.pomname

    @staticmethod
    def create_base_project_folders(project, sourceprojectfolder, destinationroot, artifactid, groupid):
        """
        this method will create the basic folder structure of a SB project
        :param project:
        :param sourceprojectfolder:
        :param destinationroot:
        :param artifactid:
        :param groupid:
        :return:
        """
        Utilities.mkdir(destinationroot)
        Utilities.mkdir(destinationroot + "/" + project.pomname)
        Utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname)
        Utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn")
        Utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper")

        Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.jar",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/maven-wrapper.jar")
        Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.properties",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/maven-wrapper.properties")
        Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/MavenWrapperDownloader.java",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/MavenWrapperDownloader.java")

        Utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/src")
        #Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.gitIgnore",
        #              destinationroot + "/" + project.pomname + "/" + project.pomname + "/.gitIgnore")
        Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/mvnw")
        Utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw.cmd",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/mvnw.cmd")
        projectrootpackage = destinationroot + "/" + project.pomname + "/" + project.pomname + "/src/"
        Utilities.mkdir(projectrootpackage + "main")
        Utilities.mkdir(projectrootpackage + "test")
        Utilities.mkdir(projectrootpackage + "main/java")
        Utilities.mkdir(projectrootpackage + "main/resources")
        Utilities.mkdir(projectrootpackage + "test/java")
        projectmainfolder = projectrootpackage + "main/java/"
        project.projectresourcesfolder = projectrootpackage + "main/resources/"
        projecttestfolder = projectrootpackage + "test/java/"
        # how far we have to go into the source folder depends on if the groupId has any periods in it, which each
        # represent its own sub-folder
        packages = groupid.split(".")
        packageslength = len(packages)
        topmainpackage = packages[0]
        toptestpackage = packages[0]
        Utilities.mkdir(projectmainfolder + topmainpackage)
        Utilities.mkdir(projecttestfolder + toptestpackage)
        if packageslength > 1:
            x = range(1, packageslength)
            for n in x:
                topmainpackage += "/" + packages[n]
                toptestpackage += "/" + packages[n]
                Utilities.mkdir(projectmainfolder + topmainpackage)
                Utilities.mkdir(projecttestfolder + toptestpackage)
        # now have to add the artifactID folder to these roots
        topmainpackage += "/" + project.lowercasename
        toptestpackage += "/" + project.lowercasename
        Utilities.mkdir(projectmainfolder + topmainpackage)
        # make subpackages
        Utilities.mkdir(projectmainfolder + topmainpackage + "/config")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/controllers")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/exceptions")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/services")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/dtos")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/proxy")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/dtos")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/pojos")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/services")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/pojos")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/repositories")
        Utilities.mkdir(projectmainfolder + topmainpackage + "/utilities")

        Utilities.mkdir(projecttestfolder + toptestpackage)
        # make subpackages
        Utilities.mkdir(projecttestfolder + toptestpackage + "/config")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/controllers")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/exceptions")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/services")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/dtos")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/proxy")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/dtos")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/pojos")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/services")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/pojos")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/repositories")
        Utilities.mkdir(projecttestfolder + toptestpackage + "/utilities")

        # set the Table object's main java and test package roots
        project.topmainpackage = projectmainfolder + topmainpackage
        project.toptestpackage = projecttestfolder + toptestpackage
        # rootpackage is for the individual Java files' "package ..." statement
        project.rootpackage = topmainpackage.replace("/", ".")
        FileMaker.create_pom_file(project, destinationroot)
        if Configuration.use_logging == True:
            FileMaker.create_logging_file(project, destinationroot)

    @staticmethod
    def create_application_resources_file( project, otherprojectnamesotherprojects = None):
        """
        this method creates the application.properties file for the project
        *** Note: if they chose Configuration.use_config_server = True(chose to use a Spring CLoud config server)
        this method will instead put these properties into a default config file called <pom name>.txt for the config server
        to deploy to GIT. It will also create a file bootstrap.properties, that contains the needed confugration to point to
        the uri of this config server, specified with Configuration.spring_cloud_config_uri
        :param project:
        :return:
        """
        if(Configuration.use_docker == True):
            resources_file = open(project.projectresourcesfolder + "/application.properties", "w")
            resources_file.write("spring.application.name=" + project.pomname + "\n")
            resources_file.write("server.port=" + str(project.portnum) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_log) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_jpa) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_jpa_show) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_hib_nmg) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_hib_seq) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_mysql_conn) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_mysql_usr) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_mysql_pwd) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_actu_conf) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_sec_usr) + "\n")
            resources_file.write(FileMaker.parseProperty(Configuration.app_sec_pwd) + "\n")
            resources_file.close()
        elif(Configuration.use_config_server == True):
            resources_file = open(project.projectresourcesfolder + "/bootstrap.properties", "w")
            resources_file.write(Configuration.app_name + project.pomname + "\n")
            resources_file.write(Configuration.app_port + str(project.portnum) + "\n")
            resources_file.write(Configuration.spring_cloud_config_uri+"\n")
            resources_file.close()
            resources_file = open(Configuration.config_server_git+"/"+project.pomname+".properties", "w")
            resources_file.write(Configuration.app_log + "\n")
            resources_file.write(Configuration.app_jpa + "\n")
            resources_file.write(Configuration.app_jpa_show + "\n")
            resources_file.write(Configuration.app_hib_nmg + "\n")
            resources_file.write(Configuration.app_hib_seq + "\n")
            resources_file.write(Configuration.app_mysql_conn + "\n")
            resources_file.write(Configuration.app_mysql_usr + "\n")
            resources_file.write(Configuration.app_mysql_pwd + "\n")
            resources_file.write(Configuration.app_actu_conf + "\n")
            resources_file.write(Configuration.app_sec_usr + "\n")
            resources_file.write(Configuration.app_sec_pwd + "\n")
            if(Configuration.use_naming_server == True):
                resources_file.write(Configuration.naming_server_url + "\n")
            resources_file.close()
        else:
            resources_file = open(project.projectresourcesfolder + "/application.properties", "w")
            resources_file.write("spring.application.name=" + project.pomname+"\n")
            resources_file.write("server.port="+str(project.portnum)+"\n")
            resources_file.write(Configuration.app_log + "\n")
            resources_file.write(Configuration.app_jpa + "\n")
            resources_file.write(Configuration.app_jpa_show + "\n")
            resources_file.write(Configuration.app_hib_nmg + "\n")
            resources_file.write(Configuration.app_hib_seq + "\n")
            resources_file.write(Configuration.app_mysql_conn + "\n")
            resources_file.write(Configuration.app_mysql_usr + "\n")
            resources_file.write(Configuration.app_mysql_pwd + "\n")
            resources_file.write(Configuration.app_actu_conf + "\n")
            resources_file.write(Configuration.app_sec_usr + "\n")
            resources_file.write(Configuration.app_sec_pwd + "\n")
            if (Configuration.use_naming_server == True):
                resources_file.write(Configuration.naming_server_url + "\n")
            resources_file.close()

    @staticmethod
    def populate_kubernetes_commands_file(project):
        """
        this method will add certain command line commands to run to make our lives easier
        :param project:
        :return:
        """
        destinationfile = open(project.root + "/kubernetes_commands.txt", "w")
        destinationfile.write("cd /c" + project.root.replace("C:\\", "/").replace("\\", "/") + "\n")
        docker_cmd = "docker run -d -p " + str(project.portnum) + ":" + str(project.portnum) + " "
        docker_cmd += Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version + " "
        if project.is_mid_level and Configuration.use_docker:
            for item in project.service_config:
                docker_cmd += "--" + item + "=" + Configuration.docker_localhost_url + " "
        destinationfile.write("-- run the project as a docker image\n")
        destinationfile.write(docker_cmd + "\n\n")
        push_cmd = "docker push " + Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version
        destinationfile.write("-- push the project to the repository\n")
        destinationfile.write(push_cmd + "\n\n")
        kub_config_cmd = "kubectl create configmap " + project.pomname + "-config "
        destinationfile.write("-- command to create the configuration map for this project in kubernetes\n")
        kub_config_cmd += FileMaker.makeParameterList(project)
        destinationfile.write(kub_config_cmd + "\n\n")
        destinationfile.write("-- command to create the secrets map for this project in kubernetes\n")
        kub_secrets_cmd = "kubectl create secret generic " + project.pomname + "-secrets "
        kub_secrets_cmd += FileMaker.addSecretsToKubernetes(project)
        destinationfile.write(kub_secrets_cmd + "\n\n")
        destinationfile.close()

    @staticmethod
    def create_pom_file(project, destinationroot):
        """
        this method will copy the pom.xml while changing some things
        - it needs to change the groupId, artifactId, description, and name fields
        - it needs to add in the swagger2 dependencies(from dependencies.xml file)
        - it needs to add in the com.fasterxml.jackson.dataformat dependency(from dependencies.xml file)
        - it needs to add in the sonarqube and jacoco stuff(from jacoco_props.xml file and sonar_jacoco.xml file)
        :param project:
        :param destinationroot:
        :return:
        """
        oldpom = open("files/demo/demo/pom.xml","r")
        newpom = open(destinationroot + "/" + project.pomname + "/" + project.pomname + "/pom.xml", "w")
        parentpassed = False
        for item in oldpom:
            itemstr = str(item)
            if(parentpassed == False):
                newpom.write(itemstr)
                if(itemstr.find("</parent>")>-1):
                    parentpassed = True
            else:
                if itemstr.find("ADD_GROUP_ID") > -1:
                   newpom.write(itemstr.replace("ADD_GROUP_ID", Configuration.groupid))
                elif itemstr.find("ADD_VERSION") > -1:
                    newpom.write(itemstr.replace("ADD_VERSION", Configuration.version))
                elif itemstr.find("ADD_ARTIFACT_ID") > -1:
                    newpom.write(itemstr.replace("ADD_ARTIFACT_ID", project.pomname))
                elif itemstr.find("ADD_PROJECT_NAME") > -1:
                    newpom.write(itemstr.replace("ADD_PROJECT_NAME", project.pomname))
                elif itemstr.find("ADD_PROJECT_DESCRIPTION") > -1:
                    newpom.write(itemstr.replace("ADD_PROJECT_DESCRIPTION", "CRUD application for the " + project.pomname + " project"))
                elif itemstr.find("IS_LOGGING_ENABLED_1") > -1:
                    if Configuration.use_logging == True:
                        FileMaker.addLoggingExclusion(newpom)
                elif itemstr.find("IS_LOGGING_ENABLED_2") > -1:
                    if Configuration.use_logging == True:
                        FileMaker.addLoggingDependency(newpom)
                elif itemstr.find("SUREFIRE_PLUGIN") > -1:
                    FileMaker.addSurefirePlugin(newpom)
                elif itemstr.find("</properties>") > -1:
                    # jaccoco properties
                    if(Configuration.use_sonar_jacoco == True):
                        jacocoprops = open("files/maven/jacoco_props.xml","r")
                        for prop in jacocoprops:
                            propstr = str(prop)
                            newpom.write(propstr)
                        jacocoprops.close()
                    # cloud config client properties
                    if (Configuration.use_config_server == True or Configuration.use_docker == True or
                            Configuration.use_gateway_server == True or Configuration.use_distributed_tracing == True or
                            Configuration.use_naming_server == True):
                        configclientprop = open("files/maven/config_client_prop.xml", "r")
                        for prop in configclientprop:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientprop.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                elif (itemstr.find("</dependencies>") > -1):
                    dependencies = open("files/maven/dependencies.xml","r")
                    for dep in dependencies:
                        depstr = str(dep)
                        newpom.write(depstr)
                    dependencies.close()
                    if (Configuration.use_docker == True):
                        naming_server_config = open("files/docker_kubernetes/feign.xml", "r")
                        for prop in naming_server_config:
                            propstr = str(prop)
                            newpom.write(propstr)
                        naming_server_config.close()
                        newpom.write("\n")
                    # cloud naming server dependencies
                    if (Configuration.use_naming_server == True):
                        naming_server_config = open("files/maven/feign_dep.xml", "r")
                        for prop in naming_server_config:
                            propstr = str(prop)
                            newpom.write(propstr)
                        naming_server_config.close()
                        newpom.write("\n")
                    # cloud config client dependency
                    if (Configuration.use_config_server == True):
                        configclientdep = open("files/maven/config_client_dep.xml", "r")
                        for prop in configclientdep:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientdep.close()
                    newpom.write("\n")
                    if (Configuration.use_distributed_tracing == True):
                        sleuthfile = open("files/maven/sleuth.xml", "r")
                        for line in sleuthfile:
                            linestr = str(line)
                            newpom.write(linestr)
                        sleuthfile.close()
                        newpom.write("\n")
                    newpom.write(itemstr)
                    # cloud config client dependency management
                    if (Configuration.use_config_server == True or Configuration.use_docker == True or
                            Configuration.use_gateway_server == True or Configuration.use_distributed_tracing == True or
                            Configuration.use_naming_server == True):
                        configclientdepmngmt = open("files/maven/cloud_conf_dep_mngmt.xml", "r")
                        for prop in configclientdepmngmt:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientdepmngmt.close()
                        newpom.write("\n")
                elif (itemstr.find("</plugins>") > -1):
                    if (Configuration.use_sonar_jacoco == True):
                        sonarjacoco = open("files/maven/sonar_jacoco.xml","r")
                        for line in sonarjacoco:
                            linestr = str(line)
                            newpom.write(linestr)
                        sonarjacoco.close()
                    if (Configuration.use_docker == True):
                        sonarjacoco = open("files/docker_kubernetes/docker_plugin.xml","r")
                        for line in sonarjacoco:
                            linestr = str(line)
                            newpom.write(linestr.replace("XXX",Configuration.docker_remote_repo_name))
                        sonarjacoco.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                else:
                    newpom.write(itemstr)
        newpom.close()

    @staticmethod
    def create_logging_file(project, destinationroot):
        """
        this method will create the log4j2 logging file in the src/main/resources directory
        it will also create a single FileAppender log file that is size
        :param project:
        :param destinationroot:
        :return:
        """
        inputloggingfile = open("files/logging/logging.xml", "r")
        outputloggingfile = open(project.projectresourcesfolder + "/log4j2.xml", "w")
        for line in inputloggingfile:
            linestr = str(line)
            if linestr.find("PATTERN_CONFIG")>-1:
                outputloggingfile.write(linestr.replace("PATTERN_CONFIG",Configuration.log_pattern))
            elif linestr.find("ABS_FILE_NAME")>-1:
                filepath = Configuration.root_logging_path
                if filepath[-1:] != "/":
                    filepath = filepath + "/"
                outputloggingfile.write(linestr.replace("ABS_FILE_NAME",filepath + project.pomname + "/" + project.pomname))
            elif linestr.find("LOG_SIZE") > -1:
                outputloggingfile.write(linestr.replace("LOG_SIZE", str(Configuration.log_size)))
            elif linestr.find("MAX_LOG_FILES") > -1:
                outputloggingfile.write(linestr.replace("MAX_LOG_FILES", str(Configuration.max_Log_files)))
            else:
                outputloggingfile.write(linestr)
        inputloggingfile.close()
        outputloggingfile.close()

    @staticmethod
    def create_docker_file( project):
        """
        this method will create the docker file for the project
        :param project:
        :return:
        """
        sourcefile = open("files/docker_kubernetes/docker","r")
        destinationfile = open(project.root + "/Dockerfile", "w")
        for line in sourcefile:
            linestr = str(line)
            destinationfile.write(linestr.replace("XXX", str(project.portnum)))
        sourcefile.close()
        destinationfile.close()

    @staticmethod
    def initialize_kubernetes_file():
        """
        this method will initialize a complete kubernetes file for our project
        :return:
        """
        if not os.path.exists(Configuration.kubernetes_complete_file_location):
            Utilities.mkdir(Configuration.kubernetes_complete_file_location)
        completefile = open(Configuration.kubernetes_complete_file_location + "/deployment.yaml", "w")
        completefile.close()

    @staticmethod
    def create_kubernetes_file( project):
        """
        this method will create the kubernetes file for the project
        :param project:
        :return:
        """
        sourcefile = open("files/docker_kubernetes/deployment.yml","r")
        destinationfile = open(project.root + "/deployment.yml", "w")
        completefile = open(Configuration.kubernetes_complete_file_location + "/deployment.yaml", "a")
        for line in sourcefile:
            linestr = str(line)
            if(linestr.find("XXX")>-1):
                destinationfile.write(linestr.replace("XXX", str(project.pomname)))
                completefile.write(linestr.replace("XXX", str(project.pomname)))
            elif(linestr.find("YYY")>-1):
                destinationfile.write(linestr.replace("YYY", str(project.portnum)))
                completefile.write(linestr.replace("YYY", str(project.portnum)))
            elif(linestr.find("ZZZ")>-1):
                destinationfile.write(linestr.replace("ZZZ", Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version))
                completefile.write(linestr.replace("ZZZ",Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version))
            elif(linestr.find("QQQ")>-1):
                if(Configuration.kubernetes_use_detailed_deployment_specs == True):
                    FileMaker.addMoreDetailedDeploymentSpecs(project,destinationfile)
                    FileMaker.addMoreDetailedDeploymentSpecs(project, completefile)
            elif(linestr.find("CCC")>-1):
                FileMaker.addCentralConfiguration(project,destinationfile)
                FileMaker.addCentralConfiguration(project, completefile)
            else:
                destinationfile.write(linestr)
                completefile.write(linestr)
        completefile.write("\n---\n")
        sourcefile.close()
        destinationfile.close()
        completefile.close()

    @staticmethod
    def create_ingress_file( projectnames, projectdata,localprojectsnames, localprojectdata):
        """
        this method will create the kubernetes ingress file for all of the generated projects
        :param projectnames:
        :param projectdata:
        :param localprojectsnames:
        :param localprojectdata:
        :return:
        """
        space = " "
        sourcefile = open("files/docker_kubernetes/ingress.yaml", "r")
        destinationfile = open(Configuration.destinationroot + "/ingress.yaml", "w")
        for line in sourcefile:
            linestr = str(line)
            if(linestr.find("XXX")>-1):
                for project in projectnames:
                    currentproject = projectdata[project]
                    for table in currentproject.tablenames:
                        currenttable = currentproject.tabledata[table]
                        destinationfile.write(space * 6 + "- path: /" + currenttable.lowercasename + "/*\n")
                        destinationfile.write(space * 8 + "backend:\n")
                        destinationfile.write(space * 10 + "serviceName: " + currentproject.pomname + "\n")
                        destinationfile.write(space * 10 + "servicePort: " + str(currentproject.portnum) + "\n")
                for project in localprojectsnames:
                    currentproject = localprojectdata[project]
                    destinationfile.write(space * 6 + "- path: /" + currentproject.lowercasename + "/*\n")
                    destinationfile.write(space * 8 + "backend:\n")
                    destinationfile.write(space * 10 + "serviceName: " + currentproject.pomname + "\n")
                    destinationfile.write(space * 10 + "servicePort: " + str(currentproject.portnum) + "\n")
            else:
                destinationfile.write(linestr)
        sourcefile.close()
        destinationfile.close()
        destinationfile = open(Configuration.destinationroot + "/ingress.yaml", "r")
        completefile = open(Configuration.kubernetes_complete_file_location + "/deployment.yaml", "a")
        for line in destinationfile:
            linestr = str(line)
            completefile.write(linestr)
        destinationfile.close()
        completefile.close()

    @staticmethod
    def addMoreDetailedDeploymentSpecs( project, destinationfile):
        """
        this method adds more detailed information for deployment resource allocation
        :param project:
        :param destinationfile:
        :return:
        """
        sourcefile = open("files/docker_kubernetes/det_dep_specs.yml", "r")
        for line in sourcefile:
            linestr = str(line)
            if (linestr.find("YYY") > -1):
                destinationfile.write(linestr.replace("YYY", str(project.portnum)))
            else:
                destinationfile.write(linestr)
        sourcefile.close()
        destinationfile.close()

    @staticmethod
    def create_kubernetes_commands_file( project):
        """
        this method will create a kubernetes commands file for the project
        :param project:
        :return:
        """
        sourcefile = open("files/docker_kubernetes/kubernetes_commands.txt","r")
        destinationfile = open(project.root + "/kubernetes_commands.txt", "w")
        for line in sourcefile:
            linestr = str(line)
            destinationfile.write(linestr)
        sourcefile.close()
        destinationfile.close()

    @staticmethod
    def makeParameterList( project):
        """
        this method creates a parameter list for the following commands in the kubernetes_commands.txt file:
        :param project:
        :param whatKind:
        :return:
        """
        returnStr = "--from-literal=kub_" + Configuration.kub_app_log.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_jpa.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_hib_dial.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_hib_nmg.replace("&", "\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_jpa_show.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_hib_seq.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_mysql_conn.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_mysql_usr.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_actu_conf.replace("&","\&")  + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_sec_usr.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_sec_pwd.replace("&","\&")
        return returnStr

    @staticmethod
    def addSecretsToKubernetes( project):
        """
        this method will add the parameters list to the secrets config command for Kubernetes
        :param project:
        :return:
        """
        returnStr = "--from-literal=kub_" + Configuration.app_mysql_pwd.replace("&","\&")
        return returnStr

    @staticmethod
    def addCentralConfiguration( project, destinationfile):
        """
        this method adds the kubernetes central configuration to the kubernetes file for the pod deployment section
        :param project:
        :param destinationfile:
        :return:
        """
        space = " "
        destinationfile.write(space*8 + "env:\n")
        configlist = [Configuration.kub_app_log, Configuration.kub_app_jpa , Configuration.kub_app_hib_dial , Configuration.kub_app_hib_nmg, Configuration.kub_app_hib_seq , Configuration.kub_app_mysql_conn ,
                      Configuration.kub_app_mysql_usr, Configuration.kub_app_jpa_show, Configuration.kub_app_actu_conf,  Configuration.kub_app_sec_usr, Configuration.kub_app_sec_pwd]
        x = range(len(configlist))
        for n in x:
            configstr = configlist[n]
            destinationfile.write(space * 8 + "- name: kub_" + configstr[0:configstr.find("=")] + "\n")
            destinationfile.write(space * 10 + "valueFrom:\n")
            destinationfile.write(space * 12 + "configMapKeyRef:\n")
            destinationfile.write(space * 14 + "key: kub_" + configstr[0:configstr.find("=")] + "\n")
            destinationfile.write(space * 14 + "name: " + project.pomname + "-config\n")
        configstr = Configuration.kub_app_mysql_pwd
        destinationfile.write(space * 8 + "- name: kub_" + configstr[0:configstr.find("=")] + "\n")
        destinationfile.write(space * 10 + "valueFrom:\n")
        destinationfile.write(space * 12 + "secretKeyRef:\n")
        destinationfile.write(space * 14 + "key: kub_" + configstr[0:configstr.find("=")] + "\n")
        destinationfile.write(space * 14 + "name: " + project.pomname + "-secrets\n")

    @staticmethod
    def parseProperty( property):
        """
        this method will adjust the property statement that goes into the application.properties
        according to the following convertion:
        key = ${<kubernetes key name>:<dafualy value if not found>}
        :param property:
        :return:
        """
        property_array = property.split("=")
        return property_array[0] + "=${kub_"+ property_array[0] + ":" + property_array[1] + "}"

    @staticmethod
    def addLoggingExclusion(newpom):
        """
        this method will add the logging exclusion needed in order to use a specialized logger
        :param newpom:
        :return:
        """
        inputfile = open("files/pom/logging_exclusion.xml")
        for line in inputfile:
            linestr = str(line)
            newpom.write(linestr)
        inputfile.close()

    @staticmethod
    def addLoggingDependency(newpom):
        """
        this method will add the logging dependency needed in order to use a specialized logger
        :param newpom:
        :return:
        """
        inputfile = open("files/pom/logging_dependency.xml")
        for line in inputfile:
            linestr = str(line)
            newpom.write(linestr)
        inputfile.close()

    @staticmethod
    def addSurefirePlugin(newpom):
        """
        this method will add the logging dependency needed in order to use a specialized logger
        :param newpom:
        :return:
        """
        inputfile = open("files/pom/bypass_testing_plugin.xml")
        for line in inputfile:
            linestr = str(line)
            newpom.write(linestr)
        inputfile.close()