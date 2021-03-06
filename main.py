"""To activate FastAPI, See the doc string in the __init__.py file.

For documentation on FastAPI continue to the following link:

https://fastapi.tiangolo.com
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# from api.visualization import visualize
from api.models import playlist_model
# from visualization import visualize
# from models import playlist_model

load_dotenv()


def create_app():
    """Create app in __init__ file."""
    app = FastAPI(
                 tltle='ML API',
                 description='API for Spotify playlist generator.\
                             The playlists are generated from two users, and\
                             their most related interests.',
                 version='0.1',
                 docs_url='/',
                 )

    app.include_router(playlist_model.router)

    # may potentially be used to return data
    # app.include_router(.router)

    app.add_middleware(
                      CORSMiddleware,
                      allow_origins=['*'],
                      allow_credentials=True,
                      allow_methods=['*'],
                      allow_headers=['*'],
                      )
    return app


if __name__ == '__main__':
    uvicorn.run(create_app())
