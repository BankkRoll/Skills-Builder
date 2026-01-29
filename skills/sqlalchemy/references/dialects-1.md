# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Dialects

The **dialect** is the system SQLAlchemy uses to communicate with various types of [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI) implementations and databases.
The sections that follow contain reference documentation and notes specific to the usage of each backend, as well as notes
for the various DBAPIs.

All dialects require that an appropriate DBAPI driver is installed.

## Included Dialects

- [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [MySQL and MariaDB](https://docs.sqlalchemy.org/en/20/dialects/mysql.html)
- [SQLite](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [Oracle](https://docs.sqlalchemy.org/en/20/dialects/oracle.html)
- [Microsoft SQL Server](https://docs.sqlalchemy.org/en/20/dialects/mssql.html)

### Supported versions for Included Dialects

The following table summarizes the support level for each included dialect.

| Database | Supported version | Best effort |
| --- | --- | --- |
| Microsoft SQL Server | 2012+ | 2005+ |
| MySQL / MariaDB | 5.6+ / 10+ | 5.0.2+ / 5.0.2+ |
| Oracle Database | 11+ | 9+ |
| PostgreSQL | 9.6+ | 9+ |
| SQLite | 3.12+ | 3.7.16+ |

### Support Definitions

>

  Supported version

**Supported version** indicates that most SQLAlchemy features should work
for the mentioned database version. Since not all database versions may be
tested in the ci there may be some not working edge cases.

  Best effort

**Best effort** indicates that SQLAlchemy tries to support basic features on these
versions, but most likely there will be unsupported features or errors in some use cases.
Pull requests with associated issues may be accepted to continue supporting
older versions, which are reviewed on a case-by-case basis.

## External Dialects

Currently maintained external dialect projects for SQLAlchemy include:

| Database | Dialect |
| --- | --- |
| Actian Data Platform, Vector, Actian X, Ingres | sqlalchemy-ingres |
| Amazon Athena | pyathena |
| Amazon Aurora DSQL | aurora-dsql-sqlalchemy |
| Amazon DynamoDB | pydynamodb |
| Amazon Redshift (via psycopg2) | sqlalchemy-redshift |
| Apache Drill | sqlalchemy-drill |
| Apache Druid | pydruid |
| Apache Hive and Presto | PyHive |
| Apache Solr | sqlalchemy-solr |
| Clickhouse | clickhouse-sqlalchemy |
| CockroachDB | sqlalchemy-cockroachdb |
| CrateDB | sqlalchemy-cratedb |
| Databend | databend-sqlalchemy |
| Databricks | databricks |
| Denodo | denodo-sqlalchemy |
| EXASolution | sqlalchemy_exasol |
| Elasticsearch (readonly) | elasticsearch-dbapi |
| Firebird | sqlalchemy-firebird |
| Firebolt | firebolt-sqlalchemy |
| Google BigQuery | sqlalchemy-bigquery |
| Google Sheets | gsheets |
| Greenplum | sqlalchemy-greenplum |
| HyperSQL (hsqldb) | sqlalchemy-hsqldb |
| IBM DB2 and Informix | ibm-db-sa |
| IBM Netezza Performance Server[1] | nzalchemy |
| Impala | impyla |
| Kinetica | sqlalchemy-kinetica |
| Microsoft Access (via pyodbc) | sqlalchemy-access |
| Microsoft SQL Server (via python-tds) | sqlalchemy-pytds |
| Microsoft SQL Server (via turbodbc) | sqlalchemy-turbodbc |
| Mimer SQL | sqlalchemy-mimer |
| MonetDB | sqlalchemy-monetdb |
| MongoDB | pymongosql |
| OceanBase | oceanbase-sqlalchemy |
| OpenGauss | openGauss-sqlalchemy |
| Rockset | rockset-sqlalchemy |
| SAP ASE (fork of former Sybase dialect) | sqlalchemy-sybase |
| SAP HANA | sqlalchemy-hana |
| SAP Sybase SQL Anywhere | sqlalchemy-sqlany |
| Snowflake | snowflake-sqlalchemy |
| Teradata Vantage | teradatasqlalchemy |
| TiDB | sqlalchemy-tidb |
| YDB | ydb-sqlalchemy |
| YugabyteDB | sqlalchemy-yugabytedb |

   [[1](#id2)]

Supports version 1.3.x only at the moment.
