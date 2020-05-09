# Summary of the Project:
Using AWS S3 and Redshift to make the ETL process from raw log file to the Sparkify app to a database schema that provides analytical data to be queired.

# How to Ran:
1. To run this project you will need to fill the following information, and save it as dwh.cfg in the project root folder.
2. Create a python environment with the dependencies listed on requirements.txt

3. Run the create_cluster script to set up the needed infrastructure for this project.

 python create_cluster.py

4. Run the create_tables script to set up the database staging and analytical tables

 python create_tables.py

5. Finally, run the etl script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables.

 python create_tables.py


# Steps followed on this project
1. Create Table Schemas
- Design schemas for your fact and dimension tables
- Write a SQL CREATE statement for each of these tables in sql_queries.py
- Complete the logic in create_tables.py to connect to the database and create these tables
- Write SQL DROP statements to drop tables in the beginning of - create_tables.py if the tables already exist. This way,  you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
- Launch a redshift cluster and create an IAM role that has read access to S3.
- Add redshift database and IAM role info to dwh.cfg.
- Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
2. Build ETL Pipeline
- Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
- Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
- Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
- Delete your redshift cluster when finished.
3. Document Process Do the following steps in your README.md file.
- Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
- State and justify your database schema design and ETL pipeline.
