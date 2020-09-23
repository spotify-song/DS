from os import getenv
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

load_dotenv()
# Connecting to DB
engine = create_engine(getenv('DATABASE_URL'))
SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=engine
                    )


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, index=True)
    display_name = Column(String, unique=True, nullable=False)

    # Backref allows you to update values in a different table
    # set the table name then the back arg will be used as the psudo
    # column that will fill the foreign key in the corresponding table
    # in the case of the value below, the 'token' value will be used to
    # fill the 'user_id' column in the 'Tokens' table
    # Ex: Tokens(all_token_column_names=all_token_values,
    #            user_token=User(object))
    token = relationship('Tokens', backref='user_token')
    user_playlist = relationship('UserPlaylist', backref='user_id')

    def __repr__(self):
        return "<User(display_name='%s')>" % (self.display_name)


class Tokens(Base):
    __tablename__ = 'track_token'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, nullable=False)
    token_type = Column(String, unique=False, nullable=False)
    expires_in = Column(Integer, unique=False, nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    scope = Column(String, unique=False, nullable=False)
    expires_at = Column(Integer, unique=False, nullable=False)
    user = Column(String, ForeignKey('user.id'))

    def __repr__(self):
        return "<Tokens(\
                        access_token='%s',\
                        token_type='%s',\
                        expires_in='%s',\
                        refresh_token='%s',\
                        scope='%s',\
                        expires_at='%s',\
                        user='%s')>" % (
                                        self.access_token,
                                        self.token_type,
                                        self.expires_in,
                                        self.refresh_token,
                                        self.scope,
                                        self.expires_at,
                                        self.user
                                        )


class Tracks(Base):
    __tablename__ = 'tracks'

    id = Column(String, primary_key=True)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    valence = Column(Float)
    liveness = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    time_signature = Column(Integer)

    user_ply_lst = relationship('UserPlaylist',
                                backref='track_id',
                                uselist=False)

    def __repr__(self):
        return "<Tracks Data(danceability='%s', energy='%s', key='%s',\
                            loudness='%s', mode='%s', speechiness='%s',\
                            acousticness='%s', instrumentalness='%s',\
                            liveness='%s', valence='%s', tempo='%s',\
                            duration_ms='%s', time_signature='%s')>" % (
                                                        self.danceability,
                                                        self.energy,
                                                        self.key,
                                                        self.loudness,
                                                        self.mode,
                                                        self.speechiness,
                                                        self.acousticness,
                                                        self.instrumentalness,
                                                        self.valence,
                                                        self.liveness,
                                                        self.tempo,
                                                        self.duration_ms,
                                                        self.time_signature
                                                        )


class UserPlaylist(Base):
    '''When running this class, make sure to set the user_id arg to the
        user object it corresponds to; same goes for the track_id arg
        (note: track_id is diff from tracks_id) to the tracks object
        user_id = User()object  to fill the u_id arg ForeignKey
        track_id = Tracks()object  to fill the tracks_id arg ForeignKey'''

    __tablename__ = 'user_playlist'

    id = Column(Integer, primary_key=True, index=True)
    u_id = Column(String, ForeignKey('user.id'))           # User_ID
    tracks_id = Column(String, ForeignKey('tracks.id'))    # Track_ID
    uri = Column(String)                                   # Playlist_URI

    def __repr__(self):
        return "<User Playlist(u_id='%s',\
                                tracks_id='%s',\
                                uri='%s')>" % (
                                        self.u_id,
                                        self.tracks_id,
                                        self.uri
                                        )
