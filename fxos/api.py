import logging
from rest import AppClient, RestJSONHandler, RestClient

logger = logging.getLogger(__name__)


class FXOSError(Exception):
    pass


class FXOSClient(AppClient):
    """
    AppClient extension for FXOS REST API.
    """
    def __init__(self, *args, **kwargs):
        self.AUTH_HTTP_STATUS = 200
        self.AUTH_REQ_HDR_FIELD = 'token'
        self.AUTH_HDR_FIELD = 'TOKEN'
        self.AUTH_URL = '/api/login'
        super(FXOSClient, self).__init__(*args, **kwargs)

    def login(self, *args, **kwargs):
        # Populate authentication headers
        self.hdrs_auth["USERNAME"] = self.username
        self.hdrs_auth["PASSWORD"] = self.password
        # Set HTTP method for login
        self.login_method = 'POST'
        # Call super!
        super(FXOSClient, self).login(*args, **kwargs)

    def logout(self, *args, **kwargs):
        # Set API URL for logout
        self.LOGOUT_URL = '/api/logout'

    def _req(self, *args, **kwargs):
        method = kwargs['method']
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise FXOSError("HTTP method {} is not supported".format(method))

        super(FXOSClient, self)._req(*args, **kwargs)


class FXOSRestClient(RestClient, FXOSClient, RestJSONHandler):
    """
    RestClient extension for FXOS with FXOSClient adn RestJSONHandler.

    Method Resolution Order:
    ```
    FXOSRestClient
    RestClient
    FXOSClient
    AppClient
    RestJSONHandler
    RestDataHandler
    object
    ```
    """
    pass


class FXOS(FXOSRestClient):
    """
    This class must be used to interact with FXOS management REST API.

    # Parameters
    url: URL of the FMC server
    username: Login username for FXOS chassis. Ensure that appropriate user role and permissions are assigned
    to perform all the intended tasks.
    password: Login password for FXOS chassis.

    """
    def get_version(self):
        """
        GET FXOS software version.
        """
        url = self.url + '/api/sys/firmware/version/mgmt'
        resp = self._req(url)
        if len(resp):
            self.version = resp['firmwareRunning'][0]['packageVersion']
            logger.info('FXOS Software {} Version is {}'.format(self.url, self.version))

