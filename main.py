# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.visualization import visualize
from api.models import playlist_model

app = FastAPI(
             tltle='ML API',
             description='API for Spotify playlist generator.  The playlists are generated from two users, and their most related interests.',
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

if __name__ == '__main__':
    uvicorn.run(app)
