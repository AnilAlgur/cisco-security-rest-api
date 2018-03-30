<h1 id="fmc">fmc</h1>


Firepower Management Center API
===============================

Python module for interacting with Cisco Firepower Management Center (FMC). This module is based on FMC 6.1 REST API
specification.

Please check the examples in the repository for guidance on how to use this module.

<h1 id="fmc.api.FMC">FMC</h1>

```python
FMC(self, url=None, username=None, password=None)
```

This class must be used to interact with FMC. Other classes are available within same module to interact with FMC
resources such as Policy Objects, Devices, Access Policies.

__Parameters__

- __url__: URL of the FMC server
- __username__: Login username for FMC server. Ensure that appropriate user role and permissions are assigned
to perform all the intended tasks.
- __password__: Login password for FMC server.


<h1 id="fmc.api.FPObject">FPObject</h1>

```python
FPObject(self, fmc, type=None, oid=None, name=None, url=None, json=None, data=None, obj=None)
```

FMC Object Manager API

Extends generic `FPResource` for Policy Object related methods. This class allows for extensive and flexible ways to
perform CRUD operations on the policy objects and object inheritance as well.

__Parameters__

- __fmc__: FMC server object `FMC` object.
- __type__: (optional) Object type supported by Cisco FMC 6.1.0.
- __oid__: (optional) Object ID, GET the object, if provided.
- __name__: (optional) Object Name, GET the object, if provided.
- __url__: (optional) URL for the object, GET the object if provided.
- __json__: (optional) Full object definition in `dict` format.
- __data__: (optional) Data that will be accpeted by Cisco FMC to create object when POST method is used.
- __obj__: (optional) Another `FPObject` to duplicate. This is useful when migrating objects between different FMC
servers.

<h1 id="fmc.api.FPObject.update">update</h1>

```python
FPObject.update(self, data)
```

Update this object with new definition.

__Parameters__

- __data__: JSON data in dict() format for the new definition

- __:return__: JSON data of the object

<h1 id="fmc.api.FPObject.rename">rename</h1>

```python
FPObject.rename(self, new_name)
```

Rename this object.

__Parameters__

- __new_name__: New object name

<h1 id="fmc.api.FPObject.delete">delete</h1>

```python
FPObject.delete(self)
```

Delete this object from FMC server.

<h1 id="fmc.api.FPObject.parent_type">parent_type</h1>


Returns group object type if this object can be grouped under
other object.

<h1 id="fmc.api.FPObject.add_to_parent">add_to_parent</h1>

```python
FPObject.add_to_parent(self, pname)
```

Add this object inside another object as a child.

__Parameters__

- __pname__: Name of the parent object

<h1 id="fmc.api.FPObject.remove_from_parent">remove_from_parent</h1>

```python
FPObject.remove_from_parent(self, pname)
```

Remove this object from another parent object

__Parameters__

- __pname__: Name of the parent object

<h1 id="fmc.api.FPObject.add_children">add_children</h1>

```python
FPObject.add_children(self, *children_names)
```

Add any number of objects to this object as a parent.

__Parameters__

- __children_names__: Comma separated names of child objects

<h1 id="fmc.api.FPObject.remove_child">remove_child</h1>

```python
FPObject.remove_child(self, child_name)
```

Remove an existing child from this object as a parent.

__Parameters__

- __child_name__: Name of the child to remove

<h1 id="fmc.api.FPObjectTable">FPObjectTable</h1>

```python
FPObjectTable(self, fmc, type)
```

Extends `FPResourceTable` for Policy Object related functionality. `FPObjectTable` allows `FMC` class to stay in
sync with policy objects available in FMC. This helps with input data validation before it is sent to FMC server.
FMC has its own input data validation mechanisms but customers prefer to send only necessary REST API requests to
FMC and encounter as few errors as possible.

In case of policy objects that allow for nested inheritance, such as network objects, table is built in child first
order. This is achieved by using `OrderedDict` in `FPResourceTable`. This is very useful in data migration and
cleanup especially between multiple FMCs and while executing test cases.

Example usage:

```python
>>> host_objs = FPObjectTable(FMC_object, 'hosts')
>>> hosts_objs.type
hosts
>>> hosts_objs.names
{}
>>> hosts_objs.build()
>>> hosts_objs.names
{'host1_name': 'host1_id', 'host2_name': 'host2_id', ...}
```

<h2 id="fmc.api.FPObjectTable.build">build</h2>

```python
FPObjectTable.build(self)
```

Build the 'names' dictionary for this table.
names = {
    'object1_name': 'object1_id',
    'object2_name': 'object2_id'
    }

<h1 id="fmc.api.FPObjectTable.__iter__">__iter__</h1>

```python
FPObjectTable.__iter__(self)
```

Generator function for FPObjectTable. It yields FPObject for
for each item inside it.

```python
>>> for fp_object in fmc.FPObjectTable(FMC_object, 'hosts'):
        print("fp_object.type, fp_object.name, fp_object.id")

hosts hosts1_name hosts1_id
hosts hosts2_name hosts2_id
```

<h1 id="fmc.api.FMCClient">FMCClient</h1>

```python
FMCClient(self, *args, **kwargs)
```

AppClient extension for FMC.

<h1 id="fmc.api.FMCRestClient">FMCRestClient</h1>

```python
FMCRestClient(self, url=None, username=None, password=None)
```

RestClient extension for FMC with FMCClient adn RestJSONHandler.

Method Resolution Order:
```
FMCRestClient
RestClient
FMCClient
AppClient
RestJSONHandler
RestDataHandler
object
```

