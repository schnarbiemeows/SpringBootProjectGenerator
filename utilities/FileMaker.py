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

    def create_application_resources_file(self, project, otherprojectnamesotherprojects = None):
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
            resources_file.write(self.parseProperty(Configuration.app_log) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_jpa) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_jpa_show) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_hib_seq) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_mysql_conn) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_mysql_usr) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_mysql_pwd) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_actu_conf) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_sec_usr) + "\n")
            resources_file.write(self.parseProperty(Configuration.app_sec_pwd) + "\n")
            resources_file.close()
        elif(Configuration.use_config_server == True):
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
            resources_file.write("spring.application.name=" + project.pomname+"\n")
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

    def populate_kubernetes_commands_file(self, project):
        """
        this method will add certain command line commands to run to make our lives easier
        :param project:
        :return:
        """
        destinationfile = open(project.root + "/kubernetes_commands.txt", "w")
        destinationfile.write("cd /c" + project.root.replace("C:\\", "/").replace("\\", "/") + "\n")
        docker_cmd = "docker run -d -p " + str(project.portnum) + ":" + str(project.portnum) + " "
        docker_cmd += Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version + " "
        if (project.is_mid_level == True and Configuration.use_docker == True):
            for item in project.service_config:
                docker_cmd += "--" + item + "=" + Configuration.docker_localhost_url + " "
        destinationfile.write("-- run the project as a docker image\n")
        destinationfile.write(docker_cmd + "\n\n")
        push_cmd = "docker push " + Configuration.docker_remote_repo_name + "/" + project.pomname + ":" + Configuration.version
        destinationfile.write("-- push the project to the repository\n")
        destinationfile.write(push_cmd + "\n\n")
        kub_config_cmd = "kubectl create configmap " + project.pomname + "-config "
        destinationfile.write("-- command to create the configuration map for this project in kubernetes\n")
        kub_config_cmd += self.makeParameterList(project)
        destinationfile.write(kub_config_cmd + "\n\n")
        destinationfile.write("-- command to create the secrets map for this project in kubernetes\n")
        kub_secrets_cmd = "kubectl create secret generic " + project.pomname + "-secrets "
        kub_secrets_cmd += self.addSecretsToKubernetes(project)
        destinationfile.write(kub_secrets_cmd + "\n\n")
        destinationfile.close()

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
                if(itemstr.find("GGG") > -1):
                   newpom.write(itemstr.replace("GGG", Configuration.groupid))
                elif (itemstr.find("VVV") > -1):
                    newpom.write(itemstr.replace("VVV", Configuration.version))
                elif (itemstr.find("AAA") > -1):
                    newpom.write(itemstr.replace("AAA", project.pomname))
                elif (itemstr.find("NNN") > -1):
                    newpom.write(itemstr.replace("NNN", project.pomname))
                elif (itemstr.find("DDD") > -1):
                    newpom.write(itemstr.replace("DDD", "CRUD application for the " + project.pomname + " project"))
                elif (itemstr.find("</properties>") > -1):
                    # jaccoco properties
                    if(Configuration.use_sonar_jacoco == True):
                        jacocoprops = open("files/jacoco_props.xml","r")
                        for prop in jacocoprops:
                            propstr = str(prop)
                            newpom.write(propstr)
                        jacocoprops.close()
                    # cloud config client properties
                    if (Configuration.use_config_server == True or Configuration.use_docker == True or
                            Configuration.use_gateway_server == True or Configuration.use_distributed_tracing == True or
                            Configuration.use_naming_server == True):
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
                    if (Configuration.use_docker == True):
                        naming_server_config = open("files/docker_kubernetes/feign.xml", "r")
                        for prop in naming_server_config:
                            propstr = str(prop)
                            newpom.write(propstr)
                        naming_server_config.close()
                        newpom.write("\n")
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
                    if (Configuration.use_config_server == True or Configuration.use_docker == True or
                            Configuration.use_gateway_server == True or Configuration.use_distributed_tracing == True or
                            Configuration.use_naming_server == True):
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

    def create_docker_file(self, project):
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

    def initialize_kubernetes_file(self):
        """
        this method will initialize a complete kubernetes file for our project
        :return:
        """
        if not os.path.exists(Configuration.kubernetes_complete_file_location):
            self.utilities.mkdir(Configuration.kubernetes_complete_file_location)
        completefile = open(Configuration.kubernetes_complete_file_location + "/deployment.yaml", "w")
        completefile.close()

    def create_kubernetes_file(self, project):
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
                    self.addMoreDetailedDeploymentSpecs(project,destinationfile)
                    self.addMoreDetailedDeploymentSpecs(project, completefile)
            elif(linestr.find("CCC")>-1):
                self.addCentralConfiguration(project,destinationfile)
                self.addCentralConfiguration(project, completefile)
            else:
                destinationfile.write(linestr)
                completefile.write(linestr)
        completefile.write("\n---\n")
        sourcefile.close()
        destinationfile.close()
        completefile.close()

    def create_ingress_file(self, projectnames, projectdata,localprojectsnames, localprojectdata):
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


    def addMoreDetailedDeploymentSpecs(self, project, destinationfile):
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



    def create_kubernetes_commands_file(self, project):
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

    def makeParameterList(self, project):
        """
        this method creates a parameter list for the following commands in the kubernetes_commands.txt file:
        :param project:
        :param whatKind:
        :return:
        """
        returnStr = "--from-literal=kub_" + Configuration.kub_app_log.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_jpa.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_hib_dial.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_jpa_show.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_hib_seq.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_mysql_conn.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_mysql_usr.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_actu_conf.replace("&","\&")  + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_sec_usr.replace("&","\&") + " "
        returnStr += "--from-literal=kub_" + Configuration.kub_app_sec_pwd.replace("&","\&")
        return returnStr

    def addSecretsToKubernetes(self, project):
        """
        this method will add the parameters list to the secrets config command for Kubernetes
        :param project:
        :return:
        """
        returnStr = "--from-literal=kub_" + Configuration.app_mysql_pwd.replace("&","\&")
        return returnStr

    def addCentralConfiguration(self, project, destinationfile):
        """
        this method adds the kubernetes central configuration to the kubernetes file for the pod deployment section
        :param project:
        :param destinationfile:
        :return:
        """
        space = " "
        destinationfile.write(space*8 + "env:\n")
        configlist = [Configuration.kub_app_log, Configuration.kub_app_jpa , Configuration.kub_app_hib_dial , Configuration.kub_app_hib_seq , Configuration.kub_app_mysql_conn ,
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

    def parseProperty(self, property):
        """
        this method will adjust the property statement that goes into the application.properties
        according to the following convertion:
        key = ${<kubernetes key name>:<dafualy value if not found>}
        :param property:
        :return:
        """
        property_array = property.split("=")
        return property_array[0] + "=${kub_"+ property_array[0] + ":" + property_array[1] + "}"