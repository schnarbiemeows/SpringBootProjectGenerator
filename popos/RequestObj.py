
"""
    this class contains the information and the chunks of JSON text needed for each request
"""
class RequestObj:

    def __init__(self):
        self.opener = "{"
        self.path_name = ''
        self.name = '"name": "XXX",'
        self.request = '"request": {'
        self.method_type = ''
        self.method = '"method": "XXX",'
        self.header = '"header": [],'
        self.body = '"body": { "mode": "raw","raw": {},"options": {"raw": { "language" : "json" }}},'
        self.raw = ''
        self.url_raw = '"raw": "XXX",'
        self.host = ''
        self.url_host = '"host": [ "XXX" ],'
        self.path = ''
        self.url_path = '"path": [ XXX ]'
        self.url = '"url": {X1X2X3}'
        self.response = '},"response": []'
        self.closer = "}"
