<h1 id="rest">rest</h1>


This module allows abstraction of REST client and creates foundation for interacting with any application using any
data representation such as JSON or XML.

<h1 id="rest.RestClient">RestClient</h1>

```python
RestClient(self, url=None, username=None, password=None)
```

Generic REST client that can be extended to interact with any application supporting any data representation
format. Appropriate `AppClient` and `RestDataHandler` must be provided for this to work correctly.

`RestClient` is designed to allow application specific extensions to focus more on application use-cases, be better
readable and abstract out underlying REST specific function as much as possible.

Initialize `RestClient` with `URL`, `username` and `password` parameters.

__Parameters__

- __url__: URL of the REST API server
- __username__: Login username for REST API server
- __password__: Login password for REST API server

<h1 id="rest.RestClient.login">login</h1>

```python
RestClient.login(self, method='POST')
```

The login method authenticates a REST client attempting to access the services provided by the REST server.
This method must be called prior to any other method called on other services.

<h1 id="rest.RestClient.logout">logout</h1>

```python
RestClient.logout(self)
```

The logout method notifies the REST server that a previously authenticated REST client is no longer requiring
session access to the server.

<h1 id="rest.RestClient._req">_req</h1>

```python
RestClient._req(self, url, method='GET', data=None, **kwargs)
```

RestClient Internal function. Submit request towards RSET API server, checks return status and parses return
content.

:param path: Path to append to URI
:param method: REST API method, can be any of
    'GET','POST','PUT','DELETE'
:param data: Request data
:return: Response from REST server

<h1 id="rest.RestClient.handle_response">handle_response</h1>

```python
RestClient.handle_response(self, resp)
```

Parse the response data. This is overridden by DataHandler class for content-type specific functions.

<h1 id="rest.AppClient">AppClient</h1>

```python
AppClient(self, *args, **kwargs)
```

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

<h1 id="rest.RestDataHandler">RestDataHandler</h1>

```python
RestDataHandler(self, *args, **kwargs)
```

Abstract class for working with different data representations such as JSON or XML. Data handler classes for JSON
and XML are already part of this repository. Other data handler may as well be created if required. If application
requires more specific data handling beyond what JSON and XML data handlers provide, they can be extended as well
for use with specific `RestClient` extension.

<h1 id="rest.json_handler.RestJSONHandler">RestJSONHandler</h1>

```python
RestJSONHandler(self, *args, **kwargs)
```

Handle data exchange between REST server and REST client that is represented in JSON format.

<h1 id="rest.xml_handler.RestXMLHandler">RestXMLHandler</h1>

```python
RestXMLHandler(self, *args, **kwargs)
```

Handle data exchange between REST server and REST client that is represented in XML format. `lxml` is required.

`OrderedDict` is used as it allows ordered list of attribute value pairs.

