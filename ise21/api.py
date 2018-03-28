import base64
import logging
from collections import OrderedDict
from rest import AppClient, RestXMLHandler, RestClient


logger = logging.getLogger(__name__)


class ISEError(Exception):
    pass


class ISEClient(AppClient):
    def __init__(self, *args, **kwargs):
        self.AUTH_HTTP_STATUS = 200
        self.AUTH_REQ_HDR_FIELD = 'Set-Cookie'
        self.AUTH_HDR_FIELD = 'Cookie'
        self.AUTH_URL = '/ers/sdk/'
        self.HDR_SEARCH_RESULT = 'application/vnd.com.cisco.ise.ers.searchresult.2.0+xml'
        self.HDR_RESOURCE = {
            'endpoint': 'application/vnd.com.cisco.ise.identity.endpoint.1.1+xml',
            'endpointgroup': 'application/vnd.com.cisco.ise.identity.endpointgroup.1.0+xml',
            'internaluser': 'application/vnd.com.cisco.ise.identity.internaluser.1.2+xml',
            'identitygroup': 'application/vnd.com.cisco.ise.identity.identitygroup.1.0+xml',
            'guestuser': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml',
            'networkdevice': 'application/vnd.com.cisco.ise.network.networkdevice.1.1+xml',
            'networkdevicegroup': 'application/vnd.com.cisco.ise.network.networkdevicegroup.1.0+xml'
        }
        self.HDR_ENDPOINT = 'application/vnd.com.cisco.ise.identity.endpoint.1.1+xml'
        self.HDR_INTERNAL_USER = 'application/vnd.com.cisco.ise.identity.internaluser.1.2+xml'
        self.HDR_ENDPOINT_GROUP = 'application/vnd.com.cisco.ise.identity.endpointgroup.1.0+xml'
        super(ISEClient, self).__init__(*args, **kwargs)

    def login(self, *args, **kwargs):
        base64str = base64.b64encode('{}:{}'.format(self.username, self.password))
        self.hdrs_auth["Authorization"] = "Basic {}".format(base64str)
        self.login_data = None
        self.login_method = 'POST'
        super(ISEClient, self).login(*args, **kwargs)

    def logout(self):
        self.cookie = ''
        self.LOGOUT_URL = ''

    def _req(self, *args, **kwargs):
        method = kwargs['method']
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise ISEError("HTTP method {} is not supported".format(method))

        super(ISEClient, self)._req(*args, **kwargs)
        

class ISERestClient(RestClient, ISEClient, RestXMLHandler):
# class ISERestClient(RestClient, ISEClient, RestPyxbHandler):
    """
    Method Resolution Order:
    ISERestClient
    RestClient
    ISEClient
    AppClient
    RestXMLHandler
    RestDataHandler
    object
    """
    pass


