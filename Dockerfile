FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

# Change CMD to exec form
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]