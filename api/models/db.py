"""Data Base table modles.

See README file for documentation, and more insight on relevant information.
"""

from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

load_dotenv()

# Connecting to DB
engine = create_engine(getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """User table contains relavent features that will be stored in the DB."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(String, unique=True, nullable=False)
    display_name = Column(String, unique=False, nullable=True)

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
        """Return style for User class."""
        return "<User(spot_id='%s', display_name='%s')>" % (
                                                            self.spot_id,
                                                            self.display_name
                                                            )


class Tokens(Base):
    """Token class for user tokens."""

    __tablename__ = 'track_token'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, nullable=False)
    token_type = Column(String, unique=False)
    expires_in = Column(Integer, unique=False)
    refresh_token = Column(String, unique=True)
    scope = Column(String, unique=False)
    user = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        """Return style for api."""
        return "<Tokens(\
                        id='%s',\
                        access_token='%s',\
                        token_type='%s',\
                        expires_in='%s',\
                        refresh_token='%s',\
                        scope='%s',\
                        user='%s')>" % (
                                        self.id,
                                        self.access_token,
                                        self.token_type,
                                        self.expires_in,
                                        self.refresh_token,
                                        self.scope,
                                        self.user
                                        )


class Tracks(Base):
    """Track class containing track audio data."""

    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    loudness = Column(Float, nullable=True)
    mode = Column(Integer, nullable=True)
    speechiness = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    liveness = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    time_signature = Column(Integer, nullable=True)
    spot_id = Column(String, nullable=False)

    user_ply_lst = relationship('UserPlaylist',
                                backref='track_id',
                                uselist=False)

    def __repr__(self):
        """Return print style for track class."""
        return "<Tracks Data(id='%s', danceability='%s', energy='%s',\
                            key='%s', loudness='%s', mode='%s',\
                            speechiness='%s', acousticness='%s',\
                            instrumentalness='%s', liveness='%s',\
                            valence='%s', tempo='%s', duration_ms='%s',\
                            time_signature='%s', spot_id='%s')>" % (
                                                        self.id,
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
                                                        self.time_signature,
                                                        self.spot_id
                                                        )


class UserPlaylist(Base):
    """Plalist class to store in DB.

    When running this class, make sure to set the user_id arg to the
    user object it corresponds to; same goes for the track_id arg
    (note: track_id is diff from tracks_id) to the tracks object
    user_id = User() object  to fill the u_id arg ForeignKey
    track_id = Tracks() object  to fill the tracks_id arg ForeignKey.
    """

    __tablename__ = 'user_playlist'

    id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey('user.id'))  # User_ID
    tracks_id = Column(
                    Integer,
                    ForeignKey('tracks.id'),
                    nullable=True)  # Track_ID
    uri = Column(String, nullable=True)  # Playlist_URI

    def __repr__(self):
        """Return style for playlist class."""
        return "<User Playlist(id='%s',\
                                u_id='%s',\
                                tracks_id='%s',\
                                uri='%s')>" % (
                                        self.id,
                                        self.u_id,
                                        self.tracks_id,
                                        self.uri
                                        )
