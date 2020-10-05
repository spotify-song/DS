# Entry point for spoti app
# To run app localy and generate access to data run
# the following line of code int he terminal:
# running with FastAPI this time
# uvicorn main:app --reload

'''Entry point for FastAPI application.'''

# imports the app creation function

# Initialize FastAPI app

# uvicorn main:app --reload

from main import create_app

APP = create_app()
