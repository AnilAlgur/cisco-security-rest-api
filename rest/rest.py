import requests
import logging

logger = logging.getLogger(__name__)


class RestClientError(Exception):
    pass


class RestDataHandler(object):
    """
    Abstract class for working with different data representations such as JSON or XML. Data handler classes for JSON
    and XML are already part of this repository. Other data handler may as well be created if required. If application
    requires more specific data handling beyond what JSON and XML data handlers provide, they can be extended as well
    for use with specific `RestClient` extension.
    """
    def __init__(self, *args, **kwargs):
        self.hdrs_auth = {}
        self.hdrs_req = {}

    def handle_response(self, resp):
        """Child must override"""
        pass


class AppClient(object):
    """
    Abstract class for working with different applications. This must be sub-classed to create application specific
    client and these variables must be overriden:
    
    `AUTH_URL`: Suffix of URL that must be appended to server FQDN in order to invoke REST API authentication.

    `LOGOUT_URL`: Suffix of URL that must be appended to server FQDN in order to logout from REST API server.

    `AUTH_HTTP_STATUS`: HTTP status returned after successful authentication, e.g. it could be 200 or 201

    `AUTH_REQ_HDR_FIELD`: Header field received in the authentication response that'll provide token or cookie that 
    must be used in subsequent requests to the REST server.

    `AUTH_HDR_FIELD`: Header field to be used in all the requests to the REST server after authentication is completed.

    If required, other methods such as `login`, `logout` may also be overridden. e.g.

    ```python
    def login(self, *args, **kwargs):
        # Populate authentication headers
        self.hdrs_auth["USERNAME"] = self.username
        self.hdrs_auth["PASSWORD"] = self.password
        # Set HTTP method for login
        self.login_method = 'POST'
        # Call super!
        super(ExampleAppClient, self).login(*args, **kwargs)

    def logout(self, *args, **kwargs):
        # Set API URL for logout
        self.LOGOUT_URL = '/api/logout'
    ```

    Check the application clients available in this repository to learn more about how `AppClient` can be extended for
    use with specific applications.
    """
    AUTH_URL = 'App/Must/Override'
    LOGOUT_URL = 'App/Must/Override'
    AUTH_HTTP_STATUS = 200
    AUTH_REQ_HDR_FIELD = 'App-Must-Override'
    AUTH_HDR_FIELD = 'App-Must-Override'

    def __init__(self, *args, **kwargs):
        self.hdrs_auth = {}
        self.hdrs_req = {}
        super(AppClient, self).__init__(*args, **kwargs)

    def _req(self, *args, **kwargs):
        self.hdrs_req[self.AUTH_HDR_FIELD] = self.token
        super(AppClient, self)._req(*args, **kwargs)


class RestClient(AppClient, RestDataHandler):
    """
    Generic REST client that can be extended to interact with any application supporting any data representation
    format. Appropriate `AppClient` and `RestDataHandler` must be provided for this to work correctly.

    `RestClient` is designed to allow application specific extensions to focus more on application use-cases, be better
    readable and abstract out underlying REST specific function as much as possible.

    Initialize `RestClient` with `URL`, `username` and `password` parameters.

    # Parameters
    url: URL of the REST API server
    username: Login username for REST API server
    password: Login password for REST API server
    """

    def __init__(self, url=None, username=None, password=None):
        if url is None:
            logger.fatal("REST API Server URL needs to be specified")
            exit(1)

        self.url = url     # Server URL
        self.token = None  # Authentication token
        self.username = username
        self.password = password
        self.session = requests.Session()
        super(RestClient, self).__init__()
        if self.username and self.password:
            self.login()

    def login(self, method='POST'):
        """
        The login method authenticates a REST client attempting to access the services provided by the REST server. 
        This method must be called prior to any other method called on other services.
        """
        self.login_data = ""
        super(RestClient, self).login()
        url_token = self.url + self.AUTH_URL
        try:
            logging.debug(url_token)
            # resp = self.session.post(url_token, data=self.login_data, headers=self.hdrs_auth, verify=False)
            req = requests.Request(
                method=self.login_method, url=url_token,
                data=self.login_data, headers=self.hdrs_auth)
            prep_req = self.session.prepare_request(req)
            resp = self.session.send(prep_req, verify=False)
            # status_code = f.getcode()
            if resp.status_code != self.AUTH_HTTP_STATUS:
                logger.fatal("Error code {} in the HTTP request".format(resp.status_code))
                exit(1)
            self.token = resp.headers.get(self.AUTH_REQ_HDR_FIELD, default=None)
            logging.info("{}: Login Successful!".format(self.url))
            logging.debug("REST API Server Auth token: {}".format(self.token))
        except requests.exceptions.HTTPError as err:
            self._handle_http_err(err)
            raise RestClientError("Login to REST API Server Failed!!")

    def logout(self):
        """
        The logout method notifies the REST server that a previously authenticated REST client is no longer requiring 
        session access to the server.
        """
        self.logout_data = 'LOGOUT'
        self.logout_method = 'POST'
        super(RestClient, self).logout()
        if self.LOGOUT_URL:
            url = self.url + self.LOGOUT_URL
            self._req(url, method=self.logout_method, data=self.logout_data)
        logging.info("{}: Logout Successful!".format(self.url))

    def _req(self, url, method='GET', data=None, **kwargs):
        """
        RestClient Internal function. Submit request towards RSET API server, checks return status and parses return
        content.

        # Parameters
        path: Path to append to server URL
        method: REST API method, can be any of methods supported by application.
        data: Request data

        return: Response from REST server
        """
        if url is None:
            raise RestClientError("REST URL needs to be specified")

        super(RestClient, self)._req(method=method, data=data, **kwargs)
        req_data = self.prepare_data(data=data, **kwargs)

        if method in ['GET', 'DELETE'] and data is not None:
            raise RestClientError("HTTP 'GET' or 'DELETE' can only accept data=None")

        logger.debug('{} data: {}'.format(method, req_data))

        obj_resp = ''  # len(json_resp) = 0 if HTTP request fails
        r = None
        try:
            logger.debug("Requesting {} for {}".format(method, url))
            req = requests.Request(method, url, data=req_data, headers=self.hdrs_req, params=kwargs.get('params'))
            prep_req = self.session.prepare_request(req)
            r = self.session.send(prep_req, verify=False)
            if r.status_code not in [200, 201, 202, 204]:
                # 200-OK, 201-Created, 202-Accepted, 204-No Content
                r.raise_for_status()
                logger.error(
                    "Error code {} in the HTTP request".format(r.status_code))
                if r.text is not None:
                    logging.debug("Error message:\n{}".format(r.text))
                return obj_resp
            resp = r.text  # logout method returns nothing
            if len(resp):
                # print(resp)
                obj_resp = self.handle_response(resp)
        except requests.exceptions.HTTPError, err:
            self._handle_http_err(err)
        return obj_resp

    def __enter__(self):
        return self

    def __exit__(self, errtype, errvalue, errtb):
        if errtype == RestClientError:
            logging.fatal(errvalue)
        else:
            self.logout()

    def handle_response(self, resp):
        """
        Parse the response data. This is overridden by DataHandler class for content-type specific functions.
        """
        obj = super(RestClient, self).handle_response(resp)
        return obj
