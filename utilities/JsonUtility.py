import json
import random

"""
    this class is used to create the Postman clooection for a given project
"""
class JsonUtility:

    numbers_and_strings = "abcdefghijklmnopqrstuvwxyz0123456789"

    def createPostmanCollection(self,project):
        tabs = "\t"
        jsonstr = '{\n'
        jsonstr += self.make_info_part(project)
        jsonstr += tabs + '"item": [\n'
        for name in project.tablenames:
            currenttable = project.tabledata[name]
            jsonstr += self.add_table_json(currenttable, project.portnum)
        jsonstr = jsonstr[0:-2] + '\n' + tabs + '],\n' + tabs + '"protocolProfileBehavior": {}\n}'
        postmanfile = open(project.projectresourcesfolder+project.pomname+".postman_collection.json","w")
        postmanfile.write(jsonstr)
        postmanfile.close()


    def make_info_part(self,project):
        """
        this generates the general info part
        :param project:
        :param json:
        :return:
        """
        tabs = "\t"
        json = tabs+'"info": {\n'
        json += tabs+tabs+'"_postman_id": "' + self.generateRandomCollectionId() + '",\n'
        json += tabs+tabs+'"name": "'+project.pomname+'",\n'
        json += tabs+tabs+'"description" : "postman testing collection for the '+project.pomname+' project",\n'
        json += tabs+tabs+'"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"\n'
        json += tabs+'},\n'
        return json

    def add_table_json(self, table, port):
        """

        :param table:
        :return:
        """
        tabs = "\t"
        # getAll operation
        json = tabs + tabs + '{\n'
        json += tabs + tabs + tabs + '"name": "getAll' + table.camelcasejavaname + '",\n'
        json += tabs + tabs + tabs + '"request": {\n'
        json += tabs + tabs + tabs + tabs + '"method": "GET",\n'
        json += tabs + tabs + tabs + tabs + '"header": [],\n'
        json += tabs + tabs + tabs + tabs + '"url": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": "http://localhost:' + str(port) + '/' + table.lowercasename + '/all",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"host": [ "http://localhost:' + str(port) + '" ],\n'
        json += tabs + tabs + tabs + tabs + tabs + '"path": [ "' + table.lowercasename + '", "all" ]\n'
        json += tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + '"response": []\n'
        json += tabs + tabs + '},\n'
        # findById operation
        json += tabs + tabs + '{\n'
        json += tabs + tabs + tabs + '"name": "find' + table.camelcasejavaname + 'ById",\n'
        json += tabs + tabs + tabs + '"request": {\n'
        json += tabs + tabs + tabs + tabs + '"method": "GET",\n'
        json += tabs + tabs + tabs + tabs + '"header": [],\n'
        json += tabs + tabs + tabs + tabs + '"url": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": "http://localhost:' + str(port) + '/' + table.lowercasename + '/findById/1",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"host": [ "http://localhost:' + str(port) + '" ],\n'
        json += tabs + tabs + tabs + tabs + tabs + '"path": [ "' + table.lowercasename + '", "findById", "1" ]\n'
        json += tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + '"response": []\n'
        json += tabs + tabs + '},\n'
        # delete operation
        json += tabs + tabs + '{\n'
        json += tabs + tabs + tabs + '"name": "delete' + table.camelcasejavaname + '",\n'
        json += tabs + tabs + tabs + '"request": {\n'
        json += tabs + tabs + tabs + tabs + '"method": "DELETE",\n'
        json += tabs + tabs + tabs + tabs + '"header": [],\n'
        json += tabs + tabs + tabs + tabs + '"url": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": "http://localhost:' + str(port) + '/' + table.lowercasename + '/delete/1",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"host": [ "http://localhost:' + str(port) + '" ],\n'
        json += tabs + tabs + tabs + tabs + tabs + '"path": [ "' + table.lowercasename + '", "delete", "1" ]\n'
        json += tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + '"response": []\n'
        json += tabs + tabs + '},\n'
        # create operation
        json += tabs + tabs + '{\n'
        json += tabs + tabs + tabs + '"name": "create' + table.camelcasejavaname + '",\n'
        json += tabs + tabs + tabs + '"request": {\n'
        json += tabs + tabs + tabs + tabs + '"method": "POST",\n'
        json += tabs + tabs + tabs + tabs + '"header": [],\n'
        json += tabs + tabs + tabs + tabs + '"body": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"mode": "raw",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": {},\n'
        json += tabs + tabs + tabs + tabs + tabs + '"options": {\n'
        json += tabs + tabs + tabs + tabs + tabs + tabs + '"raw": { "language" : "json" }\n'
        json += tabs + tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + tabs + '"url": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": "http://localhost:' + str(port) + '/' + table.lowercasename + '/create",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"host": [ "http://localhost:' + str(port) + '" ],\n'
        json += tabs + tabs + tabs + tabs + tabs + '"path": [ "' + table.lowercasename + '", "create" ]\n'
        json += tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + '"response": []\n'
        json += tabs + tabs + '},\n'
        # update operation
        json += tabs + tabs + '{\n'
        json += tabs + tabs + tabs + '"name": "update' + table.camelcasejavaname + '",\n'
        json += tabs + tabs + tabs + '"request": {\n'
        json += tabs + tabs + tabs + tabs + '"method": "POST",\n'
        json += tabs + tabs + tabs + tabs + '"header": [],\n'
        json += tabs + tabs + tabs + tabs + '"body": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"mode": "raw",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": {},\n'
        json += tabs + tabs + tabs + tabs + tabs + '"options": {\n'
        json += tabs + tabs + tabs + tabs + tabs + tabs + '"raw": { "language" : "json" }\n'
        json += tabs + tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + tabs + '"url": {\n'
        json += tabs + tabs + tabs + tabs + tabs + '"raw": "http://localhost:' + str(port) + '/' + table.lowercasename + '/update",\n'
        json += tabs + tabs + tabs + tabs + tabs + '"host": [ "http://localhost:' + str(port) + '" ],\n'
        json += tabs + tabs + tabs + tabs + tabs + '"path": [ "' + table.lowercasename + '", "update" ]\n'
        json += tabs + tabs + tabs + tabs + '}\n'
        json += tabs + tabs + tabs + '},\n'
        json += tabs + tabs + tabs + '"response": []\n'
        json += tabs + tabs + '},\n'
        return json

    def generateRandomCollectionId(self):
        """
        this function will return a random postman collection id
        :return:
        """
        counter = 0
        collection_id = ''
        while counter <8:
            index = random.randint(0, 35)
            collection_id += self.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += self.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += self.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <4:
            index = random.randint(0, 35)
            collection_id += self.numbers_and_strings[index]
            counter +=1
        collection_id += '-'
        counter = 0
        while counter <12:
            index = random.randint(0, 35)
            collection_id += self.numbers_and_strings[index]
            counter +=1
        return collection_id
