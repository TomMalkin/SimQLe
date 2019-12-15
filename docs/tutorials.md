# Tutorials

Long term variable storage is a requirement of many programs. Storing these
variables between running programs is the wheelhouse of relational databases.
The data can be written to and queried from these databases using ["Structured 
Query Language"](https://en.wikipedia.org/wiki/SQL) or "SQL".

Note - if you are unfamiliar with SQL, I highly recommend SQLite as a starting
point. Do not be fooled by the name, it is a fully featured SQL environment. It
is one of the most incredible open source victories of all time.

Many python libraries exist that allow you to connect to these databases,
however SimQLe fills a niche:

It makes it easy to:

 - Maintain multiple connections simultaneously
 - Switch development and testing modes with production
 - Share projects with complicated database connection setups
 - Use the familiar python data types of list, dict and tuples
 - Write and migrate many scripts at once by looking at a single file
 
A database can be connected to through a "connection string" which varies from 
database to database. SimQLe uses a file called `.connections.yaml` to define
these connection strings and give them names that can be referenced in your 
code.

The most basic .connections.yaml file you can have is something like:

```yaml
connections:
  - name: my-database
    driver: sqlite:///
    connection: my-database.db
```

This has 1 connection, called "my-database", which is a SQLite database
found at the file called `my-database.db` in the root of the projects.

To initialise the ConnectionManager instance, supply it with the location
of the connections file

```python
from simqle import ConnectionManager
cm = ConnectionManager(".connections.yaml")
```

Now lets create a table on our database (using SQLite [syntax](https://www.sqlite.org/lang_createtable.html))

```python
sql = """
    CREATE TABLE MyTable (
        ID integer PRIMARY KEY,
        name text,
        age integer
    )
    """
cm.execute_sql(con_name="my-database", sql=sql)
```

Now we can add some data to it

```python
sql = """
    INSERT INTO MyTable (name, age)
    VALUES (:name, :age) 
    """

# insert person 1
params = {"name": "Alice", "age": 30}
cm.execute_sql(con_name="my-database", sql=sql, params=params)

# insert person 2
params = {"name": "Bob", "age": 40}
cm.execute_sql(con_name="my-database", sql=sql, params=params)
```

And now we can query it

```python
sql = """
    SELECT * FROM MyTable
"""
result = cm.recordset(con_name="my-database", sql=sql)
```

And now we can explore our result

```
>>> result.heading
('name', 'age')

>>> result.data
[('Alice', 30), ('Bob', 40')]

>>> result.as_dict()
[{'name': 'Alice', 'age': 30},
 {'name': 'Bob', 'age': 40}]

>>> result.column('name')
['Alice', 'Bob']
```


