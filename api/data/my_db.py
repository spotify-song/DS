from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
# Connecting to DB
egine = create_engine(getenv('DATABASE_URL'))
SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=engine
                    )


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String, unique=True, nullable=False)

    token = relationship('Tokens', backref='user_token', uselist=False)

    def __repr__(self):
        return "<User(display_name='%s')>" % (self.display_name)


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, nullable=False)
    token_type = Column(String, unique=False, nullable=False)
    expires_in = Column(Integer, unique=False, nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    scope = Column(String, unique=False, nullable=False)
    expires_at = Column(Integer, unique=False, nullable=False)
    user = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Tokens(\
        access_token='%s',\
        token_type='%s',\
        expires_in='%s',\
        refresh_token='%s',\
        scope='%s',\
        expires_at='%s',\
        user='%s',\
        user_id='%s')>" % (
            self.id,
            self.access_token,
            self.token_type,
            self.expires_in,
            self.refresh_token,
            self.scope,
            self.expires_at,
            self.user,
            self.user_id)
