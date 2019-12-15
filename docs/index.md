# SimQLe Documentation

Version 0.5.3

> Never test or develop on production databases
 
 -- someone clever probably 
 
While there are differing [opinions](https://opensource.com/article/19/5/dont-test-production),
it makes sense to develop on database connections that won't ruin your production environment.


### Introduction

**SimQLe** is a library for easy and convenient SQL integration.
It can execute SQL queries and use the returning data. It has convenient return 
types and methods, and also makes named parameters easy (even in pandas).

It was created to fill the need of both easy SQL integration with multiple
databases simultaneously, but also easy integration tests and development 
environments _without_ editing the actual code of the project. Simply changing
the SIMQLE_MODE environment variable, you can use dev or test database 
connections.
 
By using a "Connection Manager" to define multiple database connections allows you to:

 - Keep connection authentication out of repositories (by keeping them in a 
 .connections.yaml file)
 - Define production, development and testing environments
 - Easily Organise all database connections required in the project 
 

SimQLe is built on top of the fantastic [SQLAlchemy](https://www.sqlalchemy.org/)
library. 

### When _shouldn't_ I use SimQLe?

SimQLe removes and doesn't expose a lot of the overhead code when truly advanced
setups are required - You can't mess around with complicated connection pools
and advanced datatypes etc. You could probably hack SimQLe to allow that to
happen though (PRs are welcome of course).

SimQLe makes assumptions about how you should develop and manage your 
connections, so don't use it if you like to do it another way.


### Repository

https://github.com/Harlekuin/SimQLe

### Quick Start

An example project.

Create a `.connections.yaml` file in the root of the project:

```yaml
# .connections.yaml

connections:
  - name: main-database
    driver: sqlite:///
    connection: databases/main-database.db
    default: true

  - name: other-database
    driver: sqlite:///
    connection: databases/other-database.db

dev-connections:
  - name: main-database
    driver: sqlite:///
    connection: databases/main-dev-database.db
    default: true

  - name: other-database
    driver: sqlite:///
    connection: databases/other-dev-database.db
```

Here we've defined 2 sqlite connections we can use in the project, 
the default "main-database" and another "other-database". We can now
reference these by name in the project.

You can query these databases by after loading them into a 
`ConnectionManager` instance:

```python
# myprogram.py

from simqle import ConnectionManager

cm = ConnectionManager(".connections.yaml")

sql = """
    SELECT name, age
    FROM Person
    Where Position = :position
    """
params = {"position": "Science Officer"}

result = cm.recordset(con_name="main-database", sql=sql, params=params)
```

The `result` variable from above now is an instance of `Recordset` with:

```python
>>> result.headings
("name", "age")

>>> result.data
[("Spock", 35), ("Jadzia Dax", 33)]
```

Now just change the con_name to reference "other-database" to query that one, 
or change the `SIMQLE_MODE` environment variable to "development" to use the 
connections under `dev-connections`.

### [Tutorials](/tutorials)
### [How-To Guides](/how-to-guides)
### [Explanation](/explanation)
### [Reference](/references)


