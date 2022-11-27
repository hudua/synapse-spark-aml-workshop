# Load CSV from raw zone
df = spark.read.load('abfss://synapse@adlsgenhuduaname.dfs.core.windows.net/raw/sample_data.csv', format='csv', header=True, inferSchema=True)

# Use SQL to create a db if not already there
%%sql
create database if not exists db

# Save as delta format in the delta / intermediate zone
df.write.format('delta').partitionBy('deviceid').mode("overwrite").save('abfss://synapse@adlsgenhuduaname.dfs.core.windows.net/delta/sample_data4')

# Now create a reference SQL table
%%sql
drop table if exists db.sensordata2;
CREATE TABLE db.sensordata2
USING DELTA
LOCATION 'abfss://synapse@adlsgenhuduaname.dfs.core.windows.net/delta/sample_data4'

# Now you can query this table
%%sql 
select * from wsibdb.sensordata2 where winddirection = 'E'
