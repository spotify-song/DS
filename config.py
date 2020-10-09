from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ML API"
    database_url: str
    spotify_client_id: str
    spotify_user_id: str
    spotify_client_secret: str
    uri: str

    class Config:
        env_file = ".env"
