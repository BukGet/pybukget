from distutils.core import setup
import bukget

setup(
    name='pyBukGet',
    version='1.0',
    description='Python Module for the BukGet JSON API',
    author='Steven McGrath',
    author_email='steve@chigeek.com',
    url='https://github.com/BukGet/bukget',
    py_modules=['bukget'],
    classifiers= [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)