from configuration.Configuration import *

"""
    this class contains information and the chunks of JSON text needed for the project's postman file 
"""
class PostManObj:

    def __init__(self):
        self.zuul = Configuration.use_gateway_server
        self.info = '{"info": {"_postman_id": "XXX","name": "YYY","description" : "postman testing collection for the YYY project","schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},'
        self.item = '"item": ['
        self.requests = []
        self.closer = '],"protocolProfileBehavior": {}}'
        self.request_name = ''
