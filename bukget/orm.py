import api

try:
    from urllib.error import HTTPError
except ImportError:
    import api
    from urllib2 import HTTPError


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
            print json_object
            raise Exception('Missing slug in plugin!')
        self.json_object = json_object
        for key, value in json_object.items():
            if key == 'versions':
                self.versions = []
                for version in json_object[key]:
                    self.versions.append(Version(self, version))
                continue
            elif key == 'popularity':
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


class Category(object):
    ''' An object to hold categories.
    This is only used for category listing
    '''    
    def __init__(self, json_object):
        ''' Initialise a new Category object.
        Should be self-explanatory...
        '''
        for key, value in json_object.items():
            setattr(self, key, value)
            
    def plugins(server=None, **query):
        ''' List plugins in this category.
        This will call the category_plugins function in pybukget, and thus takes
        the same arguments except what category to list for.
        '''
        return category_plugins(self.name, server=server, **query)


class Author(object):
    ''' A object to hold authors.
    Only used by author listing
    '''
    def __init__(self, json_object):
        ''' Initialise a new Author object.
        Should be self-explanatory...
        '''
        for key, value in json_object.items():
            setattr(self, key, value)
    
    def plugins(self, server=None, **query):
        ''' List plugins by this author.
        This will call the author_plugins function in pybukget, and thus takes
        the same arguments except what author to list for.
        '''
        return author_plugins(self.name, server=server, **query)

    
def plugins(server='', **query):
    '''Retreives a list of plugin objects.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    query['fields'] = ['-nonexistant',]
    result = api.plugins(server, **query)
    if result is None: return None
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins


def plugin_details(server, plugin, version='', **query):
    '''Retreives the plugin object.
    Optionally a specific version can be specified.  All query variables
    specified by the API docs will work here.
    '''
    result = api.plugin_details(server, plugin, version=version, **query)
    if result is None: return None
    return Plugin(result)


def authors():
    '''Returns a list of authors and their plugin counts from the API.'''
    authors = []
    result = api.authors()
    if result is None: return None
    for author in result:
        authors.append(Author(author))
    return authors

    
def author_plugins(author, server=None, **query):
    '''Retreives a list of plugins written by the specified author.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    query['fields'] = ['-nonexistant',]
    result = api.author_plugins(author, server=server, **query)
    if result is None: return None
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins


def categories():
    '''Returns the category listing with the count of plugins for each cat.
    '''
    categories = []
    result = api.categories()
    if result is None: return None
    for category in categories:
        categories.append(Category(category))
    return categories


def category_plugins(category, server=None, **query):
    '''Retreives a list of plugins in the specified category.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    query['fields'] = ['-nonexistant',]
    result = api.category_plugins(category, server=server, **query)
    if result is None: return None
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins


def search(*filters, **query):
    '''Searching the API.
    This function is only utilizing the POST searching and is expecting properly
    ftted search dictionaries.  Also all of the same query variables as is
    described in the API3 docs will work here as well.
    '''
    plugins = []
    query['fields'] = ['-nonexistant',]
    result = api.search(*filters, **query)
    if result is None: return None
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins


def find_by_name(server, name):
    ''' Find the slug by the name supplied
    First the name is turned all lowercase and checked if that is the slug.
    If it is, it's returned. Else it searches for plugins with equal names and
    chooses the first one. If no plugin has the name, it searches for a plugin
    with a smiliar name. Will return None if no slug was found.

    NOTE: This is a ORM-compliant version of the api.find_by_name
    '''
    try:
        return plugin_details(server, api.find_by_name(server, name))
    except:
        return None


def get_by_main(server, main):
    ''' 
    Fetches the slug of the plugin based on the java class name (main)

    NOTE: This is a ORM-compliant version of the api.get_by_main
    '''
    try:
        return plugin_details(server, api.get_by_main(server, main))
    except:
        return None