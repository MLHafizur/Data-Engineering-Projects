# Data Lake ETL Process

# Summery:
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project we will build an ETL pipeline that extracts their data from the data lake hosted on S3, processes them using Spark which will be deployed on an EMR cluster using AWS, and load the data back into S3 as a set of dimensional tables in parquet format.

# How to Run:
To run this project in local mode, create a file dl.cfg in the root of this project with the following data:

KEY=YOUR_AWS_ACCESS_KEY
SECRET=YOUR_AWS_SECRET_KEY
Create an S3 Bucket named sparkify-dend where output results will be stored.

Finally, run the following command:

python etl.py

# ETL pipeline:

1. Load credentials

2. Read data from S3

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data
The script reads song_data and load_data from S3.

3. Process data using spark

Transforms them to create five different tables listed under Dimension Tables and Fact Table. Each table includes the right columns and data types. Duplicates are addressed where appropriate.

Load it back to S3

Writes them to partitioned parquet files in table directories on S3.

Each of the five tables are written to parquet files in a separate analytics directory on S3. Each table has its own folder within the directory. Songs table files are partitioned by year and then artist. Time table files are partitioned by year and month. Songplays table files are partitioned by year and month.

