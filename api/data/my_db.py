from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
# Connecting to DB
db_url = getenv('DATABASE_URL')
egine = create_engine(db_url)
SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=engine
                    )
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String, unique=True, )


class UpdateTables():
    def update_users_info(
            self,
            display_name=None,
            token_info=None,
            id=None
            ):
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
