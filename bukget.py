import json
import urllib
import urllib2


USER_AGENT='pyBukGet 1.0'
BASE = 'http://dev.bukget.org/3'

def _request(url, data=None, headers={}, query={}):
    '''Base Request
    '''
    if 'fields' in query:
        query['fields'] = ','.join(query['fields'])
    if len(query) > 0:
        url += '?%s' % '&'.join(['%s=%s' % (q, query[q]) for q in query])
    if data is not None:
        data = urllib.urlencode(data)
    headers['User-Agent'] = USER_AGENT
    return urllib2.urlopen(urllib2.Request(BASE + url, data, headers)).read()


def plugins(server='', **query):
    '''Get plugins'''
    call = '/plugins/%s' % server
    return json.loads(_request(call, query=query))


def plugin_details(server, plugin, version='', **query):
    '''Plugin Details'''
    call = '/plugins/%s/%s/%s' % (server, plugin, version)
    return json.loads(_request(call, query=query))


def plugin_download(server, plugin, version):
    '''Plugin Download'''
    call = '/plugins/%s/%s/%s/download' % (server, plugin, version)
    return _request(call)


def authors():
    '''Authors'''
    return json.loads(_request('/authors'))


def author_plugins(author, server=None, **query):
    '''Author Plugins'''
    if server is not None:
        call = '/authors/%s/%s' % (server, author)
    else:
        call = '/authors/%s' % name
    return json.loads(_request(call, query=query))


def categories():
    '''Category Listing'''
    return json.loads(_request('/categories'))


def category_plugins(category, server=None, **query):
    '''Category plugin Listing'''
    if server is not None:
        call = '/categories/%s/%s' % (server, author)
    else:
        call = '/categories/%s' % name
    return json.loads(_request(call, query=query))


def search(*filters, **query):
    '''Basic Search Functionality'''
    query['filters'] = json.dumps(filters)
    return json.loads(_request('/search', data=query))