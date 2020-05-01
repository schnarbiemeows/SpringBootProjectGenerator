"""
    This class represents an Angular 8 UI project
"""
class AngularObject:

    def __init__(self):
        self.title = ''
        self.fieldnames = {}
        self.fieldtypes = {}
        # these 3 fields contain information needed by the app.modules.ts file, and the app-routing.module.ts
        self.names = []
        self.components = []
        self.selectors = []
        self.routes = []
        self.modules = []
        self.services = []
        self.dto_names = []
        self.urls = {}
        self.rest_call_names = {}
        self.rest_call_types = {}
        self.rest_call_parameters = {}