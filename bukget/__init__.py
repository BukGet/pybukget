try:
    from bukget.pybukget import *
    from bukget.api import plugin_download
except ImportError:
    from bukget import *
    from api import plugin_download
