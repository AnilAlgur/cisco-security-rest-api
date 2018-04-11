import logging
import base64
from rest import AppClient, RestJSONHandler, RestClient

logger = logging.getLogger(__name__)


class FXOSError(Exception):
    pass


class ASAClient(AppClient):
    """
    AppClient extension for ASA REST API.

    Workaround for CSCvh72007: Username and privilege display are incorrect when X-Auth-Token is used for REST API

    - Added extra Basic HTTP authentication header to be used in all requests.

    - Username:Password credentials need to be static.
    """
    def __init__(self, *args, **kwargs):
        self.AUTH_HTTP_STATUS = 204
        self.AUTH_REQ_HDR_FIELD = 'X-Auth-Token'
        self.AUTH_HDR_FIELD = 'X-Auth-Token'
        self.AUTH_URL = '/api/tokenservices'
        super(ASAClient, self).__init__(*args, **kwargs)

    def login(self, *args, **kwargs):
        # Set basic HTTP authentication header
        base64str = base64.b64encode('{}:{}'.format(self.username, self.password))
        self.hdrs_auth["Authorization"] = "Basic {}".format(base64str)
        # Set HTTP method for login
        self.login_method = 'POST'
        self.login_data = '{}'
        # Call super!
        super(ASAClient, self).login(*args, **kwargs)

    def logout(self, *args, **kwargs):
        # Set logout parameters
        self.logout_method = 'DELETE'
        self.logout_data = None
        # Set API URL for logout
        self.LOGOUT_URL = '/api/tokenservices/' + self.token

    def _req(self, *args, **kwargs):
        method = kwargs['method']
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            raise FXOSError("HTTP method {} is not supported".format(method))

        # Workaround for CSCvh72007
        # X-Auth-Token header will be added by AppClient class
        # Add additional Basic HTTP authentication header
        self.hdrs_req["Authorization"] = self.hdrs_auth["Authorization"]

        super(ASAClient, self)._req(*args, **kwargs)


class ASARestClient(RestClient, ASAClient, RestJSONHandler):
    """
    RestClient extension for ASA with ASAClient adn RestJSONHandler.

    Method Resolution Order:
    ```
    ASARestClient
    RestClient
    ASAClient
    AppClient
    RestJSONHandler
    RestDataHandler
    object
    ```
    """
    pass


class ASA(ASARestClient):
    """
    This class must be used to interact with ASA management REST API.

    # Parameters
    url: URL of the ASA REST API
    username: Login username for ASA REST API. Ensure that appropriate user role and permissions are assigned to perform
     all the intended tasks.
    password: Login password for ASA REST API.

    """
    def get_version(self):
        """
        GET ASA software version.
        """
        url = self.url + '/api/cli'
        data = {
            "commands": ["show version | in Version"]
        }
        resp = self._req(url, method='POST', data=data)
        if len(resp):
            logger.info('ASA Version is\n{}'.format(resp["response"][0]))

    def get_cli(self, cmds):
        """
        GET CLI commands output.

        # Parameters
        cmd: List of commands to be sent to ASA
        """
        url = self.url + '/api/cli'
        data = {
            "commands": cmds
        }
        resp = self._req(url, method='POST', data=data)
        if len(resp):
            for cmd, cmd_resp  in zip(cmds, resp["response"]):
                logger.info('Command: {}\nOutput is\n{}'.format(cmd, cmd_resp))

