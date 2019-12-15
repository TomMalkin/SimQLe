# Reference

## Structure of the `.connections.yaml` file. 

The structure of the `.connections.yaml` file underpins the ConnectionManager 
class. It defines the connections to one or more databases per connection mode
(production, development or testing).

Each connection has a `name`, `driver` and `connection`. Other options exist as
well, such as `default` and `url_escape`. Example:

```yaml
- name: mysql-database
  driver: mysql+pymysql://
  connection: user:password@mysql:3306/testdatabase
```

The `driver` and the `connection` options are simply the full connection string.
The are split up so the connection section can be url escaped if required.

Place the development connections and testing connections under the headings
`dev-connections` and `test-connections` respectively.

The `default=true` option in a connection means this is used when no
`con_name` is specified in either the `execute_sql` or `recordset` methods are
used.

Here is an example of a connections file that define a "main" connection to a 
Microsoft SQL Server database, with a "cache" connection to a SQLite database, 
with production, development and testing setups:

```yaml
connections:
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-server>
    url_escape: true
    default: true
 
  - name: my-sqlite-database
    driver: sqlite:///
    connection: databases/my-database.db
 
dev-connections:
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-dev-server>
    url_escape: true    
    default: true

  - name: my-sqlite-database
    driver: sqlite:///
    connection: /tmp/my-dev-database.db

test-connections:
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-test-server>
    url_escape: true
    default: true

  - name: my-sqlite-database
    driver: sqlite:///
    connection: /tmp/my-test-database.db
```

## ConnectionManager


### Intialising Options

You create a ConnectionManager instance referencing the connections
to be used in one of three ways:

1 - Reference the connection file relatively or explicitly, for example:

`cm = ConnectionManager(".connections.yaml")`

or

`cm = ConnectionManager("~/connections/.connections.yaml")`

2 - Load from a default location. If no parameter is specified, SimQLe will look
for the file first in the root of the project, and then in the home directory:

`cm = ConnectionManager()`

3 - Load from a dict. If you don't need the benefits of storing the connections
in a file (say you're just using a temporary SQLite database), then you can pass
a dict that mirrors the structure of the yaml file. For example:

```python
connections_dict = {
    "connections": [
        {"name": "my-database",
         "driver": "sqlite:///",
         "connection": "my-database.db"}
    ]
}

cm = ConnectionManager(connections_dict)
```

### Executing SQL

Once the connection manager is initialised with connections, `execute_sql`
is the method that will execute SQL commands on a given connection:

```python
cm = ConnectionManager()

cm.execute_sql(con_name="main", sql=sql, params=params)
```

Where "main" is the name of the desired connection, `sql` has the 
sql statement to execute, and `params` is a dict with the named parameters
(if any). `params` can be ignored if no named parameters exist.

### Returning Data

 
#### Recordset

To return data with multiple records, use the `recordset` method:

```python
cm = ConnectionManager()

result = cm.recordset(con_name="main", sql=sql, params=params)
```

Which has the methods:

```
>>> result.headings
("heading 1", "heading 2")

>>> result.data
[("something 1", 1), ("something 2", 2)

>>> result.as_dict()
[{"heading 1": "something 1", "heading 2": 1},
 {"heading 1": "something 2", "heading 2": 2}]

>>> result.column("heading 1")
["something 1", "something 2"]
```

#### Record

Single records can be conveniently returned with `cm.record`. Extra 
rows are discarded.

```
>>> result = cm.record(con_name="main", sql=sql, params=params)
>>> result.data
("something 1", 1)

>>> result.as_dict
{"heading 1": "something 1", "heading 2": 1},

>>> bool(result)  # if the record exists
True
```

### RecordScalar

Single datapoints can be conveniently returned with `cm.record_scalar`.
Extra rows and columns are discarded.

```
>>> result = cm.record_scalar(con_name="main", sql=sql, params=params)`
>>> result.datum
"something 1"

>>> bool(result)  # the truthiness of the datapoint
True
```
