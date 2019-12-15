# Explanation

## The Basics

SimQLe is used to execute SQL and return data from [relational databases](https://en.wikipedia.org/wiki/Relational_database),
for example [SQLite](https://www.sqlite.org/index.html), [MySQL](https://www.mysql.com/), 
[PostgreSQL](https://www.postgresql.org/) and [SQL Server](https://www.microsoft.com/en-au/sql-server/).

SimQLe is designed to use multiple connections simultaneously, as a lot of projects
use more than one database. For example a MySQL backend with a SQLite cache on a webserver.

Each database application has it's own SQL syntax. The one thing they have in common
is you can execute SQL commands on them to execute actions or return data. SimQLe uses
this genericness to make sure it works on all databases. By remaining database
agnostic, and just sending the user-define SQL statements, all current and future
relational databases (that use this generic approach) can be used.

SimQLe uses database connections defined in a yaml file called 
`.connections.yaml` that is at the root of the project, in your home folder, or
even loaded as a `dict` if you don't want to have a file.

## The Rational

SimQLe was designed to make it easy to:

 - Integrate with many databases simultaneously
 - Make it easy to write code that can be used in integration tests
 - Have dead simple and familiar return types.
 - Allow for named parameters in all database connections

## Why not just use environment variables with other libraries?

Environment variables are the obvious and useful way to define database connections
with other python SQL libraries. However, housing them in a `.connections.yaml`
has a few advantages over that:

1) Managing Environment Variables for multiple database connections are a mess
and have no standard naming convention. `DB_CONN_1`, `DB_CONN_2` etc?
2) This is exacerbated by mirrored dev and test connections.
3) It makes the project easier to share. Imagine if you could share some code,
and just say "This code requires a MySQL connection called 'main',
and a SQLite connection called 'cache'". You then spin up a MySQL container and
choose the location of your sqlite database and boom, you know this code will work
on your sharee's computer.
4) You could even share with a `.connections.yaml.template` file
5) Less thought goes into the naming of variables to remember which database is
which.
6) Each database uses the same SimQLe methods and functions.
7) Changing just one environment variable (`SIMQLE_MODE`) is quicker.
8) Keeping a `.connections.yaml` file in your home directory allows for rapid 
python scripting on any system without having to worry about getting the 
connection string correct each time. It also means you can change the location
of a system database that all your scripts point to in one quick change.
9) Easier to read when coming across a new project. 
  

## Testing applications with database connections

This seems to be an age-old quandary and the source of quite a few articles online.
In my view, when running code for integration testing or even in development
environments when seeing if the code runs as expected while actually creating it,
I don't think the code itself should be changed in any way in order to be tested.

Even having code that is designed in a way to be easy to have changing database
connections (depending on the environment) sounds like a poor design choice.
Instead, code should be written 100% for production, and then the libraries themselves
should be able to switch which databases the code is connected to.

The environment variable `SIMQLE_MODE` has three options (Similar to [Flask](https://www.palletsprojects.com/p/flask/)):
 - `production`
 - `development`
 - `testing`
 
 ### Why are development _and_ testing modes required?
 
 Development mode my connect to an existing development database filled with example
 data. An example would be a boss walking past your desk and asking "Show me what 
 this can do.". Spin up the project, connect to the example development database,
 and show off what an example process would look like.
 
 Testing mode should ideally use a brand new database spun up from scratch. Tests
 should start from a blank slate and shouldn't worry about any existing data. 
 
 ## The `ConnectionManager` class
 
 This is the class that should be defined and intialised once per project, pointing
 to a `.connections.yaml` file.
 
 `cm = ConnectionManager(".connections.yaml")`
 
 `cm` can now be used, either by `cm.recordset()`, or `cm.execute_sql()`

## The Recordset class

Data is returned into a class called RecordSet. This has the 2 main attributes
of `Recordset.headings` giving a tuple of the headings returned by the query, 
and `Recordset.data` giving a list of tuples of the returned data. Several other
methods exist for convenience, such as `Recordset.column[]` which will return a 
list of data in the particular column. `Recordset.as_dict()` returns a list
of dicts of the data.

## Executing SQL vs getting data from the database.

These are actually the same thing, except executing SQL statements doesn't expect
any returning data.
 
 
## Recordset vs Record and RecordScalar

`ConnectionManager.recordset()` can be the only method you use, however 2 others
exist for convenience and efficiency, `record` and `record_scalar`.

Simply put, `ConnectionManager.record()` assumes a single record is returned,
and any others are discarded. A classic example is selecting a row where the 
unique primary key equals a certain value.

Likewise `ConnectionManager.record_scalar` assumes only a single data point is 
being returned. This datapoint is access through the `.datum` attribute, for
example:

```python
from simqle import ConnectionManager

cm = ConnectionManager()

sql = "select age from Person where PersonID = :person_id"
params = {"person_id": 5}

my_scalar = cm.record_scalar(sql=sql, params=params)

datapoint = my_scalar.datum
```
Giving:
```python
>>> datapoint
35

>>> type(my_scalar)
<type RecordScalar>

>>> bool(my_scalar)
True
```

The truthiness  of the RecordScalar class is the same as the truthiness of
the datum. Note, there is a big different between a RecordScalar returning a value, 
returning None, or not returning a row (perhaps 0 records exist?). If 0 records
exist, then SimQLe will throw a `NoScalarDataError`. This should be caught in a
`try: except:` pattern, for example:

```python
try:
    my_scalar = cm.record_scalar(sql=sql, params=params)
    if my_scalar:
        print(datapoint equates to true)
    else:
        print(datapoint equates to false, like '', 0 or NULL)

except NoScalarDataError:
    print(no data was returned)
```



