FROM python:3.7

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# This lets Heroku dynamically inject the correct port
CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT
