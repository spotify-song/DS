"""Entry point for FastAPI application.

To run API locally, and access FastAPI UI, run the following code into the
terminal from the parent directory; in this case the parent directory is DS.

Code to run: uvicorn __init__:APP --reload

uvicorn: Is the ASGI server implementations using uvloop and httpools.

__init__: Is the first file to be loaded in module, that contains the necessary
code to be executed.

APP: Instantiates the API.

--reload: Activates debug mode for the API so that changes can be made in and
ovserved in real time.
"""

from main import create_app

APP = create_app()
