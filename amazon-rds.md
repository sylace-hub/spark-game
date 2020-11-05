Amazon RDS :
-------------

Create database instance with AWS Cli :

```console
aws rds create-db-instance \
    --db-instance-identifier rds-postgres-03 \
    --engine postgres \
    --db-instance-class db.t2.micro \
    --master-username postgres \
    --master-user-password password2020 \
    --allocated-storage 20 \
    --db-subnet-group-name rds-db-subnet-group \
    --vpc-security-group-ids sg-015f242538ba9960c \
    --publicly-accessible \
    --port 5432 \
    --db-name sample
```

Check the instances and get the host to get connected to :

```console
aws rds describe-db-instances --db-instance-identifier rds-postgres-03 | grep "Address"
                "Address": "rds-postgres-03.cmiwkjhmp07r.us-east-2.rds.amazonaws.com",
```

Try to connect :

```console
psql -U postgres -h rds-postgres-01.cjubztzqczst.eu-west-3.rds.amazonaws.com -p 5432 sample
```

+ Populate the database :

```sql
CREATE TABLE IF NOT EXISTS cafe (
  id SERIAL PRIMARY KEY,        -- AUTO_INCREMENT integer, as primary key
  category VARCHAR(20) NOT NULL,   -- Use the enum type defined earlier
  name VARCHAR(50) NOT NULL,    -- Variable-length string of up to 50 characters
  price NUMERIC(5,2) NOT NULL,  -- 5 digits total, with 2 decimal places
  last_update DATE              -- 'YYYY-MM-DD'
);

INSERT INTO cafe (category, name, price) VALUES
  ('coffee', 'Espresso', 3.19),
  ('coffee', 'Cappuccino', 3.29),
  ('coffee', 'Caffe Latte', 3.39),
  ('coffee', 'Caffe Mocha', 3.49),
  ('coffee', 'Brewed Coffee', 3.59),
  ('tea', 'Green Tea', 2.99),
  ('tea', 'Wulong Tea', 2.89);
```

To list  the tables in the current database :
```sql
\dt
```

To access database from Spark :

```console
> sudo yum install postgresql-jdbc
> sudo spark-shell --driver-class-path /usr/share/java/postgresql-jdbc.jar --jars /usr/share/java/postgresql-jdbc.jar
```

```scala
val database = "sample"
val url = "jdbc:postgresql://rds-postgres-01.cjubztzqczst.eu-west-3.rds.amazonaws.com:5432/" + database

import java.util.Properties
val connectionProperties = new Properties()
connectionProperties.setProperty("user", "postgres")
connectionProperties.setProperty("password", "password2020")

val query ="(select * from cafe) as cafe"

val cafeDf = spark.read.jdbc(url, query, connectionProperties)
cafeDf.show()
```
