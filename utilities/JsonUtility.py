import json
import random
from configuration.Configuration import *
from popos.Project import *
from popos.PostManObj import *
from popos.RequestObj import *
from configuration.Constants import *

"""
    this class is used to create the Postman collection for a given project
"""
class JsonUtility:

    numbers_and_strings = "abcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def createPostmanCollection(project):
        """
        this method will create the postman collection for the CRUD level projects
        :param project:
        :return:
        """
        tabs = Constants.tab
        jsonstr = '{\n'
        jsonstr += JsonUtility.make_info_part(project)
        jsonstr += tabs + '"item": [\n'
        for name in project.tablenames:
            currenttable = project.tabledata[name]
            jsonstr += JsonUtility.add_table_json(currenttable, project)
        jsonstr = jsonstr[0:-2] + '\n' + tabs + '],\n' + tabs + '"protocolProfileBehavior": {}\n}'
        postmanfilelocation = Configuration.postmandirectory
        if not os.path.exists(postmanfilelocation):
            print("creating Postman collection : " + postmanfilelocation)
            Utilities.mkdir(postmanfilelocation)
        postmanfile = open(Configuration.postmandirectory + "/" + project.pomname + ".postman_collection.json", "w")
        #postmanfile = open(project.projectresourcesfolder+project.pomname+".postman_collection.json","w")
        postmanfile.write(jsonstr)
        postmanfile.close()

    @staticmethod
    def make_postman_for_mid_level(project):
        """
        this method will create the postman collection for the mid-level projects
        :param project:
        :return:
        """
        # make a PostManObj
        postman_obj = PostManObj()
        # assemble the PostManObj, and fill it's RequestObj objects with the needed JSON text data
        JsonUtility.make_requests_from_controller(postman_obj, project)
        # assemble the final jsonstr JSON string object
        jsonstr = JsonUtility.assemble_final_json(postman_obj, project)
        postmanfile = open(Configuration.postmandirectory + "/" + project.pomname + ".postman_collection.json", "w")
        postmanfile.write(jsonstr)
        postmanfile.close()

    @staticmethod
    def make_requests_from_controller(postman_obj, project):
        """
        this method dynamically creates the postman request json based on the project's controller class
        :param postman_obj:
        :param project:
        :return:
        """
        inputfilepath = project.topmainpackage + "/" + Constants.pckg_contr + "/" + project.camelcasejavaname + "Controller.java"
        inputfile = open(inputfilepath,"r")
        # first thing to look for is the word "@RequestMapping"; this line will have the first part of each request's path
        requestmappingfound = False
        getname = False
        counter = 0
        for line in inputfile:
            linestr = str(line)
            # once that is found, we look for each instance of "@...Mapping" to find each request(2 lines needed)
            if requestmappingfound == True:
                # the second line, the line below the "@...Mapping" line has the method name
                if(getname == True):
                    thirdword = linestr.split(" ")[2]
                    tempname = thirdword[0:thirdword.find("(")]
                    #print("temp name = " + tempname)
                    # set the JSON text for the name
                    postman_obj.requests[counter].name = postman_obj.requests[counter].name.replace("XXX",tempname)
                    # finally, set other details about this request before we go on to look for the next request
                    JsonUtility.set_url_raw_host_and_path_items(postman_obj.requests[counter], postman_obj.request_name, project)
                    # reset this to False, so that the code knows to start looking for the next request
                    getname = False
                    counter += 1
                # but first, we need to parse the "@...Mapping" line for the request method type and the last part of the request path from the 1st line
                elif(linestr.find('Mapping(') > -1):
                    # make a new Request object
                    newobj = RequestObj()
                    # fill in the method type
                    newobj.method_type = linestr[linestr.find("@")+1:linestr.find("Mapping")].upper()
                    # and the JSON text
                    newobj.method = newobj.method.replace("XXX", newobj.method_type)
                    # fill in the path name
                    newobj.path_name = linestr[linestr.find('"') + 1:-3]
                    #print("request method = " + newobj.method_type + " , and the request path name is = " + newobj.path_name)
                    postman_obj.requests.append(newobj)
                    getname = True
            elif(linestr.find("@RequestMapping")>-1):
                postman_obj.request_name = linestr[linestr.find('path="')+6:-3]
                #print("name of the request is : ")
                requestmappingfound = True

    @staticmethod
    def set_url_raw_host_and_path_items( request_obj, request_name, project):
        """
        this method figures out the items that need to go into the RequestObj.url_and_path list for a given request
        :param request_obj:
        :return:
        """
        request_obj.raw = ''
        array = request_obj.path_name.split("/")
        secondarray = []
        # set the host and raw
        if(Configuration.use_docker == True):
            request_obj.raw += "http://" + Configuration.docker_localhost_url + ":" + str(project.portnum) + '/' + project.pomname
            request_obj.host = "http://" + Configuration.docker_localhost_url + ":" + str(project.portnum) + '/' + project.pomname
        elif (Configuration.use_gateway_server == True):
            request_obj.raw += Configuration.gateway_server_url + '/' + project.pomname + request_name
            request_obj.host = Configuration.gateway_server_url
            # add first item to the path array
            secondarray.append('"' + project.pomname + request_name + '"')
        else:
            request_obj.raw += Configuration.hostname + ":" + str(project.portnum)
            request_obj.host = Configuration.hostname + ":" + str(project.portnum)
            secondarray.append('"' + request_name + '"')
        # add the remaining items to the path array
        for item in array:
            if(len(item)>0):
                secondarray.append('"' + item + '"')
            # an append to the raw
        request_obj.raw += request_obj.path_name
        # set the JSON text fields
        request_obj.url_raw = request_obj.url_raw.replace("XXX", request_obj.raw)
        request_obj.url_host = request_obj.url_host.replace("XXX", request_obj.host)
        request_obj.url_path = request_obj.url_path.replace("XXX", ",".join(secondarray))
        request_obj.url = request_obj.url.replace("X1",request_obj.url_raw).replace("X2", request_obj.url_host).replace("X3", request_obj.url_path)

    @staticmethod
    def assemble_final_json( postman_obj, project):
        """
        this method will return the final json string to be printed to a text file
        :param postman_obj:
        :return:
        """
        # start the output json string
        jsonstr = postman_obj.info.replace("XXX",JsonUtility.generateRandomCollectionId()).replace("YYY",project.pomname)
        jsonstr += postman_obj.item
        counter = 0
        for req_object in postman_obj.requests:
            jsonstr += req_object.opener
            jsonstr += req_object.name
            jsonstr += req_object.request
            jsonstr += req_object.method
            jsonstr += req_object.header
            if(req_object.method_type == "POST"):
                jsonstr += req_object.body
            jsonstr += req_object.url
            jsonstr += req_object.response
            jsonstr += req_object.closer
            counter += 1
            if(counter < len(postman_obj.requests)):
                jsonstr += ","
        jsonstr += postman_obj.closer
        return jsonstr

    @staticmethod
    def make_info_part(project):
        """
        this generates the general info part
        :param project:
        :param json:
        :return:
        """
        tabs = Constants.tab
        json = tabs+'"info": {\n'
        json += tabs+tabs+'"_postman_id": "' + JsonUtility.generateRandomCollectionId() + '",\n'
        json += tabs+tabs+'"name": "'+project.pomname+'",\n'
        json += tabs+tabs+'"description" : "postman testing collection for the '+project.pomname+' project",\n'
        json += tabs+tabs+'"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"\n'
        json += tabs+'},\n'
        return json

    @staticmethod
    def add_table_json( table, project):
        """
        this method adds the REST request details
        :param table:
        :return:
        """
        tabs = Constants.tab
        protocol = '"http"'
        hostname_and_port = "http://localhost:" + str(project.portnum)
        path = table.lowercasename
        if(Configuration.use_docker == True):
            hostname_and_port = "http://" + Configuration.docker_localhost_url + ":" + str(project.portnum)
        elif(Configuration.use_gateway_server == True):
            hostname_and_port = str(Configuration.gateway_server_url)
            path = str(project.pomname) + '/' + table.lowercasename
        # getAll operation
        json = tabs * 2+ '{\n'
        json += tabs * 3+ '"name": "getAll' + table.camelcasejavaname + '",\n'
        json += tabs * 3+ '"request": {\n'
        json += tabs * 4 + '"method": "GET",\n'
        json += tabs * 4 + '"header": [],\n'
        json += tabs * 4 + '"url": {\n'
        json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/all",\n'
        json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
        json += tabs * 5 + '"host": [ "localhost" ],\n'
        json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
        json += tabs * 5 + '"path": [ "' + path + '", "all" ]\n'
        json += tabs * 4 + '}\n'
        json += tabs * 3+ '},\n'
        json += tabs * 3+ '"response": []\n'
        json += tabs * 2+ '},\n'
        # findById operation
        json += tabs * 2+ '{\n'
        json += tabs * 3+ '"name": "find' + table.camelcasejavaname + 'ById",\n'
        json += tabs * 3+ '"request": {\n'
        json += tabs * 4 + '"method": "GET",\n'
        json += tabs * 4 + '"header": [],\n'
        json += tabs * 4 + '"url": {\n'
        json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/findById/1",\n'
        json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
        json += tabs * 5 + '"host": [ "localhost" ],\n'
        json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
        json += tabs * 5 + '"path": [ "' + path + '", "findById", "1" ]\n'
        json += tabs * 4 + '}\n'
        json += tabs * 3+ '},\n'
        json += tabs * 3+ '"response": []\n'
        json += tabs * 2+ '},\n'
        # delete operation
        json += tabs * 2+ '{\n'
        json += tabs * 3+ '"name": "delete' + table.camelcasejavaname + '",\n'
        json += tabs * 3+ '"request": {\n'
        json += tabs * 4 + '"method": "DELETE",\n'
        json += tabs * 4 + '"header": [],\n'
        json += tabs * 4 + '"url": {\n'
        json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/delete/1",\n'
        json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
        json += tabs * 5 + '"host": [ "localhost" ],\n'
        json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
        json += tabs * 5 + '"path": [ "' + path + '", "delete", "1" ]\n'
        json += tabs * 4 + '}\n'
        json += tabs * 3+ '},\n'
        json += tabs * 3+ '"response": []\n'
        json += tabs * 2+ '},\n'
        # create operation
        json += tabs * 2+ '{\n'
        json += tabs * 3+ '"name": "create' + table.camelcasejavaname + '",\n'
        json += tabs * 3+ '"request": {\n'
        json += tabs * 4 + '"method": "POST",\n'
        json += tabs * 4 + '"header": [],\n'
        json += tabs * 4 + '"body": {\n'
        json += tabs * 5 + '"mode": "raw",\n'
        json += tabs * 5 + '"raw": {},\n'
        json += tabs * 5 + '"options": {\n'
        json += tabs * 5 + tabs + '"raw": { "language" : "json" }\n'
        json += tabs * 5 + '}\n'
        json += tabs * 4 + '},\n'
        json += tabs * 4 + '"url": {\n'
        json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/create",\n'
        json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
        json += tabs * 5 + '"host": [ "localhost" ],\n'
        json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
        json += tabs * 5 + '"path": [ "' + path + '", "create" ]\n'
        json += tabs * 4 + '}\n'
        json += tabs * 3+ '},\n'
        json += tabs * 3+ '"response": []\n'
        json += tabs * 2+ '},\n'
        # update operation
        json += tabs * 2+ '{\n'
        json += tabs * 3+ '"name": "update' + table.camelcasejavaname + '",\n'
        json += tabs * 3+ '"request": {\n'
        json += tabs * 4 + '"method": "POST",\n'
        json += tabs * 4 + '"header": [],\n'
        json += tabs * 4 + '"body": {\n'
        json += tabs * 5 + '"mode": "raw",\n'
        json += tabs * 5 + '"raw": {},\n'
        json += tabs * 5 + '"options": {\n'
        json += tabs * 5 + tabs + '"raw": { "language" : "json" }\n'
        json += tabs * 5 + '}\n'
        json += tabs * 4 + '},\n'
        json += tabs * 4 + '"url": {\n'
        json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/update",\n'
        json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
        json += tabs * 5 + '"host": [ "localhost" ],\n'
        json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
        json += tabs * 5 + '"path": [ "' + path + '", "update" ]\n'
        json += tabs * 4 + '}\n'
        json += tabs * 3+ '},\n'
        json += tabs * 3+ '"response": []\n'
        json += tabs * 2+ '},\n'

        # foreign key section
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

                json += tabs * 2 + '{\n'
                json += tabs * 3 + '"name": "find' + table.camelcasejavaname + 'By' + field.gettername + '",\n'
                json += tabs * 3 + '"request": {\n'
                json += tabs * 4 + '"method": "GET",\n'
                json += tabs * 4 + '"header": [],\n'
                json += tabs * 4 + '"url": {\n'
                json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/findBy' + field.gettername +'/1",\n'
                json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
                json += tabs * 5 + '"host": [ "localhost" ],\n'
                json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
                json += tabs * 5 + '"path": [ "' + path + '", "findBy' + field.gettername +'" , "1" ]\n'
                json += tabs * 4 + '}\n'
                json += tabs * 3 + '},\n'
                json += tabs * 3 + '"response": []\n'
                json += tabs * 2 + '},\n'

                counter += 1
        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            urlText = compoundFKstr + "/" + "/".join(inputparameters)
            json += tabs * 2 + '{\n'
            json += tabs * 3 + '"name": "find' + table.camelcasejavaname + 'By' + compoundFKstr + '",\n'
            json += tabs * 3 + '"request": {\n'
            json += tabs * 4 + '"method": "GET",\n'
            json += tabs * 4 + '"header": [],\n'
            json += tabs * 4 + '"url": {\n'
            json += tabs * 5 + '"raw": "' + hostname_and_port + '/' + path + '/findBy' + urlText + '",\n'
            json += tabs * 5 + '"protocol" : ' + protocol + ',\n'
            json += tabs * 5 + '"host": [ "localhost" ],\n'
            json += tabs * 5 + '"port" : "' + str(project.portnum) + '",\n'
            json += tabs * 5 + '"path": [ "' + path + '", "findBy' + urlText + '" ]\n'
            json += tabs * 4 + '}\n'
            json += tabs * 3 + '},\n'
            json += tabs * 3 + '"response": []\n'
            json += tabs * 2 + '},\n'

        return json

    @staticmethod
    def generateRandomCollectionId():
        """
        this function will return a random postman collection id
        :return:
        """
        counter = 0
        collection_id = ''
        while counter <8:
            index = random.randint(0, 35)
            collection_id += JsonUtility.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += JsonUtility.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += JsonUtility.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += JsonUtility.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <12:
            index = random.randint(0, 35)
            collection_id += JsonUtility.numbers_and_strings[index]
            counter +=1
        return collection_id
