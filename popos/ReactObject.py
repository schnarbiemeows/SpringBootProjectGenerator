class ReactObject:

    def __init__(self):
        self.title = ''
        self.tablenames = []
        self.tabledata = {}
        self.fieldnames = {}
        self.fieldtypes = {}
        # these 3 fields contain information needed by the app.modules.ts file, and the app-routing.module.ts
        self.names = []
        self.components = []
        self.selectors = []
        self.routes = []
        self.modules = []
        self.services = set()
        self.dto_names = []
        self.dto_tablename_mapping = {}
        self.rest_call_names = {}
        self.rest_call_types = {}
        self.rest_call_parameters = {}