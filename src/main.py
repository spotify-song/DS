from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from visualization import visualize
from models import predict

app = FastAPI(
             tltle='ML API',
             description='Lorem ipsum',
             version='0.1',
             docs_url='/',
             )


app.include_router(predict.router)
app.include_router(visualize.router)

app.add_middleware(
                  CORSMiddleware,
                  allow_origins=['*'],
                  allow_credentials=True,
                  allow_methods=['*'],
                  allow_headers=['*'],
                  )

if __name__ == '__main__':
    uvicorn.run(app)
