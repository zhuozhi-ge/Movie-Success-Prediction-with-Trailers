#script to store data in df_final.csv on postgresSQL
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

# Define a database name (we're using a dataset on births, so we'll call it birth_db)
# Set your postgres username/password, and connection specifics
user = 'YOUR_USERNAME' #input your actual user name
password = 'YOUR_PASSWORD'     # input your actual password
host     = 'localhost'
port     = '5432'            # default port that postgres listens on
dbname  = 'movie_db'

## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname) )
print(engine.url)

## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

## insert data into database from Python (proof of concept - this won't be useful for big data, of course)

df_final = pd.read_csv('data/df_final.csv')
df_final.to_sql('movies_data_table', engine, if_exists='replace')


# Connect to make queries using psycopg2
con = None
con = psycopg2.connect(database = dbname, user = user, password=password, host=host)


#uncomment the following to test an example query:


#sql_query = """
#SELECT * FROM movies_data_table WHERE budget>1000000;
#"""
#movie_data_from_sql = pd.read_sql_query(sql_query,con)
#movie_data_from_sql.shape