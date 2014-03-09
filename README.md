## What is pyBukGet?

pyBukGet is a client-side module for interfacing with the BukGet API over Python.  This module was written by the developer of the BukGet API itself and acts as a reference on how to properly communicate to BukGet.

## How do I install this?

pyBukGet is available vie pip and easy_install.  You can also manually install pyBukget by simply downloading the code here and installing it using setup.

#### Examples:

__Using pip:__

`pip install pybukget`

__Using Easy_Install:__

`easy_install pybukget`

__Manually:__

`python setup.py install`

## How do I use the API?

More detailed walkthrough is coming soon, however here are the available functions:

* plugins
* plugin_details
* plugin_download
* authors
* author_plugins
* categories
* category_plugins
* search

Overloadable variables:

* bukget.USER_AGENT - This should be set to whatever your application is.  By default, it will report as pyBukGet 2.3.