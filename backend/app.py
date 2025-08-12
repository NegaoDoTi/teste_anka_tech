from fastapi import FastAPI
from uvicorn import run
from config.env import DEBUG, PORT
from routes.upload import upload_route

app = FastAPI(debug=DEBUG)
app.include_router(upload_route)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=PORT)