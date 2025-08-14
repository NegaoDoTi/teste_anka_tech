from fastapi import FastAPI
from uvicorn import run
from config.env import DEBUG, PORT
from routes.upload import upload_route
from routes.usage import usage_route
import logging

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] - %(message)s",)


app = FastAPI(debug=DEBUG)
app.include_router(upload_route)
app.include_router(usage_route)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=PORT)