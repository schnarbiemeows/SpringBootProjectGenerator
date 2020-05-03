from utilities.Utilities import *
from utilities.JsonUtility import *
from configuration.Constants import *
from configuration.Configuration import *
from distutils.dir_util import *

class FileMaker:
    
    def __init__(self):
        """
        initilization
        :return: 
        """
        self.utilities = Utilities()
        self.jsonutility = JsonUtility()
    
    def make_postman_for_mid_level(self, project):
        """
        redirecting to JsonUtility.py make_postman_for_mid_level method
        :param project: 
        :return: 
        """
        self.jsonutility.make_postman_for_mid_level(project)

    def createPostmanCollection(self, project):
        """
        redirecting to JsonUtility.py createPostmanCollection method
        :param project:
        :return:
        """
        self.jsonutility.createPostmanCollection(project)

    def backup_project(self, project, destinationroot):
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

    def make_base_angular_project(self, project):
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
            if len(directory)>1 and not os.path.exists(directory):
                self.utilities.mkdir(directory)
        destinationroot = directory
        if(not destinationroot.endswith("/")):
            destinationroot += "/"
        if not os.path.exists(destinationroot+project.pomname):
            print("creating Angular project : " + project.pomname)
            self.utilities.mkdir(destinationroot+project.pomname)
        return destinationroot+project.pomname

    def create_base_project_folders(self, project, sourceprojectfolder, destinationroot, artifactid, groupid):
        """
        this method will create the basic folder structure of a SB project
        :param project:
        :param sourceprojectfolder:
        :param destinationroot:
        :param artifactid:
        :param groupid:
        :return:
        """
        self.utilities.mkdir(destinationroot + "/" + project.pomname)
        self.utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname)
        self.utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn")
        self.utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper")

        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.jar",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/maven-wrapper.jar")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.properties",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/maven-wrapper.properties")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/MavenWrapperDownloader.java",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.mvn/wrapper/MavenWrapperDownloader.java")

        self.utilities.mkdir(destinationroot + "/" + project.pomname + "/" + project.pomname + "/src")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.gitIgnore",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/.gitIgnore")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/HELP.md",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/HELP.md")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/mvnw")
        self.utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw.cmd",
                      destinationroot + "/" + project.pomname + "/" + project.pomname + "/mvnw.cmd")
        projectrootpackage = destinationroot + "/" + project.pomname + "/" + project.pomname + "/src/"
        self.utilities.mkdir(projectrootpackage + "main")
        self.utilities.mkdir(projectrootpackage + "test")
        self.utilities.mkdir(projectrootpackage + "main/java")
        self.utilities.mkdir(projectrootpackage + "main/resources")
        self.utilities.mkdir(projectrootpackage + "test/java")
        projectmainfolder = projectrootpackage + "main/java/"
        project.projectresourcesfolder = projectrootpackage + "main/resources/"
        projecttestfolder = projectrootpackage + "test/java/"
        # how far we have to go into the source folder depends on if the groupId has any periods in it, which each
        # represent its own sub-folder
        packages = groupid.split(".")
        packageslength = len(packages)
        topmainpackage = packages[0]
        toptestpackage = packages[0]
        self.utilities.mkdir(projectmainfolder + topmainpackage)
        self.utilities.mkdir(projecttestfolder + toptestpackage)
        if packageslength > 1:
            x = range(1, packageslength)
            for n in x:
                topmainpackage += "/" + packages[n]
                toptestpackage += "/" + packages[n]
                self.utilities.mkdir(projectmainfolder + topmainpackage)
                self.utilities.mkdir(projecttestfolder + toptestpackage)
        # now have to add the artifactID folder to these roots
        topmainpackage += "/" + project.lowercasename
        toptestpackage += "/" + project.lowercasename
        self.utilities.mkdir(projectmainfolder + topmainpackage)
        # make subpackages
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/config")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/controllers")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/exceptions")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/business")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/dtos")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/proxy")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/dtos")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/pojos")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/proxy/services")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/pojos")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/services")
        self.utilities.mkdir(projectmainfolder + topmainpackage + "/utilities")

        self.utilities.mkdir(projecttestfolder + toptestpackage)
        # make subpackages
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/config")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/controllers")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/exceptions")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/business")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/dtos")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/proxy")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/dtos")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/pojos")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/proxy/services")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/pojos")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/services")
        self.utilities.mkdir(projecttestfolder + toptestpackage + "/utilities")

        # set the Table object's main java and test package roots
        project.topmainpackage = projectmainfolder + topmainpackage
        project.toptestpackage = projecttestfolder + toptestpackage
        # rootpackage is for the individual Java files' "package ..." statement
        project.rootpackage = topmainpackage.replace("/", ".")
        self.create_pom_file(project, sourceprojectfolder, artifactid, destinationroot)

    def create_application_resources_file(self, project):
        """
        this method creates the application.properties file for the project
        *** Note: if they chose Configuration.use_config_server = True(chose to use a Spring CLoud config server)
        this method will instead put these properties into a default config file called <pom name>.txt for the config server
        to deploy to GIT. It will also create a file bootstrap.properties, that contains the needed confugration to point to
        the uri of this config server, specified with Configuration.spring_cloud_config_uri
        :param project:
        :return:
        """
        if(Configuration.use_config_server == True):
            resources_file = open(project.projectresourcesfolder + "/bootstrap.properties", "w")
            resources_file.write(Configuration.app_name + project.pomname + "\n")
            resources_file.write(Configuration.app_port + str(project.portnum) + "\n")
            resources_file.write(Configuration.spring_cloud_config_uri+"\n")
            resources_file.close()
            resources_file = open("/nms-config-server-git/"+project.pomname+".properties", "w")
            resources_file.write(Configuration.app_log + "\n")
            resources_file.write(Configuration.app_jpa + "\n")
            resources_file.write(Configuration.app_jpa_show + "\n")
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
            resources_file.write("spring.application.name=" + project.pomname)
            resources_file.write("server.port="+str(project.portnum)+"\n")
            resources_file.write(Configuration.app_log + "\n")
            resources_file.write(Configuration.app_jpa + "\n")
            resources_file.write(Configuration.app_jpa_show + "\n")
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

    def create_pom_file(self, project, sourceroot, artifactId, destinationroot):
        """
        this method will copy the pom.xml while changing some things
        - it needs to change the groupId, artifactId, description, and name fields
        - it needs to add in the swagger2 dependencies(from dependencies.xml file)
        - it needs to add in the com.fasterxml.jackson.dataformat dependency(from dependencies.xml file)
        - it needs to add in the sonarqube and jacoco stuff(from jacoco_props.xml file and sonar_jacoco.xml file)
        :param project:
        :param sourceroot:
        :param artifactId:
        :param destinationroot:
        :return:
        """
        oldpom = open(sourceroot + "/" + artifactId + "/pom.xml","r")
        newpom = open(destinationroot + "/" + project.pomname + "/" + project.pomname + "/pom.xml", "w")
        parentpassed = False
        groupIdadded = False
        artifactIdadded = False
        nameadded = False
        desc_added = False
        for item in oldpom:
            itemstr = str(item)
            if(parentpassed == False):
                newpom.write(itemstr)
                if(itemstr.find("</parent>")>-1):
                    parentpassed = True
            else:
                if(itemstr.find("</groupId>") > -1):
                    if(groupIdadded == False):
                        newpom.write(Constants.xml_grp.replace("*", Configuration.groupid)+"\n")
                        groupIdadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</artifactId>") > -1):
                    if (artifactIdadded == False):
                        newpom.write(Constants.xml_art.replace("*", project.pomname) + "\n")
                        artifactIdadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</name>") > -1):
                    if (nameadded == False):
                        newpom.write(Constants.xml_name.replace("*", project.pomname) + "\n")
                        nameadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</description>") > -1):
                    if (desc_added == False):
                        newpom.write(Constants.xml_desc.replace("*", project.pomname))
                        desc_added = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</properties>") > -1):
                    # jaccoco properties
                    if(Configuration.use_sonar_jacoco == True):
                        jacocoprops = open("files/jacoco_props.xml","r")
                        for prop in jacocoprops:
                            propstr = str(prop)
                            newpom.write(propstr)
                        jacocoprops.close()
                    # cloud config client properties
                    if (Configuration.use_config_server == True):
                        configclientprop = open("files/config_client_prop.xml", "r")
                        for prop in configclientprop:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientprop.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                elif (itemstr.find("</dependencies>") > -1):
                    dependencies = open("files/dependencies.xml","r")
                    for dep in dependencies:
                        depstr = str(dep)
                        newpom.write(depstr)
                    dependencies.close()
                    # cloud naming server dependencies
                    if (Configuration.use_naming_server == True):
                        naming_server_config = open("files/feign_dep.xml", "r")
                        for prop in naming_server_config:
                            propstr = str(prop)
                            newpom.write(propstr)
                        naming_server_config.close()
                        newpom.write("\n")
                    # cloud config client dependency
                    if (Configuration.use_config_server == True):
                        configclientdep = open("files/config_client_dep.xml", "r")
                        for prop in configclientdep:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientdep.close()
                    newpom.write("\n")
                    if (Configuration.use_distributed_tracing == True):
                        sleuthfile = open("files/sleuth.xml", "r")
                        for line in sleuthfile:
                            linestr = str(line)
                            newpom.write(linestr)
                        sleuthfile.close()
                        newpom.write("\n")
                    newpom.write(itemstr)
                    # cloud config client dependency management
                    if (Configuration.use_config_server == True):
                        configclientdepmngmt = open("files/cloud_conf_dep_mngmt.xml", "r")
                        for prop in configclientdepmngmt:
                            propstr = str(prop)
                            newpom.write(propstr)
                        configclientdepmngmt.close()
                        newpom.write("\n")
                elif (itemstr.find("</plugins>") > -1):
                    if (Configuration.use_sonar_jacoco == True):
                        sonarjacoco = open("files/sonar_jacoco.xml","r")
                        for line in sonarjacoco:
                            linestr = str(line)
                            newpom.write(linestr)
                        sonarjacoco.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                else:
                    newpom.write(itemstr)
        newpom.close()

