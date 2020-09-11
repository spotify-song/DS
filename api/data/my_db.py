from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# connecting to DB
conn = psycopg2.connect(user=getenv('DB_USER'),
                        password=getenv('DB_PASSWORD'),
                        host=getenv('DB_HOST'),
                        port=getenv('DB_PORT'),
                        database=getenv('DB_DATABASE'))

curs = conn.cursor()
# print PostgresQL Connection properties
print(conn.get_dsn_parameters(), "\n")
curs.execute("SELECT version();")
record = curs.fetchone()

curs.close()
conn.close()
