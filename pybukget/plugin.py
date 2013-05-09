try:
    from pybukget.version import Version
except ImportError:
    from version import Version

class Plugin(object):
    ''' An Object to hold Plugins.
    All atributes are the same name as the json names except the popularity.
    Popularity is stored in attributes named 'popularity_daily', 
    'popularity_weekly' and 'popularity_monthly'. Versions is turned into an
    array of Version objects. __eg__ is owerwritten, so you can use == to check
    if they are the same plugin.
    '''

    def __init__(self, json_object):
        ''' Initialise a new Plugin object.
        This will take values from the json_object and set them as attributes,
        The version value will be parsed into its own Version object
        '''
        if not 'slug' in json_object:
            raise Exception('Missing slug in plugin!')
        self.json_object = json_object
        for key, value in json_object.items():
            if key is 'version':
                self.versions = []
                for version in json_object[key]:
                    self.versions.append(Version(self, version))
                continue
            elif key is 'popularity':
                for key2, value2 in json_object[key].items():
                    setattr(self, key + '_' + key2, value2)
                continue
            setattr(self, key, value)
    
    def __eq__(self, other):
        return self.slug == other.slug
    
    def __hash__(self):
        return hash(self.slug)
    
    def join(self, other):
        return Plugin(self.json_object.update(other))
        
