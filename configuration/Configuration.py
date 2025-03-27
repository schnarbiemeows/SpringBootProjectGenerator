class Configuration:
    """
        set these configuration variables
    """

    author = "Dylan I. Kessler"
    website = "www.schnarbiesnmeowers.com"
    email = "email@email.com"
    groupid = "com.schnarbiesnmeowers"
    version = "0.0.1-SNAPSHOT"

    """
        main source and destination folder location
    """
    # source project to clone
    sourceprojectfolder = "files/demo"
    # sourcesqlfile = "configuration/nms-tables.sql"

    # location of the SQL file to parse
    sourcesqlfile = "configuration/input/nms-monolith.sql"

    # test parser only
    destinationtestfile = "configuration/output/body-dims-svc.sql"
    # nutrition_microservices_workspace

    # root destination folder where the new Spring Boot project(s) will go
    destinationroot = "configuration/output"

    ##destinationroot = "/Users/dylan/IdeaProjects/nms-monolith"
    #"/eclipse_workspaces/sbg-java-workspace"
    #test_fk = True
    """
        hostname : primarily for the postman generation functionality, it represents the ipaddress that each project 
        will be using. leave as localhost if testing locally
        otherwise, specify the ipaddress where each of these projects will be run
    """
    hostname = "http://localhost"

    # generation options:
    """
        set the variable below for generation_type, options are:
        1 - each table has its own project. The name of each project is approximately the same as the table name, project_name field is ignored
        2 - all tables are in one project, the user needs to specify the name of the overall project with the project_name field below
        3 - manually specify the table grouping using a text file called groupings.txt(located in the files folder in this project)

    """
    generation_type = 2
    project_name = "nms-monolith"
    """
        beginning_port_num : this is the port # for the first application. numbers are generated consecutively, so if you are generating
        multiple services, the first one will be this number, the next one will be this number +1, etc....
    """
    beginning_port_num = 8087
    """
        make_mid_lvl_services : would you like to make some mid-level SB services that make calls to your CRUD services?
                                use the file configuration/mid_level.txt to map the mid-level services to the CRUD services you would
                                like each service to have proxies for.
                                these mid-level service will come with some default REST endpoints in the controller(like a healthcheck GET),
                                will have no repository interface, but will have proxies to the CRUD services, with DTOs and POJOs
                                set = True, otherwise, defaults to False
    """
    make_mid_lvl_services = False
    mid_lvl_port_num = 8080

    """
        backup_all_projects :
    """
    backup_all_projects = False
    # "/eclipse_workspaces/nutrition_microservices_workspace/backup"
    backup_directory = "/eclipse_workspaces/nutrition_microservices_workspace/backup"
    """
        these options below must be set to True ; otherwise they default to False

        use_config_server : should these project be configured to use a Spring Boot centralized configuration server, that uses a localized GIT
                            repository to store the configuration. set to False if you're not sure how to use this.
                            If set to True, then the following will happen:
                            1. a bootstrap.properties file will be made instead of an application.properties file, with these 2 settings:
                            - spring.application.name => the name of the default config file in the config server
                            - spring.cloud.config.uri(set by setting spring_cloud_config_uri)
                            2. the proper dependencies will be added to the projects' pom files
                            3. a file will be added to the src/main/resources folder with the name as specified by the spring.application.name in
                                bootstrap.properties. This file needs to be committed to the config server's GIT repository.
                                The fields in this file will be all of those that would have been in the application.properties file(set below).
                                So basically, the contents of these files for each project will be the same, just with different filenames
        spring_cloud_config_uri : url to the configuration server
    """
    use_config_server = False
    config_server_git = "/Users/dylan/git/server-config"
    spring_cloud_config_uri = "spring.cloud.config.uri=http://100.26.104.131:8888/"
    """
        100.26.104.131
    """
    """
        use_sonar_jacoco : do you want to include sonarQube code analysis functionality and Jaccoco code coverage functionality?
                            set = True, otherwise, defaults to False
    """
    use_sonar_jacoco = True
    """
        use_naming_server : do you want to use Netflix's Eureka naming server, in conjunction with SB Feign and Ribbon technologies, to implement
                            load balancing for your microservices
                            set = True, otherwise, defaults to false
        naming_server_url : the url to the naming server
        naming_server_proxy_mode : this application will only make proxies to the other tables/projects if use_naming_server = True
                            has 3 modes, which depend on the generation_type mode specified:
                            1 - works for all 3 generation_type(1,2,3). this will make a simple GenericProxy interface that the user then has to
                                complete. This is the default in the event that the user does not correctly match generation_type mode with this mode.
                            2 - works for generation_type = 1 or 3, 1-proxy-per-project mode. for each project, this will create a proxy to every other
                            project
    """
    use_naming_server = False
    naming_server_url = "eureka.client.serviceUrl.defaultZone=http://54.167.34.201:8761/eureka/"
    naming_server_proxy_mode = 2
    """
        use_gateway_server : do you want to use a netflix zuul gateway server. must be used in conjunction with using both a config and a naming server

        gateway_server_url : url to the gateways server, including the port #
    """
    use_gateway_server = False
    #gateway_server_url = "http://localhost:8765"
    gateway_server_url = "http://100.26.104.131:8765"
    """
        bypass_business   : True or False. If True, the program will NOT remake the business classes for each project. Use this feature if you
                            don't want the program to overwrite any business logic that you might be working on. defaults to False.
        bypass_controllers: True or False. If True, the program will NOT remake the controller classes for each project. Use this feature if you
                            don't want the program to overwrite any controller logic that you might be working on. defaults to False.
    """
    bypass_business = False
    bypass_controllers = False
    """
        use_logging : this will add log4j2 logging into the project
    """
    use_logging = True
    log_pattern = "%d{yyyy-MM-dd HH:mm:ss.SSS} %5p : %m%n%ex"
    root_logging_path = "/home/ubuntu/logs"
    log_size = 10
    max_Log_files = 10
    """
        bypass_testing : this will make the maven install bypass the Junit testing
    """
    bypass_testing = True
    """
    *******************************************************************************************************************
                                                        ANGULAR SECTION
        create_angular_projects : this will make Angular 19 UI projects for each of the CRUD projects and mid-level 
        projects
        angular_directory : this is the directory where you want the angular project files to go in; it is up to the 
        user to manually copy these files/folders into their Angular projects
        
        what needs to be installed into an empty project:
        npm install bootstrap core-js font-awesome jquery rxjs-compat popper.js angular-notifier
        for the pagination, you need to run this command:
        npm install ngx-pagination --save
    """

    create_angular_projects = False
    angular_dest_directory = "output/angular/"
    # dependencies - OLD
    angular_boostrap = '^5.3.3'
    angular_core_js = '^14.3.0'
    angular_font_awesome = '^5.8.1'
    angular_jquery = '^3.6.1'
    angular_popper_js = '^1.16.1'
    """
        *******************************************************************************************************************
                                                    REACT SECTION
    """
    create_react_projects = True
    react_dest_directory = "output/react/"
    """
        use_distributed_tracing : this feature will enable spring cloud sleuth to generate a unique transaction ID for each transaction
                                    this is part of distributed central logging functionality
    """
    use_distributed_tracing = False
    """
        use_docker              : use docker and Kubernetes. This feature will create a Docker file and deployment.yml and/or docker-compose files.
        docker_remote_repo_name : your username on the remote repository site DockerHub. the projects are configured for pushing to
                                    <username>/#{project.name} with the tag ${project.version}
        docker_needs_192        : True or False. on some windows computers, localhost doesn't work, you have to use either 192.168.99.100, or the results
                                    of the command "docker-machine ip", run in the docker command line. Set this to True if this is the case
        docker_localhost_url    : If docker_needs_192 == True, this value is the results from running the command "docker-machine ip"
                                    in the docker command line((don't include "http://"). if localhost works, just put "localhost"(no "http://")
    """
    use_docker = False
    docker_remote_repo_name = "schnarbies"
    docker_needs_192 = True
    docker_localhost_url = "192.168.99.100"
    kubernetes_use_detailed_deployment_specs = False
    kubernetes_complete_file_location = "/eclipse_workspaces/interview_workspace/kubernetes"
    """
        postmandirectory    :   generate postman JSON files for each microservice that can be imported as a 
                                collection in postman,
                                will include all of the servive calls for each service
    """
    postmandirectory = "/Users/dylan/postman_collections"

    # for the application.properties file - this is for local testing
    app_name = "spring.application.name="
    app_port = "server.port="

    app_log = "logging.level.org.springframework=debug"
    app_actu_conf = "management.endpoints.web.exposure.include=*"
    app_sec_usr = "spring.security.user.name=test"
    app_sec_pwd = "spring.security.user.password=GYI%*&#^%G^#SHGWTRR@&^TRR23tr2fegge8"

    # for the Kubernetes global configuration
    kub_app_log = "logging.level.org.springframework=debug"
    kub_app_jpa = "spring.jpa.hibernate.ddl-auto=none"
    kub_app_hib_dial = "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL5Dialect"
    kub_app_hib_nmg = "spring.jpa.hibernate.naming.physical-strategy=org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl"
    kub_app_hib_seq = "spring.jpa.hibernate.use-new-id-generator-mappings=false"
    kub_app_mysql_conn = "spring.datasource.url=jdbc:mysql://locahost:3306/<schemaname>"
    kub_app_mysql_usr = "spring.datasource.username=<username>"
    kub_app_mysql_pwd = "spring.datasource.password=<password>"
    kub_app_jpa_show = "spring.jpa.show-sql=true"
    kub_app_actu_conf = "management.endpoints.web.exposure.include=*"
    kub_app_sec_usr = "spring.security.user.name=test"
    kub_app_sec_pwd = "spring.security.user.password=GYI%*&#^%G^#SHGWTRR@&^TRR23tr2fegge8"

