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

    def update_user(self, table_name='users', token, user_id, display_name):
        '''
        Method that updates the user table one user at a time.

        Input:
            - table_name: Table name is already in the arg, and does not need
              to be changed
            - token: Alphanumeric string of characters used to access user
              information
            - user_id: Alphanumeric string of characters used to identify users
            - display_name: User profile display name

        Output:
            - There is no output necessarily, this function will be used to
              update the user table with the pertinent information
        '''
        # psudo code: connect to db, check if user exists, if not the add user
        conn = self.conn
        table_name = table_name
