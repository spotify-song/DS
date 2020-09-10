from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Checking connection to DB
try:
    # connecting to DB
    conn = psycopg2.connect(user=getenv('DB_USER'),
                            password=getenv('DB_PASSWORD'),
                            host=getenv('DB_HOST'),
                            port=getenv('DB_PORT'),
                            database=getenv('DB_DATABASE'))

    curs = conn.cursor()
    # print PostgresQL Connection properties
    print(conn.get_dsn_parameters(), "\n")

    # print PostgresQL version
    curs.execute("SELECT version();")
    record = curs.fetchone()
    print('You are connected to - ', record, '\n')

except (Exception, psycopg2.Error) as error:
    print('Error while connectin got PostgresQL', error)

finally:
    # closing database Connection
    if (conn):
        curs.close()
        conn.close()
        print('PostgresQL connection is closed')
