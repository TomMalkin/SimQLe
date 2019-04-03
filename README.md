
# SimQLe

> The simple way to SQL in Python


[![build status](http://img.shields.io/travis/Harlekuin/SimQLe/master.svg?style=flat)](https://travis-ci.org/Harlekuin/SimQLe)
[![codecov](https://codecov.io/gh/Harlekuin/SimQLe/branch/master/graph/badge.svg)](https://codecov.io/gh/Harlekuin/SimQLe)

Execute SQL and return useful record sets without the fuss of connection management.

## Installation

### Repository
https://github.com/Harlekuin/SimQLe

Or choose your poison:

`$ pip install simqle`
`$ poetry add simqle`
`$ pipenv install simqle`

Once installed, requires a .connections.yaml file in the root of the project that defines the connection strings the project should use. See the Connection String section for syntax.

## Usage

### In Production
```python
from simqle import rst, load_connections

load_connections()

sql = "SELECT name, age from people where category = :category"
params = {"category": 5}
result = rst("my-database", sql, params)
```

### In Tests

To Do.


## The .connections.yaml File
Define the connection strings for production and test servers. The names of the `test-connections` should mirror the `connections` names. The file `.connections.yaml` should be in the root of your project. Each connection will be referred to by its name.

Example file:

```
connections:
  - name: my-database-1
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-server>

  - name: my-database-2
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};Trusted_Connection=Yes;SERVER=<my-server2>;Persist Security Info=true

test-connections:
  - name: my-database-1
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-test-server>

  - name: my-database-2
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};Trusted_Connection=Yes;SERVER=<my-test-server2>;Persist Security Info=true
```

## Author

Tom Malkin - tommalkin28@gmail.com


## Release History

- 0.1.0
	- Add the basic skeleton of the project

## Road Map
- simqle - perfect for writing integration tests.
- all known databases tested.
- test coverage and CI.
- scripts for easy project setup.
- pypi upload.
