# Summery: 
--------------------------------------------------------------------------------------------------------------------------

Sparkify would like to move their process and data onto the cloud. Song details and user activity data's are stored in JSON file. 
To analyze their data, a Relational Database Schema was created, which can be filled with an ETL pipeline.

# Python Scripts:
--------------------------------------------------------------------------------------------------------------------------
To create tables: python3 create_tables.py
To fill table with ETL: python3 ctl.py

# How to run process
--------------------------------------------------------------------------------------------------------------------------
1. Start up a AWS Redshift Cluster
- Make sure to setup the IAM role to AmazonS3ReadOnlyAccess.
- Use dc2.large cluster with 4 nodes. Note that each node a cost of USD 0.25/h (on-demand option) per cluster
2. Open up a terminal session or open run_script.ipynb

3. Run '%run create_tables.py'
- This will create the tables, must be run first
4. Run 'python etl.py'
- This will run the ETL process

# Project Structure
--------------------------------------------------------------------------------------------------------------------------
- create_tables.py - Script will drop old tables (if exist) ad re-create new tables
- etl.py - Script will executes the queries that extract JSON data from the S3 bucket and ingest them to Redshift
- sql_queries.py - File that contains variables with SQL statement in String formats, partitioned by CREATE, DROP, COPY   and INSERT statements
- dhw.cfg - Configuration file used that contains info about Redshift, IAM and S3
