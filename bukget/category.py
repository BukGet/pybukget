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
        return pybukget.category_plugins(self.name, server=server, **query)
