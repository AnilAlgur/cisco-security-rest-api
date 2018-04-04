<h1 id="fxos">fxos</h1>


Firepower eXtensible Operating System (FXOS)
============================================

Python module for interacting with Cisco FXOS REST API.

Please check the examples in the repository for guidance on how to use this module.

<h1 id="fxos.api.FXOS">FXOS</h1>

```python
FXOS(self, url=None, username=None, password=None)
```

This class must be used to interact with FXOS management REST API.

__Parameters__

- __url__: URL of the FMC server
- __username__: Login username for FXOS chassis. Ensure that appropriate user role and permissions are assigned
to perform all the intended tasks.
- __password__: Login password for FXOS chassis.


<h1 id="fxos.api.FXOS.get_version">get_version</h1>

```python
FXOS.get_version(self)
```

GET FXOS software version.

<h1 id="fxos.api.FXOSClient">FXOSClient</h1>

```python
FXOSClient(self, *args, **kwargs)
```

AppClient extension for FXOS REST API.

<h1 id="fxos.api.FXOSRestClient">FXOSRestClient</h1>

```python
FXOSRestClient(self, url=None, username=None, password=None)
```

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

