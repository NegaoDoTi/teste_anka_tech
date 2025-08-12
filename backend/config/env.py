from dotenv import load_dotenv
from os import getenv

load_dotenv("./backend/.env")

DATABASE_URL = getenv("DATABASE_URL")
RABBITMQ_URL = getenv("RABBITMQ_URL")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DEBUG = bool(eval(getenv("DEBUG")))
PORT = int(getenv("PORT"))
RABBIT_QUEUE = getenv("RABBIT_QUEUE")