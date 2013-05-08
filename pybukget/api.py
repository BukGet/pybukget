import json
try:
    from urllib import urlencode
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    

__author__ = 'Steven McGrath'
__version__ = '1.0.0'

USER_AGENT='pyBukGet 1.0'
BASE = 'http://api.bukget.org/3'

def _request(url, data=None, headers={}, query={}):
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
    if 'fields' in query and ' ' in query['fields']:
        query['fields'] = ','.join(query['fields'])

    # Append the query to the URL if we have anything in the query dictionary.
    if len(query) > 0:
        url += '?%s' % '&'.join(['%s=%s' % (q, query[q]) for q in query])

    # Lastly, if there is anything in the data variable, then urlencode it.
    if data is not None:
        data = urlencode(data)

    # Time to set the User-Agent string and actually query the API!
    headers['User-Agent'] = USER_AGENT
    print(BASE + url)
    print(query)
    return urlopen(Request(BASE + url, data, headers)).read().decode("utf-8")

def _ensure_slug(query):
    ''' Ensure that the fields contains slug.
    '''
    if hasattr(query, 'fields'):
        if query['fields'].startswith('-'):
            if '-slug,' in query['fields']:
                query['fields'] = query['fields'].replace('-slug,', '')
            elif '-slug' in query['fields']:
                query['fields'] = query['fields'].replace('-slug', '')
        elif 'slug' not in query['fields']:
            query['fields'] = query['fields'] + ',slug'
    return query

def plugins(server='', **query):
    '''Retreives a list of plugins.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''
    call = '/plugins/%s' % server
    return json.loads(_request(call, query=_ensure_slug(query)))


def plugin_details(server, plugin, version='', **query):
    '''Retreives the plugin details.
    Optionally a specific version can be specified.  All query variables
    specified by the API docs will work here.
    '''
    call = '/plugins/%s/%s/%s' % (server, plugin, version)
    return json.loads(_request(call, query=_ensure_slug(query)))


def plugin_download(server, plugin, version):
    '''Downloads the plugin binary.
    This function will return the raw data stream from the API.  We will NOT be
    returning dictionaries in this case!
    '''
    call = '/plugins/%s/%s/%s/download' % (server, plugin, version)
    return _request(call)


def authors():
    '''Returns a list of authors and their plugin counts from the API.'''
    return json.loads(_request('/authors'))


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
        call = '/authors/%s' % name
    return json.loads(_request(call, query=_ensure_slug(query)))


def categories():
    '''Returns the category listing with the count of plugins for each cat.'''
    return json.loads(_request('/categories'))


def category_plugins(category, server=None, **query):
    '''Retreives a list of plugins in the specified category.
    Optionally you can specity a server and any query variables per the API
    Documentation.
    '''

    # Depending on if the server variable is set, we can have one of 2
    # different URLs, so here we will set the call to the correct one.
    if server is not None:
        call = '/categories/%s/%s' % (server, author)
    else:
        call = '/categories/%s' % name
    return json.loads(_request(call, query=_ensure_slug(query)))


def search(*filters, **query):
    '''Searching the API.
    This function is only utilizing the POST searching and is expecting properly
    formatted search dictionaries.  Also all of the same query variables as is
    described in the API3 docs will work here as well.
    '''
    query['filters'] = json.dumps(filters)
    return json.loads(_request('/search', data=_ensure_slug(query)))