class ISE(ISERestClient):
    def __init__(self, url=None, username=None, password=None):
        """
        Initialize ISE object with URL. `username` and `password` 
        parameters are optional. If omitted, `login` method can be used.
        
        :param url: URL of the ISE server
        :param username: ISE username
        :param password: ISE password
        """
        super(ISE, self).__init__(url=url, username=username, password=password)

    def search_helper(self, resource, filter, page):
        dev_url = self.url + '/ers/config/' + resource # + filter + '&page=' + page
        XML_resp = self._req(dev_url,
                             http_accept=self.HDR_RESOURCE[resource],
                             http_search=self.HDR_SEARCH_RESULT,
                             params={'filter': filter, 'page': str(page)})
        logger.debug("Get-All {} page {}".format(resource, page))
        return XML_resp
        # for rsrc in XML_resp.iter('{ers.ise.cisco.com}resource'):
        #     logger.info(rsrc.attrib['name'] + ' --> ' + rsrc.attrib['id'])


    def endpoint_complex_search(self):
        resource = 'endpoint'
        page = 1
        dev_url = self.url + '/ers/config/' + resource # + filter + '&page=' + page
        # dev_url = dev_url + '?'
        # dev_url = dev_url + '&filter=groupId.EQ.a4a97d40-b4cb-11e5-8ffd-005056903ad0'
        dev_url = dev_url + '?filter=mac.STARTSW.00'
        dev_url = dev_url + '&filter=groupId.EQ.c5b18110-8a75-11e6-b4fd-005056926a52'
        dev_url = dev_url + '&filtertype=OR'
        XML_resp = self._req(dev_url,
                             http_accept=self.HDR_RESOURCE[resource],
                             http_search=self.HDR_SEARCH_RESULT)
        logger.debug("Get-All {} page {}".format(resource, page))
        return XML_resp

    def getAllSearchResults(self, resource, filter=None):
        page = 1
        XML_resp = self.search_helper(resource, filter, page)
        if len(XML_resp):
            yield XML_resp  # Blacnk string when request fails
        while len(XML_resp) and XML_resp.find("{v2.ers.ise.cisco.com}nextPage") is not None:
            page = page + 1
            XML_resp = self.search_helper(resource, filter, page)
            if len(XML_resp):
                yield XML_resp

    def getAllInternalUsers(self, filter=None):
        for XML_resp in self.getAllSearchResults('internaluser', filter=filter):
            yield XML_resp

    def getAllEndpoints(self, filter=None):
        for XML_resp in self.getAllSearchResults('endpoint', filter=filter):
            yield XML_resp

    def getAllEndpointIdGroups(self, filter=None):
        for XML_resp in self.getAllSearchResults('endpointgroup', filter=filter):
            yield XML_resp

    def getInternalUser(self, name=''):
        name_filter = 'name.EQ.' + name
        XML_resp = [xml_resp for xml_resp in self.getAllInternalUsers(filter=name_filter)][0]
        logger.info("Get Internal User Name {}".format(name))
        if not XML_resp.find('{ers.ise.cisco.com}resource'):
            logging.error("Internal User Name {} NOT FOUND!".format(name))
        for rsrc in XML_resp.iter('{ers.ise.cisco.com}resource'):
            logger.info(rsrc.attrib['name'] + ': ' + rsrc.attrib['description'] + ' --> ' + rsrc.attrib['id'])
            if rsrc.attrib['id'] is not None:
                self.getInternalUserById(rsrc.attrib['id'])
        return XML_resp

    def getInternalUserById(self, user_id):
        user_url = self.url + '/ers/config/internaluser/' + user_id
        XML_resp = self._req(user_url, http_accept=self.HDR_INTERNAL_USER)
        logger.info("Get Internal User {}".format(user_id))
        return XML_resp

    def createInternalUser(self, user_name, descr, group_id,
                           user_email = None, user_fname=None, user_lname=None,
                           fw_level=None, fmc_level=None, nw_level=None):
        # TODO: Build logic for getting template first and then generate this OrderedDict
        user_dict = OrderedDict([
            ('changePassword','false'),
            ('customAttributes', OrderedDict([
                ('entry', OrderedDict([
                    ('key', 'FIREWALL'),
                    ('value', fw_level)
                ])),
                ('entry', OrderedDict([
                    ('key', 'FMC'),
                    ('value', fmc_level)
                ])),
                ('entry', OrderedDict([
                    ('key', 'NETWORK'),
                    ('value', nw_level)
                ]))
            ])),
            ('email', user_email),
            ('enablePassword', 'ENABLEPASSWD!'),
            ('enabled', 'false'),
            ('expiryDateEnabled', 'false'),
            ('firstName', user_fname),
            ('identityGroups', group_id),
            ('lastName', user_lname),
            ('password', 'PSWDPSWD!'),
            ('passwordIDStore', 'RSA_RADIUS')
        ])

        xml_data = self._dict2xml('{identity.ers.ise.cisco.com}internaluser', user_name, descr, user_dict)
        dev_url = self.url + '/ers/config/internaluser'
        XML_resp = self._req(
            dev_url, method='POST', data=xml_data,
            http_accept=self.HDR_INTERNAL_USER,
            http_content=self.HDR_INTERNAL_USER + '; charset=utf-8')
        logger.info("Created Internal User: {}".format(user_name))
        return XML_resp

    def getEndpointByName(self, mac_addr):
        mac_filter = 'mac.EQ.' + mac_addr
        mac_search = [XML_resp for XML_resp in self.getAllEndpoints(filter=mac_filter)][0]
        mac_id = ''
        if len(mac_search[0]):
            mac_id = mac_search[0][0].get('id')
        return mac_id

    def getEndpoint(self, mac_addr):
        mac_filter = 'mac.EQ.' + mac_addr
        XML_resp = [xml_resp for xml_resp in self.getAllEndpoints(filter=mac_filter)][0]
        logger.info("Get Endpoint {}".format(mac_addr))
        if not XML_resp.find('{ers.ise.cisco.com}resource'):
            logging.error("Endpoint {} NOT FOUND!".format(mac_addr))
        for rsrc in XML_resp.iter('{ers.ise.cisco.com}resource'):
            logger.info(rsrc.attrib['name'] + ' --> ' + rsrc.attrib['id'])
            if rsrc.attrib['id'] is not None:
                self.getEndpointById(rsrc.attrib['id'])
        return XML_resp

    def getEndpointById(self, endpt_id):
        dev_url = self.url + '/ers/config/endpoint/' + endpt_id
        XML_resp = self._req(dev_url,
                             http_accept=self.HDR_ENDPOINT,
                             http_content=self.HDR_ENDPOINT + '; charset=utf-8')
        logger.debug("Get Network Endpoint {}".format(endpt_id))
        return XML_resp
    
    def updateEndpointById(self, endpt_id, xml_data):
        dev_url = self.url + '/ers/config/endpoint/' + endpt_id
        XML_resp = self._req(
            dev_url, method='PUT', data=xml_data,
            http_accept=self.HDR_ENDPOINT,
            http_content=self.HDR_ENDPOINT + '; charset=utf-8')
        logger.info("Update Network Endpoint {}".format(endpt_id))
        return XML_resp
    
    def createEndpoint(self, endpt_mac, descr, group_id):
        endpt_dict = OrderedDict([
                ('customAttributes',OrderedDict([
                    ('customAttributes',None)
                    ])),
                ('groupId', group_id),
                ('identityStore', None),
                ('identityStoreId', None),
                ('mac', endpt_mac),
                ('portalUser', None),
                ('profileId', None),
                ('staticGroupAssignment', 'true'),
                ('staticProfileAssignment', 'false')
                ])

        xml_data = self._dict2xml('{identity.ers.ise.cisco.com}endpoint', endpt_mac, descr, endpt_dict)
        dev_url = self.url + '/ers/config/endpoint'
        XML_resp = self._req(
            dev_url, method='POST', data=xml_data, 
            http_accept=self.HDR_ENDPOINT,
            http_content=self.HDR_ENDPOINT + '; charset=utf-8')
        logger.info("Created Network Endpoint")
        return XML_resp
    
    def getEndpointIdGroupById(self, group_id):
        dev_url = self.url + '/ers/config/endpointgroup/' + group_id
        XML_resp = self._req(dev_url, http_accept=self.HDR_ENDPOINT_GROUP)
        logger.info("Get Endpoint ID Group {}".format(group_id))
        return XML_resp
    
    def getEndpointIdGroupByName(self, group_name):
        group_filter = '?filter=name.EQ.' + group_name
        group_search = self.getAllEndpointIdGroups(filter=group_filter)
        group_id = ''
        for child in group_search[0]:
            group_id = child.get('id')
        return group_id

