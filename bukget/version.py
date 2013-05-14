class Version(object):
    ''' A class to hold version objects.
    Everythin is named the same as in the json api. Commands and versions are
    converted to objects.
    '''
    def __init__(self, plugin, json_object):
        self.json_object = json_object
        for key, value in json_object.items():
            if key is 'commands':
                self.commands = []
                for version in json_object[key]:
                    self.commands.append(Command(self, version))
                continue
            elif key is 'permissions':
                self.permissions = []
                for permission in json_object[key]:
                    self.permissions.append(Permission(self, permission))
                continue
            setattr(self, key, value)
    
    class Command(object):
    
        def __init__(self, json_object):
            self.json_object = json_object
            for key, value in json_object.items():
                setattr(self, key, value)
                    
    class Version(object):
    
        def __init__(self, json_object):
            self.json_object = json_object
            for key, value in json_object.items():
                setattr(self, key, value)
