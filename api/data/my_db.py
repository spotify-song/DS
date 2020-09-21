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

    # Backref allows you to update values in a different table
    # set the table name then the back arg will be used as the psudo
    # column that will fill the foreign key in the corresponding table
    # in the case of the value below, the 'token' value will be used to
    # fill the 'user_id' column in the 'Tokens' table
    # Ex: Tokens(all_token_column_names=all_token_values,
    #            user_token=User(object))
    token = relationship('Tokens', backref='user_token', uselist=False)
    user_playlist = relationship('UserPlaylist', backref='user_id')

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
            self.access_token,
            self.token_type,
            self.expires_in,
            self.refresh_token,
            self.scope,
            self.expires_at,
            self.user,
            self.user_id
            )


class Tracks(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    accousticness = Column(Float)
    instrumentalness = Column(Float)
    valence = Column(Float)
    liveness = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    time_signature = Column(Integer)

    user_ply_lst = relationship('UserPlaylist',
                                backref='track_id',
                                uselist=False)
    top_tracks = relationship('TopTracks',
                              backref='trx_id',
                              uselist=False)

    def __repr__(self):
        return "<Tracks Data(danceability='%s', energy='%s', key='%s',\
                loudness='%s', mode='%s', speechiness='%s',\
                accousticness='%s', instrumentalness='%s',\
                liveness='%s', valence='%s', tempo='%s', type='%s',\
                duration_ms='%s', time_signature='%s')" % (
                                                        self.danceability,
                                                        self.energy,
                                                        self.key,
                                                        self.loudness,
                                                        self.mode,
                                                        self.speechiness,
                                                        self.accousticness,
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
    u_id = Column(Integer, ForeignKey('users.id'))
    tracks_id = Column(Integer, ForeignKey('tracks.id'))
    uri = Column(String)

    def __repr__(self):
        return "<User Playlist(u_id='%s', tracks_id='%s', uri='%s')" % (
                                                    self.u_id,
                                                    self.tracks_id,
                                                    self.uri
                                                    )


class TopTracks(Base):
    '''When running make sure to set the following args:
        trx_id=Tracks()object to fill the ForeignKey for the track_id arg'''
    __tablename__ = 'top_tracks'

    id = Column(Integer, primary_key=True, index=True)
    track = Column(String, unique=True, nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'))

    def __repr__(self):
        return "<Top Tracks(track='%s', track_id='%s')" % (
                                                self.track,
                                                self.track_id
                                                )
