# Entry point for spoti app
# To run app localy and generate access to data run
# the following line of code int he terminal:
# running with FastAPI this time
# uvicorn main:app --reload

'''Entry point for FastAPI application.'''

from .app import create_app  # imports the app creation function

# Initialize FastAPI app
APP = create_app()
