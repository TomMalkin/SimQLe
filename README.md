
# SimQLe

> The simple way to SQL


[![build status](http://img.shields.io/travis/Harlekuin/SimQLe/master.svg?style=flat)](https://travis-ci.org/Harlekuin/SimQLe)
[![codecov](https://codecov.io/gh/Harlekuin/SimQLe/branch/master/graph/badge.svg)](https://codecov.io/gh/Harlekuin/SimQLe)


Perfect for no fuss SQL in your Python projects. Execute SQL and return simple
Recordsets. Manage several connections, and be certain that your production
databases aren't touched in your Integration Tests. Also, named parameters
across the board.

## Installation

### Repository
https://github.com/Harlekuin/SimQLe

Or choose your poison:

- `$ pip install simqle`
- `$ poetry add simqle`
- `$ pipenv install simqle`

Once installed, requires a .connections.yaml file in the root of the project
that defines the connection strings the project should use. See the Connection
String section for syntax.

## Usage

### In Production

Get a result from the name of your connection, the SQL statement, and a dict
of parameters:

```python
from simqle import recordset, load_connections

load_connections()

sql = "SELECT name, age FROM people WHERE category = :category"
params = {"category": 5}
result = recordset(con_name="my-database", sql=sql, params=params)
```

recordset() returns a tuple of (Data, Headings). "Data" is a list of row tuples.
Headings is a list of field names from the query.


### In Integration Tests

Before running integration tests, set the `SIMQLE_TEST` environment variable
to `True`. This will cause the `load_connections` function to load the
`test-connections` (which should mirror the `connections` in terms of name and
type of database), and will cause the code in your project to run exactly the
same, but instead connect to your defined test connections instead.

### Running the tests

To run the tests, you will need to have the "behave" package installed (TODO : put this in the setup.py). For now, do this by running

    pip install behave

Once installed, navigate to

  tests/integration-tests/behave-tests

Once there, run

  PYTHONPATH=../../.. behave

The python path will need to be set so that behave picks up the projects from the root directory. You can also install the project locally to avoid this.


## The .connections.yaml File
Define the connection strings for production and test servers. The names of the `test-connections` should mirror the `connections` names. The file `.connections.yaml` should be in the root of your project. Each connection will be referred to by its name.

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


test-connections:
    # the names of the test-connections should mirror the connections above.
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    # connecting to a different server here
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-test-server>
    url_escape: true    

  - name: my-sqlite-database
    driver: sqlite:///
    connection: /tmp/my-test-database.db  # note the absolute path syntax
```

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

## Road Map
- all available relational databases tested.
- scripts for easy project setup.
