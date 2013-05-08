import pybukget
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
    
    def plugins(server=None, **query):
        ''' List plugins by this author.
        This will call the author_plugins function in pybukget, and thus takes
        the same arguments except what author to list for.
        '''
        return pybukget.author_plugins(self.name, server=server, **query)
