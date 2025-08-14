FROM python:3.11
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN alembic revision --autogenerate -m "Primeira  migration"
RUN alembic upgrade head
CMD ["./start.sh"]