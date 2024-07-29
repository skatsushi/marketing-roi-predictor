FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

