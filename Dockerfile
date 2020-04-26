FROM python:3.8.2-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /data/nginx /app

WORKDIR /app

COPY app.py .
EXPOSE 5000
CMD [ "python", "./app.py" ]