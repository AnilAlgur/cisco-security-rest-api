<h1 id="asa">asa</h1>


Cisco Adaptive Security Appliance (ASA)
============================================

Python module for interacting with Cisco ASA REST API.

Please check the examples in the repository for guidance on how to use this module.

<h1 id="asa.api.ASA">ASA</h1>

```python
ASA(self, url=None, username=None, password=None)
```

This class must be used to interact with ASA management REST API.

__Parameters__

- __url__: URL of the ASA REST API
- __username__: Login username for ASA REST API. Ensure that appropriate user role and permissions are assigned to perform
 all the intended tasks.
- __password__: Login password for ASA REST API.


<h1 id="asa.api.ASA.get_version">get_version</h1>

```python
ASA.get_version(self)
```

GET ASA software version.

<h1 id="asa.api.ASA.get_cli">get_cli</h1>

```python
ASA.get_cli(self, cmds)
```

GET CLI commands output.

__Parameters__

- __cmd__: List of commands to be sent to ASA

<h1 id="asa.api.ASAClient">ASAClient</h1>

```python
ASAClient(self, *args, **kwargs)
```

AppClient extension for ASA REST API.

Workaround for CSCvh72007: Username and privilege display are incorrect when X-Auth-Token is used for REST API

- Added extra Basic HTTP authentication header to be used in all requests.

- Username:Password credentials need to be static.

<h1 id="asa.api.ASARestClient">ASARestClient</h1>

```python
ASARestClient(self, url=None, username=None, password=None)
```

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

