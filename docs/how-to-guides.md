# How-To Guides

## Connect to Microsoft's SQL Server

Microsoft's SQL Server requires a connection string that has the connection
part URL escaped. SimQLe makes this easy, by just setting the `url_escape`
option in your `.connections.yaml` file to true:

```yaml
connections:
  - name: my-sql-server-database
    driver: mssql+pyodbc:///?odbc_connect=
    connection: DRIVER={SQL Server};UID=<username>;PWD=<password>;SERVER=<my-server>
    url_escape: true
```

See [here](https://docs.sqlalchemy.org/en/13/dialects/mssql.html) for more details 