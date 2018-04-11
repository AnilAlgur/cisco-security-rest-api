"""
This module allows abstraction of REST client and creates foundation for interacting with any application using any 
data representation such as JSON or XML. 
"""

from .rest import *
from xml_handler import *
from json_handler import *

__author__ = "Chetankumar Phulpagare"
__copyright__ = ""
__credits__ = ["Chetankumar Phulpagare"]
__email__ = "chetanph"
__all__ = ['RestClient', 'AppClient', 'RestClientError', 'RestDataHandler', 'RestXMLHandler', 'RestJSONHandler']
