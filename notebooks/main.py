from fastapi import FastAPI

app = FastAPI()

# Notes to make:
# main refers to the file (aka: python module)
# app: the object created inside of main.property
# --reload: make server restart after code changes; use for development


@app.get('/')
async def root():
    return {'Something stating that it works': "Hello World!"}
