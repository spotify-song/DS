from os import getenv
from dotenv import load_dotenv
import psycopg2


class UpdateTables():
    def __init__(self):
        load_dotenv()
        # Connecting to DB
        self.conn = psycopg2.connect(user=getenv('DB_USER'),
                                     password=getenv('DB_PASSWORD'),
                                     host=getenv('DB_HOST'),
                                     port=getenv('DB_PORT'),
                                     database=getenv('DB_DATABASE'))

    def update_users_info(self, table_name='users', display_name=None):
        '''
        Method that updates the user information in the following tables:
        - users:
            - display_name (VarChar 255)
        - tokens:
            - access_token (VarChar 255)
            - token_type (VarChar 255)
            - expires_in (int)
            - refresh_token (VarChar 255)
            - scope (VarChar 255)
            - expires_at (int)
            - user (VarChar 255)
            - user_id (from users table)

        Input:
            - table_name: Table name is already a default arg, and does not
                          need to be changed
            - token: Alphanumeric string of characters used to access user
                     information
            - user_id: Alphanumeric string of characters used to identify users
            - display_name: User profile display name

        Output:
            - There is no output necessarily, this function will be used to
              update the user table with the pertinent information
        '''
        display_name = display_name
        
        table_name = table_name
        conn = self.conn
        curs = conn.cursor()

        # Queries to execute
        # checking to see if display_name exists
        check_for_user_query = """
            SELECT display_name
            FROM users
            WHERE display_name = (%s)
            """

        # Insert Queries:
        # display_name -> user table
        user_tbl_insert_query = """
            INSERT INTO users (DISPLAY_NAME)
            VALUES (%s)
            """

        # token -> tokens table
        token_tbl_insert_query = """
            INSERT INTO tokens ()
            """

        # (%s) var
        query_user_var = (display_name,)

        # check for user in db
        curs.execute(check_for_user_query, query_user_var)
        if curs.fetchone() == query_user_var:
            curs.close()
            conn.close()

        else:
            # print(f"{query_user_var} not in db")
            curs.execute(user_tbl_insert_query, query_user_var)
            # curs.execute(check_for_user_query, query_user_var)
            # record = curs.fetchone()
            conn.commit()
            curs.close()
            conn.close()
