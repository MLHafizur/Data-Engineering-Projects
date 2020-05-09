import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import TimestampType


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Creates Spark Session
    
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
     """
    Process all songs data from the json files specified from the input_data
    :param spark: SparkSession
    :param input_data: Root-URL to S3 bucket
    :param output_data: Path to the local directory
    :return: None
    
    """
    
    
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/*/*.json")
    
    # read song data file
    df = spark.df(song_data)

    # extract columns to create songs table
    songs_table = df['song_id', 'title', 'artist_id', 'artist_name', 'year', 'duration']
    songs_table = songs_table.drop_duplicates(subset=['song_id'])

    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id').parquet(os.path.join(output_data, 'songs.parquet'), 'overwrite')
    print("(1/2) | songs.parquet completed")

    # extract columns to create artists table
    artists_table = df['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artists_table = artists_table.drop_duplicates(subset=['artist_id'])
    
    # write artists table to parquet files
    artist_table.write.parquet(os.path.join(output_data, 'artists.parquet'), 'overwrite')
    print("(1/2) | artists.parquet completed")

def process_log_data(spark, input_data, output_data):
    """
    Process songs data from S3 to local directory. Creates dimension tables 'users' and 'time', also 
    a fact table 'songplays'
    :param spark: SparkSession
    :param input_data: Root-URL to S3 bucket
    :param output_data: Path to the local directory
    :return: None
    
    """
    # get filepath to log data file
    log_data = os.path.join(input_data, "log_data/*/*.json")

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.where(col("page") == "NextSong")

    # extract columns for users table    
    user_table = df['userId', 'firstName', 'lastName', 'gender', 'level', 'ts']
    user_table = user_table.orderBy("ts", ascending = False).dropDuplicates(subset=['userId']).drop('ts')
    
    # write users table to parquet files
    user_table.write.parquet(os.path(output_data, 'users.parquet'), 'overwrite')

    # create timestamp column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(int(int(x)/1000)), TimestampType())
    get_weekday = udf(lambda x: x.weekday())
    get_week = udf(lambda x: datetime.isocalendar(x)[1])
    get_hour = udf(lambda x: x.hour)
    get_day = udf(lambda x : x.day)
    get_year = udf(lambda x: x.year)
    get_month = udf(lambda x: x.month)
    
   
    df = df.withColumn('start_time', get_datetime(df.ts))
    df = df.withColumn('hour', get_hour(df.start_time))
    df = df.withColumn('day', get_day(df.start_time))
    df = df.withColumn('week', get_week(df.start_time))
    df = df.withColumn('month', get_month(df.start_time))
    df = df.withColumn('year', get_year(df.start_time))
    df = df.withColumn('weekday', get_weekday(df.start_time))
    time_table  = df['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_table = time_table.drop_duplicates(subset=['start_time'])
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'time.parquet'), 'overwrite')
    print("(2/3) | time.parquet completed ") 
    
 

    # read in song data to use for songplays table
    song_df = spark.read.parquet("results/songs.parquet")


    # extract columns from joined song and log datasets to create songplays table 
    df = df.join(song_df, (song_df.title == df.song) & (song_df.artist_name == df.artist))
    df = df.withColumn('songplay_id', monotonically_increasing_id()) 
    songplays_table = df['songplay_id', 'start_time', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(os.path.join(output_data, 'songplays.parquet'), 'overwrite')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
