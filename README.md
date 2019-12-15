
# SimQLe

> The simple way to SQL


[![build status](http://img.shields.io/travis/Harlekuin/SimQLe/master.svg?style=flat)](https://travis-ci.org/Harlekuin/SimQLe)
[![codecov](https://codecov.io/gh/Harlekuin/SimQLe/branch/master/graph/badge.svg)](https://codecov.io/gh/Harlekuin/SimQLe)


Perfect for no fuss SQL in your Python projects. Execute SQL and return simple
record sets with named parameters. Manage several connections, and switch 
between production, development and testing modes.

Documentation can be found [here](https://simqle.readthedocs.io/en/latest/)

## Installation

### Repository
https://github.com/Harlekuin/SimQLe

Or choose your poison:

- `$ pip install simqle`
- `$ poetry add simqle`
- `$ pipenv install simqle`

SimQLe reads from a connections file in yaml format. See the 
`.connections.yaml` file section for more details.

## Usage

### In Production

Get a result from the name of your connection, the SQL statement, and a dict
of parameters:

```python
from simqle import ConnectionManager

# Intialise your connections
cm = ConnectionManager(".connections.yaml")

# Write some simple SQL
sql = "SELECT name, age FROM people WHERE category = :category"
params = {"category": 5}
result = cm.recordset(con_name="my-database", sql=sql, params=params)

# result.headings == ["name", "age"]

# result.data == [
#    ("Jim", 30),
#    ("Bones", 35)
# ]

# result.as_dict == [
#    {"name": "Jim", "age": 30},
#    {"name": "Bones", "age": 35}
# ]

# result.column["name"] == ["Jim", "Bones"]
```

The `recordset()` method returns a RecordSet object with a bunch of handy methods for getting at the data.
There is also a `cm.record()` method for queries you know only return a single record, and
a `cm.record_scalar()` method for queries where you're after a single datum. 

### In Development

Set the SIMQLE_MODE environment variable to "development". This will use your
development connections in place of the production ones, without changing
your code.


### In Integration Tests

Set the SIMQLE_MODE environment variable to "testing".

## Testing this package

Tests require the behave package:

`> pip install behave`

To run, simply:

`> behave`


## The .connections.yaml File
Define the connection strings for production, development and test servers. The
names of the `test-connections` and `dev-connections` should mirror the 
`connections` names. Each connection is be referred to by its name.

Example file:

```yaml
connections:
 
    # The name of the connection - this is what will be used in your project
    # to reference this connection.
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-server>
 
    # some odbc connections require urls to be escaped, this is managed by
    # setting url_escaped = true:
    url_escape: true

    # File based databases like sqlite are slightly different - the driver
    # is very simple.
  - name: my-sqlite-database
    driver: sqlite:///
    # put a leading '/' before the connection for an absolute path, or omit
    # if it's relative to the project path
    connection: databases/my-database.db
    #  This connection will be used if no name is given if the default 
    # parameter is used:
    default: true


dev-connections:
    # the names of the dev-connections should mirror the connections above.
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    # connecting to a different server here
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-dev-server>
    url_escape: true    

  - name: my-sqlite-database
    driver: sqlite:///
    connection: /tmp/my-dev-database.db
    default: true


test-connections:
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-test-server>
    url_escape: true    

  - name: my-sqlite-database
    driver: sqlite:///
    connection: /tmp/my-test-database.db
    default: true
```

## Convenience functions

`bind_sql(sql, params)` can be used to bind named parameters (from a dictionary) to a SQL query, even if the library that executes
the query doesn't support named parameters. For example:

```python
import pandas as pd
from simqle import ConnectionManager, bind_sql

cm = ConnectionManager()

sql = "SELECT Age FROM Person WHERE Name = :name"
params = {"name": "Hikaru Sulu"}

bound_sql = bind_sql(sql, params)

# Note we don't need to pass the params here, they have already been bound:
df = pd.read_sql(con=cm.get_engine(), sql=bound_sql)
```

## Metrics

Useful metrics like the execution time and actual SQL sent are logged to the logging namespace "simqle".

## Chat

Say hello in the Gary: https://gitter.im/SimQLe/community


## Author

[Tom Malkin](https://github.com/Harlekuin)

## Contributors

[Zack Botkin](https://github.com/ZackBotkin)

## Release History

- 0.1.0
	- Add the basic skeleton of the project
- 0.1.1
  - Unit tests
  - Integration tests for sqlite added.
  - 100% coverage
- 0.2.0
  - Added url_escape option in connections.yaml file
  - Integration tests added for mysql and postgresql
- 0.3.0
  - Project refactored into classes
  - Default parameter added
- 0.4.0
  - Development added as a connection mode
- 0.5.0
  - RecordSet, Record and RecordScalar objects added
- 0.5.3
  - bind_sql is exposed for convenience
