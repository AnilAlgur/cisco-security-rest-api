# rest

- [API](#api)
    - [`RestClient`](#restclient)
    - [`AppClient`](#appclient)
    - [`RestClientError`](#restclienterror)
    - [`RestDataHandler`](#restdatahandler)
    - [`RestXMLHandler`](#restxmlhandler)
    - [`RestJSONHandler`](#restjsonhandler)

This module allows abstraction of REST client and creates foundation for interacting with any application using any 
data representation such as JSON or XML. 


## API

- [`RestClient`](#restclient)
- [`AppClient`](#appclient)
- [`RestClientError`](#restclienterror)
- [`RestDataHandler`](#restdatahandler)
- [`RestXMLHandler`](#restxmlhandler)
- [`RestJSONHandler`](#restjsonhandler)




### `AppClient`

Abstract class for working with different applications. This must be sub-classed to create application specific
client and these variables must be overriden:

`AUTH_URL`: Suffix of URL that must be appended to server FQDN in order to invoke REST API authentication.
    
`LOGOUT_URL`: Suffix of URL that must be appended to server FQDN in order to logout from REST API server.
    
`AUTH_HTTP_STATUS`: HTTP status returned after successful authentication, e.g. it could be 200 or 201
    
`AUTH_REQ_HDR_FIELD`: Header field received in the authentication response that'll provide token or cookie that 
must be used in subsequent requests to the REST server.
    
`AUTH_HDR_FIELD`: Header field to be used in all the requests to the REST server after authentication is completed.




### `RestDataHandler`

Abstract class for working with different data representations such as JSON or XML.


### `RestXMLHandler`

Handle data exchange between REST server and REST client that is represented in XML format. `lxml` is required.

`OrderedDict` is used as it allows ordered list of attribute value pairs.


### `RestJSONHandler`

Handle data exchange between REST server and REST client that is represented in JSON format.
