try:
    from bukget import api
    from bukget.plugin import Plugin
    from bukget.author import Author
    from bukget.category import Category
    from urllib.error import HTTPError
except ImportError:
    import api
    from plugin import Plugin
    from author import Author
    from category import Category
    from urllib2 import HTTPError

def _levenshtein(s1, s2):
    """ Get the levenshtein edit distance between two strings
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def _get_best_match(to_match, possible_matches):
    """ Return the value in possible_matches that has the smallest edit
    distance to to_match
    """
    lowest_distance = -1
    distances = {}
    for match in possible_matches:
        distance = _levenshtein(to_match, match)
        if lowest_distance < 0 or distance < lowest_distance:
            lowest_distance = distance
        if lowest_distance == 0:
            break
    for match in distances:
        if distances[match] == lowest_distance:
            return match
    return None

def find_slug(server, name):
    ''' Find the slug by the name supplied
    First the name is turned all lowercase and checked if that is the slug.
    If it is, it's returned. Else it searches for plugins with equal names and
    chooses the first one. If no plugin has the name, it searches for a plugin
    with a smiliar name. Will return None if no slug was found
    '''
    # First we are testing if the name is the same as the slug
    try:
        if api.plugin_details(server, name.lower().replace(' ', '-'),
                        fields='slug') is not None:
            return name.lower().replace(' ', '-')
    except HTTPError:
        pass

    # Then we search for a plugin with name that matches
    search_result = api.search({'field': 'plugin_name', 'action': '=', 'value': 
                            name}, {'field': 'server', 'action': '=', 'value':
                            server}, fields='slug')
    if len(search_result) > 0:
        return search_result[0]['slug']

    # Then we search for a plugin with a name like it
    search_result = api.search({'field': 'plugin_name', 'action': 'like', 'value':
                            name}, {'field': 'server', 'action': '=', 'value':
                            server}, fields='slug')
    if len(search_result) > 0:
        return _get_best_match(name, [i['slug'] for i in search_result])
    
    #No plugin found =(
    return None
    
def plugins(server='', **query):
    '''Retreives a list of plugin objects.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    result = api.plugins(server **query)
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins

def plugin_details(server, plugin, version='', **query):
    '''Retreives the plugin object.
    Optionally a specific version can be specified.  All query variables
    specified by the API docs will work here.
    '''
    result = api.plugin_details(server, plugin, version=version, **query)
    return Plugin(result)

def authors():
    '''Returns a list of authors and their plugin counts from the API.'''
    authors = []
    result = api.authors()
    for author in result:
        authors.append(Author(author))
    return authors
    
def author_plugins(author, server=None, **query):
    '''Retreives a list of plugins written by the specified author.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    result = api.author_plugins(author, server=server, **query)
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins

def categories():
    '''Returns the category listing with the count of plugins for each cat.
    '''
    categories = []
    result = api.categories()
    for category in categories:
        categories.append(Category(category))
    return categories

def category_plugins(category, server=None, **query):
    '''Retreives a list of plugins in the specified category.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    plugins = []
    result = api.category_plugins(category, server=server, **query)
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins
    
def search(*filters, **query):
    '''Searching the API.
    This function is only utilizing the POST searching and is expecting properly
    formatted search dictionaries.  Also all of the same query variables as is
    described in the API3 docs will work here as well.
    '''
    plugins = []
    result = api.search(*filters, **query)
    for plugin in result:
        plugins.append(Plugin(plugin))
    return plugins

