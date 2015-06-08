import json
try:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
except ImportError:
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode

__author__ = 'Steven McGrath'
__version__ = '2.3.1'
USER_AGENT='pyBukGet %s' % __version__
BASE = 'http://api.bukget.org/3'


def _request(url, data=None, jsonify=True, headers={}, query={}):
    '''Base Request
    The parent function that all public functions call in order to initiate
    communication to the API.  Simply converts the Pythonic values into the
    the URL format expected by the API.  Also will add the User-Agent defined
    by the USER_AGENT variable.
    '''

    # There is no reason for there ever to be a callback specified.  If we see
    # one, just remove it.
    if 'callback' in query: del(query['callback'])

    # Here we will collapse the fields list if we see it into a string as is
    # expected by the API.
    if 'fields' in query and (' ' in query['fields'] or\
                              isinstance(query['fields'], list)):
        query['fields'] = ','.join(query['fields'])
    if data is not None and 'fields' in data and (' ' in data['fields'] or\
                              isinstance(data['fields'], list)):
        data['fields'] = ','.join(data['fields'])

    # Append the query to the URL if we have anything in the query dictionary.
    if len(query) > 0:
        url += '?%s' % '&'.join(['%s=%s' % (q, query[q]) for q in query])

    # Lastly, if there is anything in the data variable, then urlencode it.
    if data is not None:
        data = urlencode(data).encode('utf-8')

    # Time to set the User-Agent string and actually query the API!
    headers['User-Agent'] = USER_AGENT
    try:
        response = urlopen(Request(BASE + url, data, headers)).read()
    except HTTPError:
        return None
    else:
        if jsonify:
            return json.loads(response.decode("utf-8"))
        else:
            return response


def plugins(server='', **query):
    '''Retreives a list of plugins.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    call = '/plugins/%s' % server
    return _request(call, query=query)


def plugin_details(server, plugin, version='', **query):
    '''Retreives the plugin details.
    Optionally a specific version can be specified.  All query variables
    specified by the API docs will work here.
    '''
    call = '/plugins/%s/%s/%s' % (server, plugin, version)
    return _request(call, query=query)


def plugin_download(server, plugin, version):
    '''Downloads the plugin binary.
    This function will return the raw data stream from the API.  We will NOT be
    returning dictionaries in this case!
    '''
    call = '/plugins/%s/%s/%s/download' % (server, plugin, version)
    return _request(call, jsonify=False)


def authors():
    '''Returns a list of authors and their plugin counts from the API.'''
    return _request('/authors')


def author_plugins(author, server=None, **query):
    '''Retreives a list of plugins written by the specified author.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''

    # Depending on if the server variable is set, we can have one of 2
    # different URLs, so here we will set the call to the correct one.
    if server is not None:
        call = '/authors/%s/%s' % (server, author)
    else:
        call = '/authors/%s' % author
    return _request(call, query=query)


def categories():
    '''Returns the category listing with the count of plugins for each cat.'''
    return _request('/categories')


def category_plugins(category, server=None, **query):
    '''Retreives a list of plugins in the specified category.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''

    # Depending on if the server variable is set, we can have one of 2
    # different URLs, so here we will set the call to the correct one.
    if server is not None:
        call = '/categories/%s/%s' % (server, category)
    else:
        call = '/categories/%s' % category
    return _request(call, query=query)


def search(*filters, **query):
    '''Searching the API.
    This function is only utilizing the POST searching and is expecting properly
    formatted search dictionaries.  Also all of the same query variables as is
    described in the API3 docs will work here as well.
    '''
    query['filters'] = json.dumps(filters)
    return _request('/search', data=query)


def _levenshtein(s1, s2):
    """ Get the levenshtein edit distance between two strings
    """
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
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


def find_by_name(server, name):
    ''' Find the slug by the name supplied
    First the name is turned all lowercase and checked if that is the slug.
    If it is, it's returned. Else it searches for plugins with equal names and
    chooses the first one. If no plugin has the name, it searches for a plugin
    with a smiliar name. Will return None if no slug was found
    '''
    # First we are testing if the name is the same as the slug
    try:
        if plugin_details(server, name.lower().replace(' ', '-'),
                          fields='slug') is not None:
            return name.lower().replace(' ', '-')
    except HTTPError:
        pass

    # Then we search for a plugin with name that matches
    search_result = search({
                'field': 'plugin_name', 
                'action': '=', 'value': name
            }, {
                'field': 'server', 
                'action': '=', 'value': server
            }, 
            fields='slug')
    if len(search_result) > 0:
        return search_result[0]['slug']

    # Then we search for a plugin with a name like it
    search_result = search({
                'field': 'plugin_name', 
                'action': 'like', 'value': name
            }, {
                'field': 'server', 
                'action': '=', 'value': server
            }, 
            fields='slug')
    if len(search_result) > 0:
        return _get_best_match(name, [i['slug'] for i in search_result])
    
    #No plugin found =(
    return None


def get_by_main(server, main):
    ''' 
    Fetches the slug of the plugin based on the java class name (main)
    '''
    search_result = search({
                'field': 'main', 
                'action': '=', 'value': main
            }, {
                'field': 'server', 
                'action': '=', 'value': server
            }, 
            fields='slug')
    if len(search_result) > 0:
        return search_result[0]['slug']
    else:
        return None
