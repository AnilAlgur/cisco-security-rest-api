"""
Firepower Management Center API
===============================

Python module for interacting with Cisco Firepower Management Center (FMC). This module is based on FMC 6.1 REST API
specification.

Please check the examples in the repository for guidance on how to use this module.
"""

from .api import FMC
from .api import FPObject
from .api import FPObjectTable
from .api import FPPolicyTable
from .api import FPDeviceTable

__author__ = "Chetankumar Phulpagare"
__copyright__ = "Copyright 2017, Cisco"
__credits__ = ["Chetankumar Phulpagare"]
__email__ = "cphulpag@cisco.com"
__all__ = ['FMC', 'FPObject', 'FPObjectTable', 'FPDeviceTable', 'FPPolicyTable']