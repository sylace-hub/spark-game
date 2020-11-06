
### Spark SQL Analytics

- For this workshop, you can use the provided Bureau of Transporation Dataset

- Reminder : 

By now, you should have Downloade the DataSets from S3 & stored them with a proper schema as Parquet files :

/user/root/data/BOTS/PARQUET

In the provided S3 bucket, you have a data & a ref folder
The ref folder contains reference tables 

- ToolBox : 

    * Joining Dataframes (Dataframe API): 

```
joinDF = DF_ONE.join(DF_TWO, DF_ONE.join_field ==  DF_TWO.join_field)
```

    * Creating Temporary Views : 

```
DF_ONE.createOrReplaceTempView("EMPLOYEES")
DF_TWO.createOrReplaceTempView("DEPT")
```
    * Joining Dataframes (Dataframe API): 

```
joinDF = spark.sql("select * from EMP e, DEPT d where e.emp_dept_id == d.dept_id") \
  .show(truncate=False)
```
